from decouple import config as env


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def is_valid_api_key(api_key: str) -> bool:
    key_length = len(env("API_KEY"))
    return api_key[:key_length] == env("API_KEY")


def construct_query(query_base, conditions):
    query = query_base
    if conditions:
        query += " WHERE "
        query += " AND ".join(conditions)
    query += ";"
    return query


def get_username(api_key: str) -> str:
    key_length = len(env("API_KEY"))
    return api_key[key_length:]
