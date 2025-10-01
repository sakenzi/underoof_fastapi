from typing import Tuple
import re


def parse_address_query(query: str) -> Tuple[str, str]:
    query = query.lower().strip()
    query = re.sub(r'^(ул\.?|улица|д\.?|дом)\s*', '', query)
    query = re.sub(r'[,\s]+', ' ', query).strip()

    number_watch = re.search(r'\b(\d+[a-zA-Z]?(/\d+)?)\b', query)
    if number_watch:
        number = number_watch.group(0)
        street_name = query.replace(number, '').strip()
        return street_name, number
    else:
        return query, ""