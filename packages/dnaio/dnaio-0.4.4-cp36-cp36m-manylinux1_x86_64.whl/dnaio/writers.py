from xopen import xopen

from ._util import _is_path


class FileWriter:
    def __init__(self, file, opener=xopen, _close_file=None):
        self._file = file
        if _is_path(file):
            self._file = opener(file, "wb")
            self._close_on_exit = True
        else:
            self._close_on_exit = bool(_close_file)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, getattr(self._file, "name", self._file))

    def close(self):
        if self._close_on_exit:
            self._file.close()

    def __enter__(self):
        if self._file.closed:
            raise ValueError("I/O operation on closed file")
        return self

    def __exit__(self, *args):
        self.close()


class FastaWriter(FileWriter):
    """
    Write FASTA-formatted sequences to a file.
    """

    def __init__(self, file, line_length=None, opener=xopen, _close_file=None):
        """
        If line_length is not None, the lines will
        be wrapped after line_length characters.
        """
        super().__init__(file, opener=opener, _close_file=_close_file)
        self.line_length = line_length if line_length != 0 else None

    def __repr__(self):
        return "FastaWriter('{}')".format(getattr(self._file, "name", self._file))

    def write(self, name_or_record, sequence=None):
        """Write an entry to the the FASTA file.

        If only one parameter (name_or_record) is given, it must have
        attributes .name and .sequence, which are then used.
        Otherwise, the first parameter must be the name and the second
        the sequence.

        The effect is that you can write this:
        writer.write("name", "ACCAT")
        or
        writer.write(Sequence("name", "ACCAT"))
        """
        if sequence is None:
            name = name_or_record.name
            sequence = name_or_record.sequence
        else:
            name = name_or_record

        if self.line_length is not None:
            self._file.write(('>' + name + '\n').encode('ascii'))
            s = []
            for i in range(0, len(sequence), self.line_length):
                s.append(sequence[i:i + self.line_length] + '\n')
            self._file.write(''.join(s).encode('ascii'))
        else:
            s = '>' + name + '\n' + sequence + '\n'
            self._file.write(s.encode('ascii'))


class FastqWriter(FileWriter):
    """
    Write sequences with qualities in FASTQ format.

    FASTQ files are formatted like this:
    @read name
    SEQUENCE
    +
    QUALITIS
    """
    file_mode = 'wb'

    def __init__(self, file, two_headers=False, opener=xopen, _close_file=None):
        super().__init__(file, opener=opener, _close_file=_close_file)
        self._two_headers = two_headers
        self.write = self._write_two_headers if self._two_headers else self._write

    def __repr__(self):
        return "FastqWriter('{}')".format(getattr(self._file, "name", self._file))

    def _write(self, record):
        """
        Write a Sequence record to the FASTQ file.

        """
        self._file.write(record.fastq_bytes())

    def _write_two_headers(self, record):
        """
        Write a Sequence record to the FASTQ file, repeating the header
        in the third line after the "+" .
        """
        self._file.write(record.fastq_bytes_two_headers())

    def writeseq(self, name, sequence, qualities):
        self._file.write("@{0:s}\n{1:s}\n+\n{2:s}\n".format(
            name, sequence, qualities).encode('ascii'))
