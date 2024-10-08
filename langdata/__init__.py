import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from PySide6.QtGui import QIcon

BASE_DIR = Path(__file__).parent.joinpath("resources")


def _create_icon(flag_path: Path) -> QIcon:
    return QIcon(str(flag_path))


@dataclass
class Language:
    name: str
    pt1: str
    country: str
    flag: QIcon

    def from_dict(data: dict[str, Any]) -> Self:
        return Language(
            name=data.get("name"),
            pt1=data.get("pt1"),
            country=data.get("country"),
            flag=data.get("flag"),
        )


language_data: dict[str, Language] = None
country_data: dict[str, dict[str, Any]] = None

def load_languages() -> dict[str, Language]:
    global language_data 
    if not language_data:
        flags = load_flags()

        languages_path = BASE_DIR.joinpath("languages.json")
        with open(languages_path, "r", encoding="utf-8") as file:
            languages = json.load(file)

        language_data = {}
        for language in languages:
            country = language["country"]
            language["flag"] = flags.get(country)["flag_4x3"]
            lang = Language.from_dict(language)
            language_data[language["pt1"]] = lang

    return language_data


def load_flags() -> dict[str, dict[str, Any]]:
    global country_data
    if not country_data:
        countries_path = BASE_DIR.joinpath("countries.json")
        with open(countries_path, "r", encoding="utf-8") as file:
            countries = json.load(file)

        country_data = {country["code"]: country for country in countries}
        for country in list(country_data.values()):
            flag_1x1 = _create_icon(BASE_DIR.joinpath(country["flag_1x1"]))
            flag_4x3 = _create_icon(BASE_DIR.joinpath(country["flag_4x3"]))
            country["flag_1x1"] = flag_1x1
            country["flag_4x3"] = flag_4x3

    return country_data
