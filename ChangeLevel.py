import Models
import Globals
import main
import math
""" Reading level adapter.

This module allows for the increase or decrease of reading difficulty.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


def change_level():
    Globals.target_reading_score = convert_reading_level_to_score(Globals.target_reading_level)
    if Globals.reading_level_score >= Globals.target_reading_score.low_score and \
            Globals.reading_level_score <= Globals.target_reading_score:
        # Score is already within acceptable range
        print('Text is within target range')
    else:
        # Need to adjust score
        if adjust_contractions():
            # Adjusting contractions should achieve reading level
            # run main.main() to re-evaluate and pass through again
            print("Adjusting Contractions")
        else:
            # Contractions didn't do enough
            adjust_syllables()
            print('One pass through level changer, evaluating again')


def adjust_contractions():
    calculate_needed_contractions()
    return True


def adjust_syllables():
    return True


def calculate_needed_contractions():
    target_score = (Globals.target_reading_score.high_score + Globals.target_reading_score.low_score) / 2

    # Below are two candidate roots of the equation which determine number of words needed to achieve a certain reading score
    # Note: these can throw errors (due to root of 0) which seem to happen when trying to make major changes to reading level
    #candidate = -1 * ((-206835 * Globals.total_sentences) + (1000 * target_score * Globals.total_sentences) -
    #                  math.sqrt(((206835 * Globals.total_sentences) -
    #                             (1000 * target_score * Globals.total_sentences)) ** 2 -
    #                            (343476000 * Globals.total_sentences * Globals.total_syllables))) / 2030
    words_needed = -1 * ((-206835 * Globals.total_sentences) + (1000 * target_score * Globals.total_sentences) +
                  math.sqrt(((206835 * Globals.total_sentences) -
                             (1000 * target_score * Globals.total_sentences))**2 -
                            (343476000 * Globals.total_sentences * Globals.total_syllables))) / 2030
    word_difference = Globals.total_words - words_needed
    # Determine if we need to add or remove words (increase or decrease complexity)
    # Also check total number of contractions present.
    # either expand or contract them until word difference is achieved

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
