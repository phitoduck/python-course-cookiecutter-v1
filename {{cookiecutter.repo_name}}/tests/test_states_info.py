from {{cookiecutter.package_import_name}}.states_info import is_city_capitol_of_state, slow_add
import pytest


@pytest.mark.parametrize(
    argnames=("city_name", "state", "is_capitol"),
    argvalues=[
        ("Montgomery", "Alabama", True),
        ("Oklahoma City", "Oklahoma", True),
        ("Salem", "Oregon", True),
        ("Salt Lake City", "Alabama", False),
    ],
)
def test__is_city_capitol_of_state(city_name: str, state: str, is_capitol: bool):
    assert is_city_capitol_of_state(city_name=city_name, state=state) == is_capitol

@pytest.mark.slow
def test__slow_add():
    assert slow_add(1, 2) == 3
