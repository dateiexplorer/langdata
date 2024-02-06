import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from PySide6.QtGui import QIcon

base_dir = Path(__file__).parent.joinpath("resources")


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


def load_languages() -> dict[str, Language]:
    flags = _load_flags()

    languages_path = base_dir.joinpath("languages.json")
    with open(languages_path, "r", encoding="utf-8") as file:
        languages = json.load(file)

    language_dict = {}
    for language in languages:
        country = language["country"]
        language["flag"] = flags.get(country)["flag_4x3"]
        lang = Language.from_dict(language)
        language_dict[language["pt1"]] = lang

    return language_dict


def _load_flags() -> dict[str, dict[str, Any]]:
    countries_path = base_dir.joinpath("countries.json")
    with open(countries_path, "r", encoding="utf-8") as file:
        countries = json.load(file)

    countries = {country["code"]: country for country in countries}
    for country in list(countries.values()):
        flag_1x1 = _create_icon(base_dir.joinpath(country["flag_1x1"]))
        flag_4x3 = _create_icon(base_dir.joinpath(country["flag_4x3"]))
        country["flag_1x1"] = flag_1x1
        country["flag_4x3"] = flag_4x3

    return countries
