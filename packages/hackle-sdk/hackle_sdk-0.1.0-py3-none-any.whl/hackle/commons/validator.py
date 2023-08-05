from six import string_types
from six import integer_types


def is_non_empty_string(input_id_key):
    if input_id_key and isinstance(input_id_key, string_types):
        return True

    return False


def is_non_zero_and_empty_int(input_id_key):
    if input_id_key and isinstance(input_id_key, integer_types) and input_id_key > 0:
        return True

    return False
