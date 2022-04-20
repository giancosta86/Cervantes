from functools import reduce
from io import StringIO
from os.path import dirname, join
from typing import Iterable
from xml.sax.saxutils import escape

from info.gianlucacosta.eos.core.functional import Producer
from info.gianlucacosta.wikiprism.page import Page

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

expected_terms_by_page: dict[str, set[SpanishTerm]] = {}


def get_expected_terms_by_test_page() -> dict[str, set[SpanishTerm]]:
    return dict(expected_terms_by_page)


def read_page_from_file(title: str) -> Page:
    text_path = join(dirname(__file__), f"{title.replace(' ', '_')}.txt")

    with open(text_path, encoding="utf-8") as text_file:
        text = text_file.read()

        return Page(title=title, text=text)


def build_test_wiki(*page_titles: str) -> str:
    buffer = StringIO()

    buffer.write(
        """
    <mediawiki>
        <siteinfo></siteinfo>
    """
    )

    for page_title in page_titles:
        test_page = read_page_from_file(page_title)

        buffer.write("<page>")
        buffer.write(f"<title>{escape(test_page.title)}</title>")
        buffer.write("<text>")
        buffer.write(escape(test_page.text))
        buffer.write("</text>")
        buffer.write("</page>")

    buffer.write("</mediawiki>")
    return buffer.getvalue()


def get_expected_terms(*page_titles: str) -> set[SpanishTerm]:
    return reduce(
        lambda all_terms, current_set: all_terms.union(current_set),
        (expected_terms_by_page[page_title] for page_title in page_titles),
        set(),
    )


def page(title: str):
    def decorator(expected_terms_producer: Producer[Iterable[SpanishTerm]]):

        producer_result = expected_terms_producer()

        match producer_result:
            case set():
                expected_terms = producer_result

            case list() | tuple():
                expected_terms = set(producer_result)

            case _:
                expected_terms = {producer_result}

        expected_terms_by_page[title] = expected_terms

    return decorator


@page("body")
def foreign_word():
    return set()


@page("también")
def affirmation_adverb():
    return Adverb(
        entry="también",
        pronunciation="tam'bjen",
        kind="afirmación",
    )


@page("rápidamente")
def manner_adverb():
    return Adverb(
        entry="rápidamente",
        pronunciation="ˌra.pi.ða'men.te",
        kind="modo",
    )


@page("aunque")
def conjunction():
    return Conjunction(entry="aunque", pronunciation="'awŋ.ke")


@page("ah")
def interjection():
    return Interjection(entry="ah", pronunciation="a")


@page("vez")
def feminine_noun():
    return Noun(
        entry="vez",
        pronunciation="beθ",
        gender="f",
        reference_entry=None,
    )


@page("veces")
def feminine_noun_plural():
    return {
        Noun(
            entry="veces",
            pronunciation="'be.ses",
            gender="f",
            reference_entry="vez",
        ),
        VerbForm(
            entry="veces",
            pronunciation="'be.ses",
            infinitive="vezar",
            mode="subjuntivo",
            tense="presente",
            person="2s",
        ),
    }


@page("flor")
def feminine_noun_with_interjection():
    return {
        Noun(
            entry="flor",
            pronunciation="floɾ",
            gender="f",
            reference_entry=None,
        ),
        Interjection(entry="flor", pronunciation="floɾ"),
    }


@page("flores")
def feminine_noun_plural_with_verb_form():
    return {
        Noun(
            entry="flores",
            pronunciation="'flo.ɾes",
            gender="f",
            reference_entry="flor",
        ),
        VerbForm(
            entry="flores",
            pronunciation="'flo.ɾes",
            infinitive="florar",
            mode="subj",
            tense="pres",
            person="2s",
        ),
    }


@page("modo")
def masculine_noun():
    return Noun(
        entry="modo",
        pronunciation="'mo.ðo",
        gender="m",
        reference_entry=None,
    )


@page("modos")
def masculine_noun_plural():
    return Noun(
        entry="modos",
        pronunciation="'mo.ðos",
        gender="m",
        reference_entry="modo",
    )


@page("tijeras")
def plural_only_feminine_noun():
    return Noun(
        entry="tijeras",
        pronunciation="ti'xe.ɾas",
        gender="f",
        reference_entry=None,
        number_trait="p",
    )


@page("tórax")
def invariant_masculine_noun():
    return Noun(
        entry="tórax",
        pronunciation="'to.ɾaks",
        gender="m",
        reference_entry=None,
        number_trait="i",
    )


