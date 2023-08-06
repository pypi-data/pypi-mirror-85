import os

from .textstat import TextStat
from .files import TextStatFile


class TextStatCli(object):
    """
    Wrapper for textstat
    """

    TEXTSTAT = TextStat
    TEXTSTATFILE = TextStatFile

    ACCEPTABLE_FILE_EXTENSIONS = ["txt", "md"]

    # methods in textstat for analysing text
    TESTS = {
        "Syllable Count": "syllable_count",
        "Lexion Count": "lexicon_count",
        "Reading time in minutes slowly": "time_to_read_100wpm",
        "Reading time in minutes at average speed": "time_to_read_130wpm",
        "Reading time in minutes fast": "time_to_read_160wpm",
        "Flesch Reading Ease": "flesch_reading_ease",
        "Smog Index": "smog_index",
        "Flesch Kincaid Grade": "flesch_kincaid_grade",
        "Coleman Liau Index": "coleman_liau_index",
        "Automated Readability Index": "automated_readability_index",
        "Automated Readability Index": "automated_readability_index",
        "Dale/Chall Readability Score": "dale_chall_readability_score",
        "Difficult Words": "difficult_words",
        "Linsear Write Formula": "linsear_write_formula",
        "Gunning Fog": "gunning_fog",
        "Text Standard": "text_standard",
    }

    @classmethod
    def from_args(cls, args):
        """Initialises this class based on the results of argparse Namespace
        defined in __main__.create_args().

        :param args: :class:`argparse.Namespace` like object to populate this
            class
        """
        return cls(paths=args.path, language=args.language)

    def __init__(self, paths, language="en_US"):
        """
        :param paths: A list of paths as strings to look for files to run the
            tests against.
        :type paths: list
        :param language: :class:`textstat.textstat` defined language string
        """
        self.paths = paths
        self.language = language

        self._textstat = None
        self._files = []

    @property
    def textstat(self):
        """Textstat singleton that is used throughought this library."""
        if not self._textstat:
            self._textstat = self.TEXTSTAT(language=self.language)
        return self._textstat

    @property
    def files(self):
        """A list of all the files to scan, based upon initial root path.
        Only lists files that have the right file extension.
        Wraps those files in to the TextStatFile object.
        """
        if not self._files:
            self._paths_walk()
        return self._files

    def _paths_walk(self):
        for path in self.paths:
            if os.path.isfile(path):
                self._claim_file(path)
            else:
                for root_path, _, file_names, _ in os.fwalk(path):
                    for file_name in file_names:
                        file_path = os.path.join(root_path, file_name)
                        self._claim_file(file_path)

    def _claim_file(self, file_path):
        """Takes file path, does some checks, and adds it to the files list if
        it meets the criteria.

        :param file_path: The path to the file to check
        :type file_path: str
        """
        if self._extension_ok(file_path):
            self._add_file(file_path)

    def _extension_ok(self, file_name):
        """Pass in a file path to see if the file is OK to be processed.

        :param file_path: Path of file to be checked
        :type file_path: str

        :return: True if this file is OK to process. False if not and should be
            rejected.
        :rtype: bool
        """
        # get the file extension, or the thing after the last dot
        # in the file name, to see if it's on the approved list
        extension = file_name.rsplit(".", maxsplit=1)[-1].lower()
        return extension in self.ACCEPTABLE_FILE_EXTENSIONS

    def _add_file(self, file_path):
        """Wraps file in processor object and adds to list of local variables

        :param file_path: Path of file to add
        :type file_path: str
        """
        self._files.append(self.TEXTSTATFILE.from_path(file_path, self))

    def to_dict(self):
        """Get all the results as a python dictionary object. Useful for converting
        to JSON.
        """
        return dict(
            [
                (textstatfile.f.name, textstatfile.to_dict())
                for textstatfile in self.files
            ]
        )
