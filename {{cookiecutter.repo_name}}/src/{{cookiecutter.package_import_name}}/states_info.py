from pathlib import Path
import json
from typing import List

THIS_DIR = Path(__file__).parent
CITIES_JSON_FPATH = THIS_DIR / "cities.json"


def is_city_capitol_of_state(city_name: str, state: str) -> bool:
    cities_json_contents = CITIES_JSON_FPATH.read_text()
    cities: List[dict] = json.loads(cities_json_contents)
    matching_cities: List[dict] = [city for city in cities if city["city"] == city_name]
    if len(matching_cities) == 0:
        return False
    matched_city = matching_cities[0]
    return matched_city["state"] == state

def slow_add(a: int, b: int) -> int:
    return a + b
