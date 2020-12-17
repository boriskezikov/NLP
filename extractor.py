import string
import re

from yargy.parser import Match
from Lab2.rule import *


def extract(token, type):
    from yargy import Parser
    schema_pattern = get_schema_pattern(type)

    parser = Parser(schema_pattern['pattern'])
    jsons = map(to_json, [t for t in parser.findall(token)])
    parsed_model = dict()
    empty_model = {key: None for key in schema_pattern['schema']}
    for json in jsons:
        parsed_model = {**parsed_model, **dict(json)} if len(json) > len(parsed_model) else {**dict(json),
                                                                                             **parsed_model}
    model_json = dict({**empty_model, **parsed_model})
    for token in model_json:
        if model_json[token] is None:
            continue
        model_json[token] = "".join(
            _ for _ in model_json[token] if _ not in re.sub('[-/]', '', string.punctuation))
    return model_json


def to_json(match: Match):
    return match.fact.as_json
