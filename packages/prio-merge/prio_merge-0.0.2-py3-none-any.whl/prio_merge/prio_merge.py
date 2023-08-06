"""
Prio merge!
"""


def prio_merge(dict_a, dict_b):
    return _handle_two_dicts(dict_a, dict_b)


def _handle_two_dicts(a, b):
    for b_key, b_value in b.items():
        if b_key not in a:
            a[b_key] = b_value
        elif type(a[b_key]) == type(b_value) and isinstance(b_value, dict):
            a[b_key] = _handle_two_dicts(a[b_key], b_value)
        elif type(a[b_key]) == type(b_value) and isinstance(b_value, list):
            a[b_key] = sorted(list(set(a[b_key] + b_value)))
    return a
