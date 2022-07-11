import json

# save words and their weights on JSON file
def order_old_words_and_weights():
    with open('JSON files/old_words_and_weights.js','r+') as json_file:
        # First we load existing data into a dict.
        file_data = json.load(json_file)

        # order the dict
        aux_list = []

        for old_word in file_data:
            aux_list.append([file_data[old_word], old_word])

        aux_list.sort(reverse=True)

        for index, value in enumerate(aux_list):
            aux_list[index] = [aux_list[index][1], aux_list[index][0]]

        aux_dict = dict(aux_list)

        # Sets file's current position at offset.
        json_file.seek(0)

        # convert back to json.
        json.dump(aux_dict, json_file, indent = 4)


order_old_words_and_weights()