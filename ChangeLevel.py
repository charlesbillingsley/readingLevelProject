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
    """
    Changes the reading level to a new level going up
    or down based on the global variables.
    """
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
    """
    Contracts or elongates the contractions in the text.
    :param should_raise: whether or not the reading level should be raised
    :return: net result in words added/removed
    """
    print("Adjusting Contractions")
    total_contractions = 0
    Globals.full_output = Globals.full_input
    if should_raise:
        # Raising difficulty -> shrink contractions
        for phrase in Contractions.expanded_as_key:
            # Count lowercase version of phrase + phrase with capitalized first letter
            total_contractions += Globals.full_output.count(phrase) + \
                                  Globals.full_output.count(
                                      phrase[0].upper() + phrase[1:])
            # Replace lowercase phrase
            Globals.full_output = Globals.full_output.replace(phrase,
                                                              Contractions.expanded_as_key[
                                                                  phrase])
            # Replace phrase with first letter capitalized (ex. Can not -> Can't)
            Globals.full_output = Globals.full_output.replace(
                phrase[0].upper() +
                phrase[1:],
                Contractions.expanded_as_key[phrase][0].upper() +
                Contractions.expanded_as_key[phrase][1:])
    else:
        # Lowering difficulty -> expand contractions
        for contraction in Contractions.contractions_as_key:
            # Count lowercase version of contraction + contractions with capitalized first letter
            total_contractions += Globals.full_output.count(contraction) + \
                                  Globals.full_output.count(
                                      contraction[0].upper() + contraction[1:])
            # Replace lowercase contraction
            Globals.full_output = Globals.full_output.replace(contraction,
                                                              Contractions.contractions_as_key[
                                                                  contraction])
            # Replace contractions with first letter capitalized (ex. Can't -> Can not)
            Globals.full_output = Globals.full_output.replace(
                contraction[0].upper() +
                contraction[1:],
                Contractions.contractions_as_key[contraction][0].upper() +
                Contractions.contractions_as_key[contraction][1:])
    # Return net result in words added/removed
    return (-1 * total_contractions) if should_raise else total_contractions


def adjust_syllables(should_raise):
    """
    Finds synonyms for each word with more or less syllables
    depending on if the score is being raised or lowered.

    :param should_raise: should_raise: whether or not
                         the reading level should be raised
    """
    print("Finding Synonyms")
    # See about tokenizing all words to keep context (ie love as verb vs adverb)
    # Either disambiguate words automatically (as below) or use http://www.nltk.org/howto/wordnet.html
    temp_sentence = ''
    sentences = nltk.sent_tokenize(Globals.full_output)
    # Replace current output completely for testing
    Globals.full_output = ''
    for sentence in sentences:
        tokens = pywsd.disambiguate(sentence)
        for token in tokens:
            # Token[0] = word, Token[1] = synset
            synset = token[1]
            if synset:
                # If token has synonyms
                matched_synonym = max(synset.lemma_names(),
                                      key=main.get_syllables) if should_raise else min(
                    synset.lemma_names(), key=main.get_syllables)
                temp_sentence += " " + matched_synonym
            else:
                temp_sentence += " " + token[0]
        Globals.full_output += "\n" + temp_sentence
        temp_sentence = ''


def adjust_sentences(should_raise):
    """
    Adjusts the length of sentences based on if the
    score is being raised or lowered.
    :param should_raise: should_raise: whether or not
                         the reading level should be raised
    """
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
                if sen_index < (
                            len(
                                sentences) - 1) and current_sentence_end == ".":
                    for tok_index, token in enumerate(tokens):
                        if tok_index != (len(
                                tokens) - 1):  # If we're not at the end, just go as normal.
                            new_sentence += " " + token[0]
                        else:
                            new_sentence += ";"
                    changed_recently = True
            else:
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
                    elif (tok_index + 1 < len(tokens) and token[0] == "," and (
                                tok_index + 5) < len(tokens) and
                              (tokens[tok_index + 1][0].lower() == "and" or
                                       tokens[tok_index + 1][
                                           0].lower() == "or" or
                                       tokens[tok_index + 1][
                                           0].lower() == "but" or
                                       tokens[tok_index + 1][
                                           0].lower() == "however")):
                        Globals.full_output += new_sentence + ".\n"
                        new_sentence = ""
                        skip_word = True  # Skip the "and", "or", "but", or "however".
                        first_word = True
                    else:
                        if first_word:
                            new_sentence += " " + token[0].capitalize()
                            first_word = False
                        else:
                            new_sentence += " " + token[0]
                else:
                    skip_word = False  # Change back, after we skipped.
            Globals.full_output += new_sentence + "\n"
            new_sentence = ""
