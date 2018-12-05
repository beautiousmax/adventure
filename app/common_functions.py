import random
import re

from termcolor import colored

from data.text import numbers, names


def formatted_items(item_list):
    formatted = []
    for item in item_list:
        if item.quantity > 1:
            formatted.append(f"{numbers[item.quantity]} {colored(item.plural, 'yellow')}")
        else:
            formatted.append(colored(item.name, 'yellow'))
    return formatted


def comma_separated(words):
    if len(words) >= 3:
        commas = ", ".join(words[0:-1])
        return f"{commas} and {words[-1]}"
    elif len(words) == 2:
        return f"{words[0]} and {words[1]}"
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


def remove_little_words(phrase):
    if type(phrase) != list:
        phrase = phrase.split(" ")
    phrase_words = []
    for word in phrase:
        if word not in ('a', 'an', 'the', 'that', 'this'):
            phrase_words.append(word)
    return " ".join(phrase_words)


def odds(x):
    return True if random.randint(1, x) == 1 else False


def are_is(noun_list):
    quantity = len(noun_list)
    if quantity == 1:
        quantity = noun_list[0].quantity
    return f"{'are' if quantity > 1 else 'is'} {comma_separated(formatted_items(noun_list))}"


def capitalize_first(string):
    if not string[0].isalpha() and not string[0].isdigit():
        return f"{string[0:3]}{string[4].upper()}{string[5:]}"


def find_specifics(words, list_of_objects):
    specifics = []
    if list_of_objects is None:
        return specifics
    if words in ('all', 'everyone', 'everything') or words is None or words == '':
        return list_of_objects
    for word in remove_little_words(words).split(' '):
        for o in list_of_objects:
            for individual_word in remove_little_words(o.name).lower().split(' '):
                if word.lower() in individual_word.lower() or word.lower() == individual_word.lower() or \
                        word.lower() == o.plural.lower() or word.lower() in o.plural:
                    specifics.append(o)
                    break
    return specifics


def the_name(n):
    for name in names:
        if name in n:
            return name
    else:
        return f"the {remove_little_words(n)}"
