class TextStatFile(object):
    """An object that represents files on your system to run the tests against."""

    OPEN_MODE = "r"

    @classmethod
    def from_path(cls, file_path, cli):
        """Initialise this class when you don't have a file object, but do have
        the file path.

        :param file_path: Path to file to process
        :type file_path: str
        :param cli: parent config object
        """
        return cls(open(file_path, cls.OPEN_MODE), cli)

    def __init__(self, f, cli):
        """
        :param f: file object to run methods in this function over
        :param cli: parent CLI object to get config from
        """
        self.f = f
        self.cli = cli

        self._text = None

    @property
    def text(self):
        """Get the contents of the file (memory inefficent)

        :return: Contents of file object this class was initialised with
        :rtype: str
        """
        if not self._text:
            self._text = self.f.read()
        return self._text

    def __getattr__(self, attr):
        """There are a lot of methods in textstat and they're likely to change.
        This is the lazy (i.e.: DRY) way of accessing those methods

        :param attr: Name of the attribute to access in this object

        :return: Attribute from self or from textstat
        """
        return lambda: getattr(self.cli.textstat, attr)(self.text)

    def to_dict(self):
        """For all of the tests/methods available in textstat, run through them
        all and produce the results as a dictionary.

        :return: A dictionary representation of the results
        :rtype: dict
        """
        return dict(
            (friendly_name, getattr(self, method_name)())
            for friendly_name, method_name in self.cli.TESTS.items()
        )
