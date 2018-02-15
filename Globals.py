import Models
from nltk.corpus import cmudict

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
target_reading_level = ''
target_reading_score = Models.ReadingScoreRange()
target_reading_level = ''
should_modify = False
full_output = ''

