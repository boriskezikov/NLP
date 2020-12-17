from yargy import rule, and_, not_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES

from Lab2.data import *
from Lab2.constants import *

SIMPLE_CITIES = [city.lower() for city in city_test if city.find('-') == -1 and city.find(' ') == -1]
COMPLEX_CITIES = [city.lower() for city in city_test if city.find('-') != -1 or city.find(' ') != -1]

Address = fact('Address', get_address_schema())

CITY_NAME = or_(rule(dictionary(SIMPLE_CITIES)), morph_pipeline(COMPLEX_CITIES)).interpretation(Address.city)

SIMPLE = and_(true(), or_(get_noun_gram(), get_adjective_gram()))
COMPLEX = or_(rule(SIMPLE, is_dash().optional(), SIMPLE),
              rule(true(), is_dash().optional(), caseless('на'), is_dash().optional(), true()))
PERSON_RULE = or_(rule(SIMPLE), COMPLEX)
MAYBE_CITY_NAME = or_(PERSON_RULE, rule(PERSON_RULE, '-', get_int_type())).interpretation(Address.city)

CITY_WORDS = or_(rule(normalized('город')), rule(caseless('г'), is_dot().optional())).interpretation(
    Address.city_type.const('город'))

CITY = or_(rule(CITY_NAME), rule(CITY_WORDS, CITY_NAME), rule(CITY_NAME, CITY_WORDS)).interpretation(Address)

SHORT_MODIFIER_WORDS = rule(in_caseless({*ex_word}), is_dash().optional())

MODIFIER_WORDS = or_(SHORT_MODIFIER_WORDS)

LET_WORDS = or_(rule(caseless('лет')), rule(is_dash().optional(), caseless('летия')))

LET = rule(get_int_type(), LET_WORDS)

MONTH_WORDS = dictionary({*months})

DAY = and_(get_int_type(), gte(1), lte(31))
YEAR = and_(get_int_type(), gte(1), lte(2100))
YEAR_WORDS = normalized('год')
DATE = or_(rule(DAY, MONTH_WORDS), rule(get_adjective_gram(), normalized('дней')), rule(YEAR, YEAR_WORDS))

TITLE_RULE = and_(
    true(),
    not_(get_int_type()),
    not_(get_intj_type()),
    not_(length_eq(3)),
    not_(normalized('проезд')),
    not_(normalized('видный')),
    not_(normalized('крылова')),
    not_(normalized('питер'))
)

PART = and_(TITLE_RULE, or_(gram('Name'), gram('Surn')))

MAYBE_FIO = or_(rule(gram('Surn')), rule(gram('Name')), rule(TITLE_RULE, PART), rule(PART, TITLE_RULE))

POSITION_WORDS = or_(rule(dictionary(roles_test)))

MAYBE_PERSON = or_(MAYBE_FIO, rule(POSITION_WORDS, MAYBE_FIO))

IMENI_WORDS = or_(rule(caseless('им'), is_dot().optional()), rule(caseless('имени')))
IMENI = rule(IMENI_WORDS.optional(), MAYBE_PERSON)

SIMPLE = and_(or_(get_adjective_gram(), and_(get_noun_gram(), get_genitive())), TITLE_RULE)
COMPLEX = or_(rule(and_(get_adjective_gram(), TITLE_RULE), get_noun_gram()),
              rule(TITLE_RULE, is_dash().optional(), TITLE_RULE))

EXCEPTION = dictionary({'арбат', 'варварка'})
MAYBE_NAME = or_(rule(SIMPLE), rule(EXCEPTION))

MAIL_STREET = rule(get_int_type(), get_adjective_gram(), get_noun_gram())

LET_NAME = or_(MAYBE_NAME, LET, DATE, IMENI)
MODIFIER_NAME = rule(MODIFIER_WORDS, get_noun_gram())
PERSON_RULE = or_(LET_NAME, MODIFIER_NAME, MAIL_STREET)
ADDR_NAME = PERSON_RULE

SPB_SHORT = rule(normalized('питер')).interpretation(Address.city.const('санкт-петербург'))
SBP_NAME = LET_NAME.interpretation(Address.street)
SPB_STREET = rule(SPB_SHORT, SBP_NAME).interpretation(Address)

STREET_NAME = ADDR_NAME.interpretation(Address.street)
STREET_WORDS = or_(rule(normalized('улица')), rule(normalized('улица'), normalized('значит')),
                   rule(caseless('ул'), is_dot().optional())
                   ).interpretation(Address.street_type.const('улица'))
STREET = or_(rule(STREET_WORDS, STREET_NAME), rule(STREET_NAME, STREET_WORDS)).interpretation(Address)

BOULEVARD_WORDS = or_(rule(caseless('б'), '-', caseless('р')),
                      rule(caseless('бул'), is_dot().optional())).interpretation(Address.street_type.const('бульвар'))
BOULEVARD_NAME = ADDR_NAME.interpretation(Address.street)
BOULEVARD = or_(rule(BOULEVARD_WORDS, BOULEVARD_NAME), rule(BOULEVARD_NAME, BOULEVARD_WORDS)).interpretation(Address)

