import json

def return_as_xs(word_length):
    aux_string = ""

    for index in range(word_length):
        aux_string += "x"

    return aux_string

def old_words_to_new_words():
    # with open('JSON files/ordered_old_words_to_new_words.js','r+') as json_file:
    #     # First we load existing data into a dict.
    #     old_words_to_new_words = json.load(json_file)

    old_words_to_new_words = {
        "a": "a",
        "o": "e",
        "um": "i",
        "uma": "u"
    }

    print(
    """-----------------------------
    type:
    exit - to exit
    some word or sentence in portuguese - to translate it
    -----------------------------"""
    )

    text_input = input()

    while (text_input != "exit"):

        input_as_list = text_input.split(" ")
        
        new_word_or_sentence = ""

        for old_word in input_as_list:
            if(old_word in old_words_to_new_words):
                new_word_or_sentence += old_word + " "

            else:
                new_word_or_sentence += return_as_xs(len(old_word)) + " "

        print(new_word_or_sentence)

        text_input = input()

print(
"""-----------------------------
type:
1 - to translate from old words to new words
2 - to translate from new words to old words
-----------------------------"""
)

initial_input = input()

if(initial_input == "1"):
    old_words_to_new_words()

elif(initial_input == "2"):
    print("aa")

else:
    print("typo")