@page("éste")
def demonstrative_pronoun():
    return Pronoun(
        entry="éste",
        pronunciation="'es.te",
        kind="demostrativo",
    )


@page("ésta")
def demonstrative_pronoun_form():
    return Pronoun(
        entry="ésta",
        pronunciation="'es.ta",
        kind="demostrativo",
    )


@page("yo")
def personal_pronoun_and_noun():
    return {
        Pronoun(
            entry="yo",
            pronunciation="ʝo",
            kind="personal",
        ),
        Noun(
            entry="yo",
            pronunciation="ʝo",
            gender="m",
            reference_entry=None,
        ),
    }


@page("tuyo")
def possessive_pronoun_with_masculine_noun():
    return {
        Pronoun(
            entry="tuyo",
            pronunciation="'tu.ʝ̞o̞",
            kind="posesivo",
        ),
        Noun(
            entry="tuyo",
            pronunciation="'tu.ʝ̞o̞",
            gender="m",
            reference_entry=None,
        ),
    }


@page("tuya")
def feminine_noun_and_personal_pronoun_with_unusual_notation():
    return {
        Noun(
            entry="tuya",
            pronunciation="'tu.ʝ̞a̠",
            gender="f",
            reference_entry=None,
        ),
        Pronoun(
            entry="tuya",
            pronunciation="'tu.ʝ̞a̠",
            kind="posesivo",
        ),
    }


@page("tuyas")
def irregular_page_for_pronoun_and_adjective():
    return Pronoun(entry="tuyas", pronunciation="'tu.ʝas")


@page("hacia")
def preposition():
    return Preposition(entry="hacia", pronunciation="'a.sja")


@page("sobre")
def preposition_and_noun():
    return {
        Preposition(entry="sobre", pronunciation="'so.βɾe"),
        Noun(
            entry="sobre",
            pronunciation="'so.βɾe",
            gender="m",
            reference_entry=None,
        ),
    }


@page("el")
def article_with_twice_the_same_entry():
    return {
        Article(entry="el", pronunciation="el", kind="determinado"),
    }


@page("la")
def article_pronoun_and_noun():
    return {
        Article(entry="la", pronunciation="la", kind="determinado"),
        Pronoun(entry="la", pronunciation="la", kind="personal"),
        Noun(
            entry="la",
            pronunciation="la",
            gender="m",
            reference_entry=None,
        ),
    }


@page("maravilloso")
def adjective():
    return Adjective(
        entry="maravilloso",
        pronunciation="ma.ɾa.βi'ʎo.so",
        reference_entry=None,
    )


@page("caro")
def adjective_and_adverb():
    return {
        Adjective(
            entry="caro",
            pronunciation="'ka.ɾo",
            reference_entry=None,
        ),
        Adverb(entry="caro", pronunciation="'ka.ɾo"),
    }


@page("maravillosa")
def adjective_form_without_pronunciation():
    return Adjective(entry="maravillosa", reference_entry="maravilloso", pronunciation=None)


@page("cara")
def noun_and_adjective_with_undecorated_pronunciation_tag():
    return {
        Noun(
            entry="cara",
            pronunciation=None,
            gender="f",
            reference_entry=None,
        ),
        Adjective(entry="cara", pronunciation=None, reference_entry="caro"),
    }


@page("amar")
def transitive_verb():
    return Verb(entry="amar", pronunciation="a'maɾ", kind="transitivo")


@page("venir")
def intransitive_verb():
    return Verb(
        entry="venir",
        pronunciation="be'niɾ",
        kind="intransitivo",
    )


@page("reírse")
def pronominal_verb_without_pronunciation():
    return Verb(entry="reírse", pronunciation=None, kind="pronominal")


@page("íbamos")
def verb_form():
    return VerbForm(
        entry="íbamos",
        pronunciation="'i.βa.mos",
        infinitive="ir",
        mode="indicativo",
        tense="pret imp",
        person="1p",
    )


@page("lucid")
def imperative_verb_form():
    return VerbForm(
        entry="lucid",
        pronunciation=None,
        infinitive="lucir",
        mode="imperativo",
        tense=None,
        person="2p",
    )


