
""" Data Models.

This module holds models for reading level data.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


class ReadingScoreRange:
    low_score = 0
    high_score = 0

    def __init__(self, low_score=0, high_score=0):
        self.low_score = low_score
        self.high_score = high_score
