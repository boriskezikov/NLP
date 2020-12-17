from yargy import or_
from yargy.predicates import *


def get_genitive():
    return gram('gent')


def get_intj_type():
    return gram('INTJ')


def is_dash():
    return eq('-')


def is_dot():
    return eq('-')


def is_whitespace():
    return eq('')


def get_abbr_gram():
    return gram("Abbr")


# allowed len generator
def len_generator():
    len_rule_list = []
    for allowed_len in range(3, 20):
        len_rule_list.append(length_eq(allowed_len))
    return len_rule_list


def get_len():
    return or_(*len_generator())


def get_adjective_gram():
    return gram('ADJF')


def get_noun_gram():
    return gram('NOUN')


def get_int_type():
    return type('INT')


def get_address_schema():
    return ['city', 'city_type', 'street', 'street_type', 'house', 'house_type', 'corpus', 'corpus_type',
            'apartment', 'apartment_type', 'building', 'building_type', 'flat', 'flat_type']


def get_person_schema():
    return ['first', 'last', 'middle']


def get_schema_pattern(type):
    from Lab2.rule import ADDRESS_RULE
    from Lab2.rule import PERSON_RULE
    if type == PERSON:
        return dict({'schema': get_person_schema(), 'pattern': PERSON_RULE})
    elif type == ADDRESS:
        return dict({'schema': get_address_schema(), 'pattern': ADDRESS_RULE})


ADDRESS = 'a'
PERSON = 'p'
