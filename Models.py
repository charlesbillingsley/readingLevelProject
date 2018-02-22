
""" Data Models.

This module holds models for reading level data.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


class ReadingScoreRange:
    """
        Holds the range of reading scores.
    """
    low_score = 0
    high_score = 0

    def __init__(self, low_score=0, high_score=0):
        """
        Constructor for the range of reading scores.

        :param low_score: the low score value
        :param high_score: the high score value
        """
        self.low_score = low_score
        self.high_score = high_score
