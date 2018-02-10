import re
import sys

import nltk
from nltk.corpus import cmudict

""" Reading level analyzer and adapter.

This module reads in text from a file, analyzes the reading level, and allows 
for the increase or decrease of reading difficulty.

Example:
    The program can be run by the following command::

        $ python main.py input.txt

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""

dictionary = cmudict.dict()
input_file = ''
current_line_number = 0
full_input = ''
total_words = 0
total_sentences = 0
total_syllables = 0


def get_next_line():
    """
    Looks at the global line number and file and sets the given variable to the
    data at that line
    """
    global current_line_number
    current_line_data = ''

    # Open the file and loop until the requested line number is found
    with open(input_file) as file:

        for number, line in enumerate(file):
            if number == current_line_number:
                current_line_data = line
                break

    # If the line data was updated increment the current line number
    # and return the found data
    if current_line_data:
        current_line_number += 1
        return current_line_data
    else:
        return "!!!End of File!!!"


def get_syllables(words):
    """
    Uses the nltk corpus library to get the syllables of each word. If the word
    is not found in the cmu dictionary, it calls manually parses the word.

    Code in this section is based off of the following Stack Overflow post:
        https://datascience.stackexchange.com/questions/23376/
            how-to-get-the-number-of-syllables-in-a-word

    :param words: The list of words to be parsed
    :return: The total number of syllables
    """
    global dictionary

    number_of_syllables = 0

    for word in words:
        try:
            ''' If word is in the dictionary, get it's syllables list.
                Then take pronunciation wit the maximum syllables'''
            number_of_syllables += max(
                [len(list(y for y in x if y[-1].isdigit()))
                 for x in dictionary[word.lower()]])
        except KeyError:
            # The cmu dictionary didn't have the word so manually parse it
            number_of_syllables += manually_parse_syllables(word)

    return number_of_syllables


def manually_parse_syllables(word):
    """
    Manually finds the syllables in a word if
    the cmu dictionary did not have it.

    This code is referred from:
        https://www.stackoverflow.com/questions/14541303/
            count-the-number-of-syllables-in-a-word

    :param word: The word to be parsed
    :return: The number of syllables in the word
    """
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count


def strip_punctuation(tokens):
    """
    Strips the punctuation from the list of tokens.

    :param tokens: The list of words and punctuation from nltk
    :return: A list of words without punctuation
    """

    words_or_digits_only_regex = re.compile('.*[A-Za-z0-9].*')

    # If the word matches the regex, save it. Else ignore it
    words_only = [word for word in tokens if
                  words_or_digits_only_regex.match(word)]

    return words_only


def calculate_reading_level_score(number_of_words, number_of_sentences,
                                  number_of_syllables):
    """
    Calculates the reading level score of the file using the Flesh-Kincaid
    Reading Ease Formula.

    The formula is as follows:
        206.835 - 1.015 (Total Words / Total Sentences)
            - 84.6 (Total Syllables / Total Words)

    :param number_of_words: The number of words in the piece
    :param number_of_sentences: The number of sentences in the piece
    :param number_of_syllables: The number of syllables in the piece
    :return: The calculated reading level score from the Flesh-Kincaid Reading
    Ease Formula
    """
    first_flesh_kincaid_constant = 206.835
    second_flesh_kincaid_constant = 1.015
    third_flesh_kincaid_constant = 84.6

    return first_flesh_kincaid_constant - second_flesh_kincaid_constant * (
        number_of_words / number_of_sentences) - third_flesh_kincaid_constant * (
        number_of_syllables / number_of_words)


def main():
    """
    The main function
    """
    global full_input
    global total_words
    global total_sentences
    global total_syllables

    while True:
        # Parse each sentence
        sentence = get_next_line()

        if sentence == "!!!End of File!!!":
            break

        full_input += sentence
        total_sentences += 1

        tokens = nltk.word_tokenize(sentence)
        words = strip_punctuation(tokens)
        total_words += len(words)

        total_syllables += get_syllables(words)

    reading_level_score = calculate_reading_level_score(total_words,
                                                        total_sentences,
                                                        total_syllables)

    print("Total Sentences: " + str(total_sentences))
    print("Total Words: " + str(total_words))
    print("Total Syllables " + str(total_syllables))
    print("Reading Level Score " + str(reading_level_score))


if __name__ == "__main__":

    # Check for an input file
    if len(sys.argv) < 2:
        print("Input file required")
        print("On EOS Try: python3 main.py input.txt")
        sys.exit(2)
    elif len(sys.argv) > 2:
        print("Too many arguments")
        print("On EOS Try: python3 main.py input.txt")
        sys.exit(2)
    else:
        # Get file
        input_file = sys.argv[1]

    # Run the program
    main()
