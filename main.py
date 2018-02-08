import nltk
import sys

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

input_file = ''
current_line_number = 0


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


def calculate_reading_level():
    """
    Calculates the reading level of the file.
    """
    # Todo: figure out what needs to be passed in.
    # Todo: add the calculation given in class to this method


def main():
    """
    The main function
    """

    while True:
        sentence = get_next_line()

        if sentence == "!!!End of File!!!":
            break

        # Example of tokenizing from the nltk documentation
        print(sentence.strip('\n'))
        tokens = nltk.word_tokenize(sentence)
        print(tokens)
        tagged = nltk.pos_tag(tokens)
        print(tagged[0:6])
        print('\n')


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
