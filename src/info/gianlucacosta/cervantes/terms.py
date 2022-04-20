from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class SpanishTerm(ABC):
    entry: str
    pronunciation: Optional[str]


@dataclass(frozen=True, slots=True)
class Preposition(SpanishTerm):
    pass


@dataclass(frozen=True, slots=True)
class Conjunction(SpanishTerm):
    pass


@dataclass(frozen=True, slots=True)
class Interjection(SpanishTerm):
    pass


@dataclass(frozen=True, slots=True)
class Adverb(SpanishTerm):
    kind: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Article(SpanishTerm):
    kind: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Pronoun(SpanishTerm):
    kind: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Verb(SpanishTerm):
    kind: Optional[str] = None


@dataclass(frozen=True, slots=True)
class Adjective(SpanishTerm):
    reference_entry: Optional[str]


@dataclass(frozen=True, slots=True)
class Noun(SpanishTerm):
    gender: str
    reference_entry: Optional[str]
    number_trait: Optional[str] = None


@dataclass(frozen=True, slots=True)
class VerbForm(SpanishTerm):
    infinitive: str
    mode: str
    tense: Optional[str] = None
    person: Optional[str] = None
