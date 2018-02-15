import Models
import Globals
import main
import math
import re
import Contractions

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
    if acceptable_score(Globals.reading_level_score):
        # Score is already within acceptable range
        print('Text is within target range')
    else:
        # Need to adjust score
        # start by adjusting contractions
        # Is the current score greater than the highest score in range?
        # (I.e is it below the lowest value for that grade)
        should_raise = Globals.reading_level_score > Globals.target_reading_score.high_score
        print("Adjusting Contractions")
        net_word_change = adjust_contractions(should_raise)
        # Estimated score is based on the estimate that expanding/shrinking a contraction
        # has a net change of 1 word and 1 syllable
        estimated_score = main.calculate_reading_level_score(Globals.total_words + net_word_change,
                                                             Globals.total_sentences,
                                                             Globals.total_syllables + net_word_change)
        if acceptable_score(estimated_score):
            print("New Reading level score " + str(estimated_score))
            print("Score is within target range")
        else:
            print("Attempting to replace with synonyms")

        # Write output file
        output_file = open("output.txt", "w")
        output_file.write(Globals.full_output)
        output_file.close()


def adjust_contractions(should_raise):
    total_contractions = 0
    Globals.full_output = Globals.full_input
    if should_raise:
        # Raising difficulty -> shrink contractions
        for phrase in Contractions.expanded_as_key:
            # Count lowercase version of phrase + phrase with capitalized first letter
            total_contractions += Globals.full_output.count(phrase) + \
                                  Globals.full_output.count(phrase[0].upper() + phrase[1:])
            # Replace lowercase phrase
            Globals.full_output = Globals.full_output.replace(phrase, Contractions.expanded_as_key[phrase])
            # Replace phrase with first letter capitalized (ex. Can not -> Can't)
            Globals.full_output = Globals.full_output.replace(phrase[0].upper() +
                                                              phrase[1:],
                                                              Contractions.expanded_as_key[phrase][0].upper() +
                                                              Contractions.expanded_as_key[phrase][1:])
    else:
        # Lowering difficulty -> expand contractions
        for contraction in Contractions.contractions_as_key:
            # Count lowercase version of contraction + contractions with capitalized first letter
            total_contractions += Globals.full_output.count(contraction) + \
                                  Globals.full_output.count(contraction[0].upper() + contraction[1:])
            # Replace lowercase contraction
            Globals.full_output = Globals.full_output.replace(contraction,
                                                              Contractions.contractions_as_key[contraction])
            # Replace contractions with first letter capitalized (ex. Can't -> Can not)
            Globals.full_output = Globals.full_output.replace(contraction[0].upper() +
                                                              contraction[1:],
                                                              Contractions.contractions_as_key[contraction][0].upper() +
                                                              Contractions.contractions_as_key[contraction][1:])
    # Return net result in words added/removed
    return (-1 * total_contractions) if should_raise else total_contractions


def acceptable_score(score):
    return Globals.target_reading_score.low_score <= score <= Globals.target_reading_score.high_score


def calculate_needed_contractions():
    target_score = (Globals.target_reading_score.high_score + Globals.target_reading_score.low_score) / 2

    # Below are two candidate roots of the equation which determine number of words needed to achieve a certain reading score
    # Note: these can throw errors (due to root of 0) which seem to happen when trying to make major changes to reading level
    # candidate = -1 * ((-206835 * Globals.total_sentences) + (1000 * target_score * Globals.total_sentences) -
    #                  math.sqrt(((206835 * Globals.total_sentences) -
    #                             (1000 * target_score * Globals.total_sentences)) ** 2 -
    #                            (343476000 * Globals.total_sentences * Globals.total_syllables))) / 2030
    words_needed = -1 * ((-206835 * Globals.total_sentences) + (1000 * target_score * Globals.total_sentences) +
                         math.sqrt(((206835 * Globals.total_sentences) -
                                    (1000 * target_score * Globals.total_sentences)) ** 2 -
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
