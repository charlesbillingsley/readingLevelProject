from nltk.corpus import cmudict

""" Global variables.

This module holds the global variables for the reading level application.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""

# Main Globals
dictionary = cmudict.dict()
input_file = ''
file_content = ''
current_line_number = 0
full_input = ''
total_words = 0
total_sentences = 0
total_syllables = 0
tokens = []
reading_level_score = 0

# ChangeLevel Globals
target_raise = False  # True to make more difficult, False to make easier.
should_modify = False
full_output = ''

