from contextlib import closing
from sqlite3 import Connection

from ..terms import (
    Adjective,
    Adverb,
    Article,
    Conjunction,
    Interjection,
    Noun,
    Preposition,
    Pronoun,
    SpanishTerm,
    Verb,
    VerbForm,
)

SCHEMA_SCRIPT = """

CREATE TABLE prepositions (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    PRIMARY KEY (entry)
);

CREATE TABLE interjections (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    PRIMARY KEY (entry)
);

CREATE TABLE conjunctions (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    PRIMARY KEY (entry)
);

CREATE TABLE adverbs (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    kind TEXT,
    PRIMARY KEY (entry, kind)
);

CREATE TABLE verbs (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    kind TEXT,
    PRIMARY KEY (entry, kind)
);

CREATE TABLE pronouns (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    kind TEXT,
    PRIMARY KEY (entry, kind)
);

CREATE TABLE articles (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    kind TEXT,
    PRIMARY KEY (entry, kind)
);

CREATE TABLE adjectives (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    reference_entry TEXT,
    PRIMARY KEY (entry, reference_entry)
);

CREATE TABLE nouns (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    gender TEXT NOT NULL,
    number_trait TEXT,
    reference_entry TEXT,
    PRIMARY KEY (entry, gender, reference_entry)
);

CREATE TABLE verb_forms (
    entry TEXT NOT NULL,
    pronunciation TEXT,
    infinitive TEXT NOT NULL,
    mode TEXT NOT NULL,
    tense TEXT,
    person TEXT,
    PRIMARY KEY (entry, infinitive, mode, tense, person)
);
"""


def create_spanish_schema(connection: Connection) -> None:
    with closing(connection.cursor()) as cursor:
        cursor.executescript(SCHEMA_SCRIPT)


def get_table_name_for_term(term: SpanishTerm) -> str:
    match term:
        case Verb():
            return "verbs"
        case VerbForm():
            return "verb_forms"
        case Noun():
            return "nouns"
        case Adjective():
            return "adjectives"
        case Pronoun():
            return "pronouns"
        case Adverb():
            return "adverbs"
        case Conjunction():
            return "conjunctions"
        case Preposition():
            return "prepositions"
        case Article():
            return "articles"
        case Interjection():
            return "interjections"
        case _:
            raise TypeError(f"Unexpected term type: {type(term).__name__}")