HIGHWAY_WORDS = or_(rule(caseless('ш'), is_dot()), rule(normalized('шоссе'))).interpretation(
    Address.street_type.const('шоссе'))
HIGHWAY_NAME = ADDR_NAME.interpretation(Address.street)
HIGHWAY = or_(rule(HIGHWAY_WORDS, HIGHWAY_NAME), rule(HIGHWAY_NAME, HIGHWAY_WORDS)).interpretation(Address)

TRACT_WORDS = or_(rule(caseless('тр'), is_dot()), rule(normalized('тракт'))).interpretation(
    Address.street_type.const('тракт'))
TRACT_NAME = ADDR_NAME.interpretation(Address.street)
TRACT = or_(rule(TRACT_WORDS, TRACT_NAME), rule(TRACT_NAME, TRACT_WORDS)).interpretation(Address)

GAI_WORDS = rule(normalized('гай'))
GAI_NAME = ADDR_NAME
GAI = or_(rule(GAI_WORDS, GAI_NAME), rule(GAI_NAME, GAI_WORDS)).interpretation(Address.street)

VAL_WORDS = rule(normalized('вал'))
VAL_NAME = ADDR_NAME
VAL = or_(rule(VAL_WORDS, VAL_NAME), rule(VAL_NAME, VAL_WORDS)).interpretation(Address.street)

ALLEY_WORDS = rule(normalized('аллеи')).interpretation(Address.street_type.const('аллеи'))
ALLEY_NAME = ADDR_NAME.interpretation(Address.street)
ALLEY = rule(ALLEY_NAME, ALLEY_WORDS).interpretation(Address)

AVENUE_WORDS = or_(rule(in_caseless({'пр', 'просп'}), is_dot().optional()),
                   rule(caseless('пр'), '-', in_caseless({'кт', 'т'}), is_dot().optional()),
                   rule(normalized('проспект'))).interpretation(Address.street_type.const('проспект'))
AVENUE_NAME = ADDR_NAME.interpretation(Address.street)
AVENUE = or_(rule(AVENUE_WORDS, AVENUE_NAME), rule(AVENUE_NAME, AVENUE_WORDS)).interpretation(Address)

DISTRICT_WORDS = or_(rule(in_caseless({'мк', 'мкр'}), is_dot().optional()),
                     rule(caseless('мк'), '-', in_caseless({'рн', 'н'}), is_dot().optional()),
                     ).interpretation(Address.street_type.const('микрорайон'))
DISTRICT_NAME = ADDR_NAME.interpretation(Address.street)
DISTRICT = or_(rule(DISTRICT_WORDS, DISTRICT_NAME), rule(DISTRICT_NAME, DISTRICT_WORDS)).interpretation(Address)

DRIVEWAY_WORDS = or_(rule(normalized('проезд')), rule(caseless('пр'), is_dot().optional())).interpretation(
    Address.street_type.const('проезд'))
DRIVEWAY_NAME = ADDR_NAME.interpretation(Address.street)
DRIVEWAY = or_(rule(DRIVEWAY_NAME, DRIVEWAY_WORDS), rule(DRIVEWAY_WORDS, DRIVEWAY_NAME)).interpretation(Address)

ALLEYWAY_WORDS = or_(rule(caseless('п'), is_dot()), rule(caseless('пер'), is_dot().optional()), ).interpretation(
    Address.street_type.const('переулок'))

ALLEYWAY_NAME = ADDR_NAME.interpretation(Address.street)
ALLEYWAY = or_(rule(ALLEYWAY_WORDS, ALLEYWAY_NAME), rule(ALLEYWAY_NAME, ALLEYWAY_WORDS)).interpretation(Address)

SQUARE_WORDS = or_(rule(caseless('пл'), is_dot().optional())).interpretation(Address.street_type.const('площадь'))
SQUARE_NAME = ADDR_NAME.interpretation(Address.street)
SQUARE = or_(rule(SQUARE_WORDS, SQUARE_NAME), rule(SQUARE_NAME, SQUARE_WORDS)).interpretation(Address)

EMBANKMENT_WORDS = or_(rule(caseless('наб'), is_dot().optional())).interpretation(
    Address.street_type.const('набережная'))
EMBANKMENT_NAME = ADDR_NAME.interpretation(Address.street)
EMBANKMENT = or_(rule(EMBANKMENT_WORDS, EMBANKMENT_NAME), rule(EMBANKMENT_NAME, EMBANKMENT_WORDS)).interpretation(
    Address)

LETTER = in_(ru)
QUOTE = in_(QUOTES)
LETTER = or_(rule(LETTER), rule(QUOTE, LETTER, QUOTE))
SEP = in_(r' /\-')
VALUE = or_(rule(get_int_type(), SEP, LETTER), rule(get_int_type(), LETTER),
            rule(get_int_type(), is_whitespace(), LETTER), rule(get_int_type()),
            rule(get_int_type(), SEP, get_int_type()))
ADDR_VALUE = rule(eq('№').optional(), VALUE)

HOUSE_WORDS = or_(rule(normalized('номер')), rule(normalized('дом')), rule(caseless('д'), is_dot())).interpretation(
    Address.house_type.const('дом'))
