import Models
from nltk.corpus import cmudict

""" Global variables for the reading level project.

This module holds the global variables for the project.

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
target_reading_level = ''
shouldModify = False

# ChangeLevel Globals
target_reading_level = ''
target_reading_score = Models.ReadingScoreRange()


