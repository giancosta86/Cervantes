from info.gianlucacosta.eos.core.db.sqlite import ConnectionLender
from info.gianlucacosta.eos.core.db.sqlite.serializer import BufferedDbSerializer, DbRow

from ..terms import (
    Adjective,
    Adverb,
    Article,
    Conjunction,
    Interjection,
    Noun,
    Preposition,
    Pronoun,
    Verb,
    VerbForm,
)


def create_spanish_serializer(
    connection_lender: ConnectionLender,
) -> BufferedDbSerializer:
    serializer = BufferedDbSerializer(connection_lender)

    @serializer.register(
        """
        INSERT OR IGNORE INTO prepositions
        (entry, pronunciation)
        VALUES
        (?, ?)
        """
    )
    def serialize_preposition(preposition: Preposition) -> DbRow:
        return (preposition.entry, preposition.pronunciation)

    @serializer.register(
        """
        INSERT OR IGNORE INTO interjections
        (entry, pronunciation)
        VALUES
        (?, ?)
        """
    )
    def serialize_interjection(interjection: Interjection) -> DbRow:
        return (interjection.entry, interjection.pronunciation)

    @serializer.register(
        """
            INSERT OR IGNORE INTO conjunctions
            (entry, pronunciation)
            VALUES
            (?, ?)
            """
    )
    def serialize_conjunction(conjunction: Conjunction) -> DbRow:
        return (conjunction.entry, conjunction.pronunciation)

    @serializer.register(
        """
            INSERT OR IGNORE INTO adverbs
            (entry, pronunciation, kind)
            VALUES
            (?, ?, ?)
            """
    )
    def serializer_adverb(adverb: Adverb) -> DbRow:
        return (adverb.entry, adverb.pronunciation, adverb.kind)

    @serializer.register(
        """
            INSERT OR IGNORE INTO verbs
            (entry, pronunciation, kind)
            VALUES
            (?, ?, ?)
            """,
        max_buffer_len=4000,
    )
    def serialize_verb(verb: Verb) -> DbRow:
        return (verb.entry, verb.pronunciation, verb.kind)

    @serializer.register(
        """
        INSERT OR IGNORE INTO pronouns
        (entry, pronunciation, kind)
        VALUES
        (?, ?, ?)
        """
    )
    def serialize_pronoun(pronoun: Pronoun) -> DbRow:
        return (pronoun.entry, pronoun.pronunciation, pronoun.kind)

    @serializer.register(
        """
        INSERT OR IGNORE INTO articles
        (entry, pronunciation, kind)
        VALUES
        (?, ?, ?)
        """
    )
    def serialize_article(article: Article) -> DbRow:
        return (article.entry, article.pronunciation, article.kind)

    @serializer.register(
        """
            INSERT OR IGNORE INTO adjectives
            (entry, pronunciation, reference_entry)
            VALUES
            (?, ?, ?)
            """
    )
    def serialize_adjective(adjective: Adjective) -> DbRow:
        return (
            adjective.entry,
            adjective.pronunciation,
            adjective.reference_entry,
        )

    @serializer.register(
        """
            INSERT OR IGNORE INTO nouns
            (entry, pronunciation, gender, number_trait, reference_entry)
            VALUES
            (?, ?, ?, ?, ?)
            """,
        max_buffer_len=5000,
    )
    def serialize_noun(noun: Noun) -> DbRow:
        return (
            noun.entry,
            noun.pronunciation,
            noun.gender,
            noun.number_trait,
            noun.reference_entry,
        )

    @serializer.register(
        """
        INSERT OR IGNORE INTO verb_forms
        (entry, pronunciation, infinitive, mode, tense, person)
        VALUES
        (?, ?, ?, ?, ?, ?)
        """,
        max_buffer_len=15000,
    )
    def serialize_verb_form(verb_form: VerbForm) -> DbRow:
        return (
            verb_form.entry,
            verb_form.pronunciation,
            verb_form.infinitive,
            verb_form.mode,
            verb_form.tense,
            verb_form.person,
        )

    return serializer
