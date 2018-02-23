import Models
import Globals
import main
import Contractions
import nltk
import pywsd
from nltk.corpus import wordnet

""" Reading level adapter.

This module allows for the increase or decrease of reading difficulty.

Authors:
    Charles Billingsley
    Josh Getter
    Adam Stewart
    Josh Techentin

"""


def change_level():
    # Make the text as difficult as we can, or as easy as we can.
    should_raise = Globals.target_raise
    adjust_contractions(should_raise)
    adjust_syllables(should_raise)
    adjust_sentences(should_raise)
    # Write output file
    output_file = open("output.txt", "w")
    output_file.write(Globals.full_output)
    output_file.close()
    print("The change is complete!")


def adjust_contractions(should_raise):
    print("Adjusting Contractions")
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


# Adjust syllables to either raise or lower difficulty
def adjust_syllables(should_raise):
    print("Finding Synonyms")
    # disambiguate words automatically
    temp_sentence = ''
    sentences = nltk.sent_tokenize(Globals.full_output)
    Globals.full_output = ''
    for sentence in sentences:
        # Get tokens from sentence
        tokens = pywsd.disambiguate(sentence)
        for index, token in enumerate(tokens):
            if index + 1 < len(tokens):
                if Contractions.contractions_as_key.get(tokens[index][0] + tokens[index + 1][0]):
                    # Don't find synonyms for contractions
                    temp_sentence += " " + token[0]
                    continue
            synset = token[1]
            if synset:
                # If token has synonyms -> Get max or min syllable'd synonym
                matched_synonym = max(synset.lemma_names(), key=main.get_syllables) if should_raise else min(
                    synset.lemma_names(), key=main.get_syllables)
                temp_sentence += " " + matched_synonym
            else:
                # Token has no synonyms so just append it as is.
                temp_sentence += " " + token[0]
        Globals.full_output += "\n" + temp_sentence
        # Reset local temp sentence var for next loop.
        temp_sentence = ''


def adjust_sentences(should_raise):
    print("Changing Sentence Lengths")
    sentences = nltk.sent_tokenize(Globals.full_output)
    # Replace current output completely for testing
    Globals.full_output = ''
    new_sentence = ""
    if should_raise:  # Going to make sentences longer.
        changed_recently = False  # Keeps track if we just changed one of the last two sentences.
        for sen_index, sentence in enumerate(sentences):
            tokens = pywsd.disambiguate(sentence)
            if not changed_recently:
                # Get the punctuation of the end of the sentence (e.g. ! ? .)
                current_sentence_end = tokens[len(tokens) - 1][0]
                # If there's another sentence, and we're ending in a period, just change it.
                if sen_index < (len(sentences) - 1) and current_sentence_end == ".":
                    for tok_index, token in enumerate(tokens):
                        if tok_index != (len(tokens) - 1):  # If we're not at the end, just go as normal.
                            new_sentence += " " + token[0]
                        else:
                            new_sentence += ";"
                    changed_recently = True
            else:
                # This basically makes sure after we combined two sentences, the start of the second one starts
                # with a lowercase. (e.g. Sentence_one. Sentence_two. -> Sentence_one; sentence_two.)
                for tok_index, token in enumerate(tokens):
                    if tok_index == 0:
                        new_sentence += " " + token[0].lower()
                    else:
                        new_sentence += " " + token[0]

                Globals.full_output += "\n" + new_sentence
                new_sentence = ""
                changed_recently = False  # Change back after we pass the sentences we just modified.

    else:  # Going to make sentences shorter.
        skip_word = False  # Will keep track if we need to skip a word due to resizing.
        first_word = False  # Will keep track if we need to capitalize the first word of a sentence.
        for sentence in sentences:
            tokens = pywsd.disambiguate(sentence)
            for tok_index, token in enumerate(tokens):
                if not skip_word:
                    # If we have ";", then replace with period.
                    if token[0] == ";":
                        Globals.full_output += new_sentence + ".\n"
                        new_sentence = ""
                        first_word = True
                    # If we have "___, and", "___, or", "___, but", or "___, however", replace with period.
                    # Also checks to make sure sentence isn't like: "Is it sunny, cold, or windy?"
                    elif (tok_index + 1 < len(tokens) and token[0] == "," and (tok_index + 5) < len(tokens) and
                          (tokens[tok_index + 1][0].lower() == "and" or tokens[tok_index + 1][0].lower() == "or" or
                           tokens[tok_index + 1][0].lower() == "but" or tokens[tok_index + 1][0].lower() == "however")):
                        Globals.full_output += new_sentence + ".\n"  # End sentence early.
                        new_sentence = ""
                        skip_word = True  # Skip the "and", "or", "but", or "however".
                        first_word = True  # Starting a new sentence in the middle of an old one.
                    else:  # Comes here if there's no sentence to shorten quite yet.
                        if first_word:  # If we had cut a sentence short earlier, capitalize the start of the new one.
                            new_sentence += " " + token[0].capitalize()
                            first_word = False
                        else:
                            new_sentence += " " + token[0]
                else:
                    skip_word = False  # Change back, after we skipped.
            Globals.full_output += new_sentence + "\n"
            new_sentence = ""
