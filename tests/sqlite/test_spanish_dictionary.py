from contextlib import closing
from functools import wraps

from info.gianlucacosta.eos.core.db.sqlite import create_memory_db
from info.gianlucacosta.eos.core.functional import Producer
from info.gianlucacosta.wikiprism.dictionary import DictionaryView

from info.gianlucacosta.cervantes.sqlite.dictionary import SpanishSqliteDictionary
from info.gianlucacosta.cervantes.sqlite.schema import get_table_name_for_term
from info.gianlucacosta.cervantes.terms import (
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


def sqlite_dictionary_test():
    def decorator(test_function: Producer[SpanishTerm]):
        @wraps(test_function)
        def wrapper():
            with SpanishSqliteDictionary(create_memory_db()) as dictionary:
                dictionary.create_schema()

                term = test_function()

                dictionary.add_term(term)
                dictionary.flush()

                with closing(dictionary.connection.cursor()) as cursor:
                    table_name = get_table_name_for_term(term)
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table_name} WHERE entry = ?",
                        [term.entry],
                    )
                    db_result = cursor.fetchone()
                    assert db_result == (1,)

        return wrapper

    return decorator


@sqlite_dictionary_test()
def test_storing_adverb():
    return Adverb(
        entry="Test adverb",
        pronunciation="X",
        kind="AdverbKind",
    )


@sqlite_dictionary_test()
def test_storing_interjection():
    return Interjection(entry="Test interjection", pronunciation="X")


@sqlite_dictionary_test()
def test_storing_conjunction():
    return Conjunction(entry="Test conjunction", pronunciation="X")


@sqlite_dictionary_test()
def test_storing_preposition():
    return Preposition(entry="Test preposition", pronunciation="X")


@sqlite_dictionary_test()
def test_storing_article():
    return Article(
        entry="Test article",
        pronunciation="X",
        kind="ArticleKind",
    )


@sqlite_dictionary_test()
def test_storing_adjective():
    return Adjective(entry="Test adjective", pronunciation="X", reference_entry="Z")


@sqlite_dictionary_test()
def test_storing_pronoun():
    return Pronoun(entry="Test pronoun", pronunciation="X", kind="Z")


@sqlite_dictionary_test()
def test_storing_noun():
    return Noun(
        entry="Test noun",
        pronunciation="X",
        gender="m",
        reference_entry="Z",
        number_trait="p",
    )


@sqlite_dictionary_test()
def test_storing_verbs():
    return Verb(entry="Test verb", pronunciation="X", kind="Z")


@sqlite_dictionary_test()
def test_storing_personal_verb_form():
    return VerbForm(
        entry="the entry",
        pronunciation="the pronunciation",
        infinitive="the infinitive",
        mode="the mode",
        tense="the tense",
        person="the person",
    )


@sqlite_dictionary_test()
def test_storing_impersonal_verb_form():
    return VerbForm(
        entry="the entry",
        pronunciation="the pronunciation",
        infinitive="the infinitive",
        mode="the mode",
        tense=None,
        person=None,
    )


def test_query_execution_after_flush():
    with SpanishSqliteDictionary(create_memory_db()) as dictionary:
        dictionary.create_schema()

        dictionary.add_term(Preposition(entry="sobre", pronunciation=None))
        dictionary.flush()

        query_result = dictionary.execute_command("SELECT COUNT(*) FROM prepositions")

        assert query_result == DictionaryView(headers=["COUNT(*)"], rows=[(1,)])
