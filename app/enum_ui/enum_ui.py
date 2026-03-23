from dataclasses import dataclass
from enum import Enum
from typing import TypeVar


@dataclass
class EnumView:
    label:   str
    icon:    str
    classes: str   # classes Tailwind ex: "bg-blue-100 text-blue-700"


T = TypeVar('T', bound=Enum)


class ViewRegistry:
    def __init__(self):
        self._registry: dict[type, dict[Enum, EnumView]] = {}

    def register(self, mapping: dict[Enum, EnumView]):
        enum_type = type(next(iter(mapping)))
        self._registry[enum_type] = mapping

    def get(self, value: Enum) -> EnumView:
        return self._registry[type(value)][value]


# Instance globale unique
registry = ViewRegistry()