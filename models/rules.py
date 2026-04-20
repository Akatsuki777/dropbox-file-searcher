from dataclasses import dataclass

@dataclass
class Condition:
    field: str
    op: str
    value: object

@dataclass
class Rule:
    name: str
    all: list[Condition]