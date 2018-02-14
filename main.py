import re
import sys
import ChangeLevel
import nltk
import Globals
from nltk.corpus import cmudict

""" Reading level analyzer.

This module reads in text from a file and analyzes the reading level.

Example:
    The program can be run by the following command::

        $ python main.py input.txt

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


def get_next_line():
    """
    Looks at the global line number and file and sets the given variable to the
    data at that line
    """
    current_line_data = ''

    # Open the file and loop until the requested line number is found
    with open(Globals.input_file) as file:

        for number, line in enumerate(file):
            if number == Globals.current_line_number:
                current_line_data = line
                break

    # If the line data was updated increment the current line number
    # and return the found data
    if current_line_data:
        Globals.current_line_number += 1
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

    number_of_syllables = 0

    for word in words:
        try:
            ''' If word is in the dictionary, get it's syllables list.
                Then take pronunciation wit the maximum syllables'''
            number_of_syllables += max(
                [len(list(y for y in x if y[-1].isdigit()))
                 for x in Globals.dictionary[word.lower()]])
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
    words_or_digits_only_regex = re.compile('.*\w+.*')

    # If the word matches the regex, save it. Else ignore it
    words_only_with_contractions = [word for word in tokens if
                                    words_or_digits_only_regex.match(word)]

    remove_contractions_regex = re.compile("\w*'\w*")
    # Remove all the contractions as nltk counts them as 2 words
    words_only = [word for word in words_only_with_contractions if
                  not remove_contractions_regex.match(word)]

    return words_only


def get_number_of_sentences(file_text):
    """
    Calculates the number of sentences based on the punctuation using regex.

    :param file_text: The text in the file
    :return: The number of sentences
    """

    ''' 
    Regex that looks for punctuation, followed by an optional
    quotation mark, followed by white space and/or a new line, followed by
    a capital letter or a quotation mark. Should match text such as 
    the following:
        . "
        . T
        ."\n"        
    '''
    end_of_sentence_regex = re.compile('(([.!?])"*(\s+|\n+)([A-Z]|"))')

    number_of_sentences = len(
        re.findall(end_of_sentence_regex, file_text)
    ) + 1  # +1 accounts for the last sentence

    return number_of_sentences


def calculate_reading_level_score(number_of_words, number_of_sentences,
                                  number_of_syllables):
    """
    Calculates the reading level score of the file using the Flesch-Kincaid
    Reading Ease Formula.

    The formula is as follows:
        206.835 - 1.015 (Total Words / Total Sentences)
            - 84.6 (Total Syllables / Total Words)

    :param number_of_words: The number of words in the piece
    :param number_of_sentences: The number of sentences in the piece
    :param number_of_syllables: The number of syllables in the piece
    :return: The calculated reading level score from the Flesch-Kincaid Reading
    Ease Formula
    """
    first_flesch_kincaid_constant = 206.835
    second_flesch_kincaid_constant = 1.015
    third_flesch_kincaid_constant = 84.6

    return first_flesch_kincaid_constant - second_flesch_kincaid_constant * (
        number_of_words / number_of_sentences) \
        - third_flesch_kincaid_constant * (
        number_of_syllables / number_of_words)


def convert_score_to_reading_level(score):
    """
    Converts the score from the Flesch-Kincaid Reading Ease Formula into the
    equivalent reading level.

    :param score: The score calculated from the
                    Flesch-Kincaid Reading Ease Formula
    :return: The description of the reading level
    """
    if 100.0 >= score >= 90.0:
        return "5th Grade Reading Level"
    elif 90.0 > score >= 80.0:
        return "6th Grade Reading Level"
    elif 80.0 > score >= 70.0:
        return "7th Grade Reading Level"
    elif 70.0 > score >= 60.0:
        return "8th & 9th Grade Reading Level"
    elif 60.0 > score >= 50.0:
        return "10th to 12th Grade Reading Level"
    elif 50.0 > score >= 30.0:
        return "College Reading Level"
    elif 30.0 > score >= 0:
        return "College Graduate Reading Level"
    else:  # Got a number greater than 100, or less than 0.
        return "A reading level so complex, it cannot be classified."


def main():
    """
    The main function
    """

    with open(Globals.input_file) as file:
        Globals.file_content = file.read()

    while True:
        # Parse each sentence
        sentence = get_next_line()

        if sentence == "!!!End of File!!!":
            break

        Globals.full_input += sentence

        tokens = nltk.word_tokenize(sentence)

        # Update global tokens (which contains all tokens)
        Globals.tokens += tokens

        words = strip_punctuation(tokens)
        Globals.total_words += len(words)

        Globals.total_syllables += get_syllables(words)

    Globals.total_sentences = get_number_of_sentences(Globals.file_content)

    Globals.reading_level_score = calculate_reading_level_score(Globals.total_words,
                                                        Globals.total_sentences,
                                                        Globals.total_syllables)

    reading_level = convert_score_to_reading_level(Globals.reading_level_score)

    print("Total Sentences: " + str(Globals.total_sentences))
    print("Total Words: " + str(Globals.total_words))
    print("Total Syllables " + str(Globals.total_syllables))
    print("Reading Level Score " + str(Globals.reading_level_score))
    print("Reading Level: " + str(reading_level))

    if Globals.should_modify:
        print("Changing Reading Level to " + Globals.target_reading_level)
        ChangeLevel.change_level()


if __name__ == "__main__":

    # Check for an input file
    if len(sys.argv) == 2:
        # Analyze reading level data
        Globals.input_file = sys.argv[1]
    elif len(sys.argv) == 3:
        # Analyze reading data and modify to reach target
        Globals.input_file = sys.argv[1]
        Globals.should_modify = True
        Globals.target_reading_level = sys.argv[2]
    elif len(sys.argv) < 2:
        print("Too few arguments provided")
        print("On EOS Try: python3 main.py input.txt {targetLevel}")
        sys.exit(2)
    elif len(sys.argv) > 3:
        print("Too many arguments")
        print("On EOS Try: python3 main.py input.txt {targetLevel}")
        sys.exit(2)

    # Run the program
    main()
