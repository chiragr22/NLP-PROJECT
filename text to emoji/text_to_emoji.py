import json
import string
import re
import copy
import random

# To convert json data to dictionary
def load_emojis_json(emojis_file):
    with open(emojis_file) as f:
        emojis_dict = json.load(f)
    return emojis_dict

def text_to_emoji(emojis_dict, text):
    # text cleaning
    words_set = re.findall(r"[\w']+|[!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ]", text)
    temp_words_set = words_set
    words_set = [x.lower() for x in words_set]
    result_text = []
    possible_emojis = {}

    for index, each_word in enumerate(words_set):

        if each_word in string.punctuation:
            result_text.append(temp_words_set[index])

        elif each_word in emojis_dict['keys']:
            emoji_match = [each_key for each_key in emojis_dict['keys'] if each_word == each_key][0]

            if each_word not in possible_emojis:
                possible_emojis[each_word] = emojis_dict[emoji_match]['char']

            # Store the emoji in the result
            result_text.append(possible_emojis[each_word])
 
        # remove plurals
        elif each_word[:-1] in emojis_dict:
            emoji_match = [each_key for each_key in emojis_dict if each_word[:-1] == each_key][0]

            if each_word not in possible_emojis:
                possible_emojis[each_word] = emojis_dict[emoji_match]['char']

            result_text.append(possible_emojis[each_word])

        # keyword search
        else:
            temp_emojis_dict = copy.deepcopy(emojis_dict)

            del temp_emojis_dict['keys']

            new_emojis_dict = {}

            flag_new_sing = 0

            flag_new_plur = 0

            for each_key, each_val in temp_emojis_dict.items():
                if (each_word in each_val['keywords']):

                    new_emojis_dict[each_key] = each_val

                    flag_new_sing = 1

            # check fo plural in keywords
            for each_key, each_val in temp_emojis_dict.items():

                mod_each_val = [each + 's' for each in each_val['keywords']]

                if (each_word in mod_each_val):
                    new_emojis_dict[each_key] = each_val
                    flag_new_plur = 1 

            if flag_new_sing == 0 and flag_new_plur == 0:
                result_text.append(temp_words_set[index])
                continue

            if flag_new_sing == 1 or flag_new_plur == 1:
                if each_word not in possible_emojis:
                    possible_emojis[each_word] = [each_val['char'] for each_val in list(new_emojis_dict.values())]
                result_text.append(random.choice(possible_emojis[each_word]))

    # Return the resultant statement
    return result_text, possible_emojis, words_set