from textstat.textstat import textstatistics as TextStatistics


class TextStat(TextStatistics):
    """Over-rides the `textstatistics` class because of weirdnesses in the way it
    was written such as lack of PEP8 and not having an `init`.
    """

    def __init__(self, language=None):
        """
        :param args: :class:`argparse.Namespace` like object to populate this
            class
        """
        super(TextStat, self).__init__()
        if language:
            self.set_lang(language)

    def reading_speed(self, text, speed):
        """Estimate how long a block of text takes to read based upon number of
        words and how many words a reader can read per minute.

        :param text: The text to check for the amount of words
        :param speed: How many words per minute the reader should be able to do

        :return: How long it would take to read the text in minutes
        :rtype: float
        """
        return self.lexicon_count(text) / speed

    def time_to_read_100wpm(self, text):
        """Estimate how long a block of text takes to read at a slow reading
        speed.

        :param text: The text to check for the amount of words

        :return: How long it would take to read the text in minutes
        :rtype: float
        """
        return self.reading_speed(text, 100)

    def time_to_read_130wpm(self, text):
        """Estimate how long a block of text takes to read at an average reading
        speed.

        :param text: The text to check for the amount of words

        :return: How long it would take to read the text in minutes
        :rtype: float
        """
        return self.reading_speed(text, 130)

    def time_to_read_160wpm(self, text):
        """Estimate how long a block of text takes to read at a fast reading
        speed.

        :param text: The text to check for the amount of words

        :return: How long it would take to read the text in minutes
        :rtype: float
        """
        return self.reading_speed(text, 160)
