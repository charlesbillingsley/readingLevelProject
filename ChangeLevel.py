import Models
import Globals
import main
""" Reading level adapter.

This module allows for the increase or decrease of reading difficulty.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


def change_level():
    Globals.target_reading_level = convert_reading_level_to_score(Globals.target_reading_level)


def convert_reading_level_to_score(reading_level):
    """
    Converts the reading level from the Flesch-Kincaid Reading Ease Formula
    into the equivalent reading score.

    :param reading_level: The grade level
    :return: The score range associated with the reading level
    """
    if reading_level == '5':
        return Models.ReadingScoreRange(90, 100)
    elif reading_level == '6':
        return Models.ReadingScoreRange(80, 90)
    elif reading_level == '7':
        return Models.ReadingScoreRange(70, 80)
    elif reading_level == '8' or reading_level == '9':
        return Models.ReadingScoreRange(60, 70)
    elif reading_level == '10' or reading_level == '11' \
            or reading_level == '12':
        return Models.ReadingScoreRange(50, 60)
    elif reading_level == 'College':
        return Models.ReadingScoreRange(30, 50)
    elif reading_level == 'CollegeGrad':
        return Models.ReadingScoreRange(0, 30)
