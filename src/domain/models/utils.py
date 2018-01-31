import re


# Source: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def camel_case_to_underscores(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def dict_keys_camel_case_to_underscores(value):
    """Recursively converts all keys of a dictionary to be underscore-delimited"""
    if not isinstance(value, dict):
        return value
    result = dict()
    for k, v in value.items():
        underscored_key = camel_case_to_underscores(k)
        new_value = dict_keys_camel_case_to_underscores(v)
        result[underscored_key] = new_value
    return result
