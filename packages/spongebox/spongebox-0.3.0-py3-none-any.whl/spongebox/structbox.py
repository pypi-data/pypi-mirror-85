def flatten_list(li):
    return sum(([x] if not isinstance(x, list) else flatten_list(x) for x in li), [])