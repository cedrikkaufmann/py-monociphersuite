class IfStream:

    def __init__(self, file):
        super().__init__()

        # check if file is string
        if type(file) != str:
            raise Exception('File has to be of type string')

        try:
            # open file
            f = open(file, 'r')
            # read file content
            content = f.read()

            # filter alphabetic chars
            content = filter(lambda c: True if (c.isalpha() and c.isascii()) else False, content)
            content = ''.join(content)

            # convert to lowercase
            self._data = content.lower()

        finally:
            # finally close file
            f.close()

    def read(self):
        return enumerate(self._data)

    @property
    def data(self):
        return self._data