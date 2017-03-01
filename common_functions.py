from text import *
import re


def formatted_items(item_list):
    formatted = []
    for item in item_list:
        if item.quantity > 1:
            formatted.append(
                "{} {}".format(numbers[item.quantity], item.plural))
        else:
            formatted.append(item.name)
    return formatted


def comma_separated(words):
    if len(words) >= 3:
        commas = ", ".join(words[0:-1])
        return "{} and {}".format(commas, words[-1])
    elif len(words) == 2:
        return "{} and {}".format(words[0], words[1])
    else:
        return words[0]


def add_dicts_together(dict1, dict2):
    dict3 = dict(dict1)
    dict3.update(dict2)
    return dict3


def parse_inventory_action(words):
    words = words.lower().strip()
    words_s = words.split(" ")

    if words == "everything" or words == "all":
        quantity = "all"
        item_text = None

    elif re.match(r"\d* .*", words):
        quantity = int(words_s[0])
        item_text = " ".join(words_s[1:])

    elif words_s[0] in ("all", "the"):
        quantity = "all"
        item_text = " ".join(words_s[1:])

    elif words_s[0] in ("a", "an", "some"):
        quantity = 1
        item_text = " ".join(words_s[1:])

    elif words_s[0] in numbers.values():
        quantity = [k for k, v in numbers.items() if v == words_s[0]][0]
        item_text = " ".join(words_s[1:])

    elif words == "":
        item_text = None
        quantity = None

    else:
        quantity = "all"
        item_text = " ".join(words_s[0:])

    return quantity, item_text