@page("acudiría")
def conditional_verb_form():
    return [
        VerbForm(
            entry="acudiría",
            pronunciation=None,
            infinitive="acudir",
            mode="condicional",
            tense=None,
            person="1s",
        ),
        VerbForm(
            entry="acudiría",
            pronunciation=None,
            infinitive="acudir",
            mode="condicional",
            tense=None,
            person="3s",
        ),
    ]


@page("segará")
def verb_form_with_language_mark():
    return VerbForm(
        entry="segará",
        pronunciation="se.ɣa'ɾa",
        infinitive="segar",
        mode="ind",
        tense="fut",
        person="3s",
    )


@page("totora")
def page_without_verb_forms():
    return [
        Noun(
            entry="totora",
            pronunciation="to.'to.ɾa",
            gender="f",
            reference_entry=None,
            number_trait=None,
        )
    ]


@page("o")
def page_without_articles():
    return [
        Noun(
            entry="o",
            pronunciation="o",
            gender="f",
            reference_entry=None,
            number_trait=None,
        ),
        Conjunction(entry="o", pronunciation="o"),
    ]


@page("sido")
def participle():
    return VerbForm(
        entry="sido",
        pronunciation="'si.ðo",
        infinitive="ser",
        mode="participio",
    )


@page("yendo")
def gerund():
    return VerbForm(
        entry="yendo",
        pronunciation="'ʝen̪.do",
        infinitive="ir",
        mode="gerundio",
    )


@page("cerca")
def entry_with_two_adverbs_and_noun_and_personal_verb_form():
    return {
        Adverb(
            entry="cerca",
            pronunciation="'θeɾ.ka",
            kind="lugar",
        ),
        Adverb(
            entry="cerca",
            pronunciation="'θeɾ.ka",
            kind="tiempo",
        ),
        Noun(
            entry="cerca",
            pronunciation="'θeɾ.ka",
            gender="f",
            reference_entry=None,
        ),
        VerbForm(
            entry="cerca",
            pronunciation="'θeɾ.ka",
            infinitive="cercar",
            mode="indicativo",
            tense="presente",
            person="3s",
        ),
        VerbForm(
            entry="cerca",
            pronunciation="'θeɾ.ka",
            infinitive="cercar",
            mode="imperativo",
            tense=None,
            person="2s",
        ),
    }


@page("hecho")
def noun_and_adjective_and_impersonal_verb_form():
    return {
        Noun(
            entry="hecho",
            pronunciation="'e.ʧo",
            gender="m",
            reference_entry=None,
        ),
        Adjective(
            entry="hecho",
            pronunciation="'e.ʧo",
            reference_entry=None,
        ),
        VerbForm(
            entry="hecho",
            pronunciation="'e.ʧo",
            infinitive="hacer",
            mode="participio",
        ),
    }


@page("vino")
def noun_and_adjective_and_personal_verb_form_with_different_pronunciation():
    return {
        Noun(
            entry="vino",
            pronunciation="'bi.no",
            gender="m",
            reference_entry=None,
        ),
        Adjective(
            entry="vino",
            pronunciation="'bi.no",
            reference_entry=None,
        ),
        VerbForm(
            entry="vino",
            pronunciation="'bi.no",
            infinitive="venir",
            mode="indicativo",
            tense="pret ind",
            person="3s",
        ),
    }


@page("pronombre personal")
def ambiguous_pronoun_page():
    return Noun(
        entry="pronombre personal",
        pronunciation="pɾo'nom.bɾe peɾ.so'nal",
        gender="m",
        reference_entry=None,
        number_trait=None,
    )


@page("naranja")
def many_categories_including_pronoun_without_kind():
    return {
        Noun(
            entry="naranja",
            pronunciation="na'ɾaŋ.xa",
            gender="m",
            reference_entry=None,
            number_trait="s",
        ),
        Noun(
            entry="naranja",
            pronunciation="na'ɾaŋ.xa",
            gender="f",
            reference_entry=None,
            number_trait=None,
        ),
        Adjective(entry="naranja", pronunciation="na'ɾaŋ.xa", reference_entry=None),
        Pronoun(entry="naranja", pronunciation="na'ɾaŋ.xa", kind=None),
    }


@page("abundadamente")
def adverb_with_adjective_origin():
    return Adverb(entry="abundadamente", pronunciation="a.βun̪'da.ða'men̪.te", kind=None)


@page("abitado")
def participle_with_lang_marker():
    return VerbForm(
        entry="abitado",
        pronunciation=None,
        infinitive="abitar",
        mode="participio",
        tense=None,
        person=None,
    )
