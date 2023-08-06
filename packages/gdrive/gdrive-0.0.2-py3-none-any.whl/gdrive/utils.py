from urllib.parse import urlparse, parse_qs


def query_string_to_dict(qs):
    query_parsed = urlparse(qs)
    query_dict = parse_qs(query_parsed.query)

    # unwrap values as by default arguments are parsed to lists { 'k': ['v']}
    for k, v in query_dict.items():
        if isinstance(v, list) and len(v) == 1:
            query_dict[k] = v[0]

    return query_parsed, query_dict
