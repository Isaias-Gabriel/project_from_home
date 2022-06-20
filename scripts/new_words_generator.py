# -*- coding: utf-8 -*-

import json

# g = sound of g in 'gostar';   q = sound of q in 'querer'
# h = sound of rr in 'carro';   x = sound of x in 'xadrez'
# s = sound of ng in 'king' or the sound after the last a in 'manhã'
letters = [
    "a", "b", "c", "d", "e", "f", "g", "i",
    "j", "l", "m", "n", "o", "p", "q", "r",
    "h", "s", "t", "u", "v", "x", "z"
]

new_words_dictionary = {}
new_words_list = []
word_index = 1

#returns true or false
#if true, then word + letter do not form a triple sequence of the variable letter
def do_not_form_triple_sequence(word, letter):
    return not word[-2:] == letter + letter

# create_words receive a list with words with a number n of characters
# and create new words with a number n + 1 of characters
# by adding the letters from the list letters
def create_words(
    word_index, words_with_n_characters, word_number_of_characters, maximum_number_of_characters
):
    if(word_number_of_characters == (maximum_number_of_characters + 1)):
        return True
    else:
        words_with_n_plus_one_characters = []

        for word in words_with_n_characters:
            for letter in letters:
                # the if checks if the word will have a triple sequence
                # of the same letter, which is not allowed in a new word
                if(do_not_form_triple_sequence(word, letter)):
                    new_word = word + letter

                    new_words_dictionary[word_index] = new_word
                    words_with_n_plus_one_characters.append(new_word)

                    word_index += 1

                    del new_word

        create_words(
            word_index, words_with_n_plus_one_characters,
            word_number_of_characters + 1, maximum_number_of_characters
        )

# [""] to prevent the second for in create_words()
# from not running

create_words(word_index, [""], 1, 5)

#save the data from the dictionary in a JSON file
with open('JSON files/indexes_and_new_words.js', 'w') as fp:
    json.dump(new_words_dictionary, fp, indent=4)