HOUSE_VALUE = ADDR_VALUE.interpretation(Address.house)
HOUSE = rule(HOUSE_WORDS, HOUSE_VALUE).interpretation(Address)

APARTMENT_WORDS = or_(rule(in_caseless('кв'), is_dot().optional()), rule(normalized('квартира'))).interpretation(
    Address.corpus_type.const('корпус'))
APARTMENT_VALUE = ADDR_VALUE.interpretation(Address.apartment)

APARTMENT = or_(rule(APARTMENT_WORDS, APARTMENT_VALUE), rule(APARTMENT_VALUE, APARTMENT_WORDS)).interpretation(Address)

corpus_words_const = {'к', 'корп', 'кор', 'корпус'}
CORPUS_WORDS = or_(rule(in_caseless(corpus_words_const), is_dot().optional())).interpretation(
    Address.corpus_type.const('корпус'))
CORPUS_VALUE = ADDR_VALUE.interpretation(Address.corpus)
CORPUS = rule(CORPUS_WORDS, CORPUS_VALUE).interpretation(Address)

building_words_const = {'ст', 'строение'}
BUILDING_WORDS = or_(
    rule(in_caseless(building_words_const), is_dot().optional())).interpretation(
    Address.building_type.const('строение'))
BUILDING_VALUE = ADDR_VALUE.interpretation(Address.building)
BUILDING = rule(BUILDING_WORDS, BUILDING_VALUE).interpretation(Address)

STREET_HOUSE_CORPUS = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE,
    CORPUS_WORDS,
    CORPUS_VALUE
).interpretation(Address)

HOUSE_CORPUS = rule(HOUSE_VALUE, CORPUS_WORDS, CORPUS_VALUE).interpretation(Address)

HOUSE_BUILDING = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE,
    BUILDING_WORDS,
    BUILDING_VALUE
).interpretation(Address)

HOUSE_STREET = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE
).interpretation(Address)

VALUE_HOUSE = rule(get_int_type()).interpretation(Address.house)

NUMBER_HOUSE = rule(rule(normalized('номер')), VALUE_HOUSE).interpretation(Address)

TRIPLE_HOUSE = rule(rule(normalized('дом')), VALUE_HOUSE).interpretation(Address)

DOM_APARTMENT = rule(HOUSE_VALUE, APARTMENT_VALUE).interpretation(Address)

ADDRESS_RULE = or_(
    SPB_STREET, CITY, NUMBER_HOUSE, HOUSE_CORPUS, HOUSE_BUILDING, TRIPLE_HOUSE,
    HOUSE_STREET, DOM_APARTMENT, STREET, DRIVEWAY, ALLEYWAY, SQUARE, HIGHWAY, TRACT, EMBANKMENT, VAL, GAI, ALLEY, HOUSE,
    STREET_HOUSE_CORPUS, HOUSE_BUILDING, BOULEVARD, DISTRICT, CORPUS, APARTMENT, BUILDING
).interpretation(Address)

Name = fact('Name', name)
name = and_(gram('Name'), not_(get_abbr_gram()), get_len())
patronymic = and_(gram('Patr'), not_(get_abbr_gram()), get_len())
surname = and_(gram('Surn'), get_len())

FIRST = name.interpretation(Name.first)
FIRST_ABBR = and_(get_abbr_gram(), true()).interpretation(Name.first)
LAST = surname.interpretation(Name.last)
MAYBE_LAST = and_(true(), not_(get_abbr_gram()), get_len()).interpretation(Name.last)
MIDDLE = patronymic.interpretation(Name.middle)
MIDDLE_SHORT = and_(get_abbr_gram(), true()).interpretation(Name.middle)

FIRST_LAST = rule(FIRST, MAYBE_LAST)
LAST_FIRST = rule(MAYBE_LAST, FIRST)
LAST_ABBR_FIRST = rule(MAYBE_LAST, FIRST_ABBR, is_dot())
LAST_ABBR_FIRST_MIDDLE = rule(MAYBE_LAST, FIRST_ABBR, is_dot(), MIDDLE_SHORT, is_dot())

FIRST_MIDDLE = rule(FIRST, MIDDLE)
MIDDLE_FIRST = rule(MIDDLE, FIRST)
FIRST_MIDDLE_LAST = rule(FIRST, MIDDLE, LAST)
LAST_FIRST_MIDDLE = rule(LAST, FIRST, MIDDLE)

SHORT_FIRST_MIDDLE_LAST = rule(FIRST_ABBR, is_dot(), MIDDLE_SHORT, is_dot(), MAYBE_LAST)
SHORT_FIRST_LAST = rule(FIRST_ABBR, is_dot(), MAYBE_LAST)

PERSON_RULE = or_(LAST_FIRST_MIDDLE, FIRST_MIDDLE_LAST, FIRST_MIDDLE, FIRST_LAST, LAST_FIRST, SHORT_FIRST_LAST,
                  LAST_ABBR_FIRST, SHORT_FIRST_MIDDLE_LAST, LAST_ABBR_FIRST_MIDDLE, MIDDLE_FIRST).interpretation(Name)
