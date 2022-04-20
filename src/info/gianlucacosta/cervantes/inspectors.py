import re
from functools import wraps
from inspect import signature
from re import Match, Pattern
from typing import Callable, Optional, get_args

from info.gianlucacosta.eos.core.functional import Mapper, Producer

from .partial_term import PartialTerm, extract_partial_term
from .terms import (
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

PotentialTermPattern = Pattern[str]

PotentialTermMatch = Match[str]

PotentialMatchInspector = Callable[[PartialTerm, PotentialTermMatch], Optional[SpanishTerm]]


potential_match_inspectors: list[tuple[PotentialTermPattern, PotentialMatchInspector]] = []


def inspector(
    expected_regex: str,
) -> Mapper[PotentialMatchInspector, PotentialMatchInspector]:
    def decorator(
        inspector_to_register: PotentialMatchInspector,
    ) -> PotentialMatchInspector:
        expected_pattern = re.compile(expected_regex)
        potential_match_inspectors.append((expected_pattern, inspector_to_register))
        return inspector_to_register

    return decorator


def basic_term_inspector(
    expected_regex: str,
) -> Mapper[Producer[Optional[SpanishTerm]], PotentialMatchInspector]:
    def decorator(
        empty_inspector_anchor: Producer[Optional[SpanishTerm]],
    ) -> PotentialMatchInspector:
        anchor_signature = signature(empty_inspector_anchor)
        term_class, _ = get_args(anchor_signature.return_annotation)

        @inspector(expected_regex)
        @wraps(empty_inspector_anchor)
        def actual_inspector(
            partial_term: PartialTerm, _: PotentialTermMatch
        ) -> Optional[SpanishTerm]:
            return term_class(entry=partial_term.entry, pronunciation=partial_term.pronunciation)

        return actual_inspector

    return decorator


def extract_terms_from_spanish_block(page_title: str, spanish_block: str) -> list[SpanishTerm]:
    partial_term = extract_partial_term(page_title, spanish_block)

    return [
        term
        for potential_term_pattern, match_inspector in potential_match_inspectors
        for term_match in potential_term_pattern.finditer(spanish_block)
        if (term := match_inspector(partial_term, term_match))
    ]


@inspector(
    r"""(?x)(?i)
\{\{
    \s*forma\s+verbo\s*\|
    (?:l(?:a|e)ng\s*=\s*es\s*\|)?
    \s*(?P<infinitive>\w[\w.\-\ ]*\w)\s*\|
    \s*(?:p\s*=\s*)?(?P<person>[\w.\-\ ]+)\s*\|
    \s*(?:t\s*=\s*)?(?P<tense>[\w.\-\ ]+?)\s*
    (?:(?:\|)(?:\s*m\s*=)?\s*(?P<mode>[\w.\-\ ]+?))?\s*
    [}|]
"""
)
def extract_personal_verb_form(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[VerbForm]:
    mode = potential_match.group("mode")
    tense = potential_match.group("tense")

    if tense.startswith("imperat") or tense.startswith("condi"):
        actual_mode = tense
        actual_tense = None
    else:
        actual_mode = mode
        actual_tense = tense

    if not actual_mode:
        return None

    return VerbForm(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        infinitive=potential_match.group("infinitive"),
        mode=actual_mode,
        tense=actual_tense,
        person=potential_match.group("person"),
    )


@inspector(
    r"""(?x)(?i)
\{\{
    \s*(?P<mode>participio|gerundio)\s*\|
    (?:l(?:a|e)ng\s*=\s*es\s*\|)?
    \s*(?P<infinitive>\w[\w.\-\ ]*\w)\s*
[\|}]
"""
)
def extract_impersonal_verb_form(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[VerbForm]:
    return VerbForm(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        mode=potential_match.group("mode"),
        infinitive=potential_match.group("infinitive"),
    )


@inspector(
    r"""(?x)(?i)(?s)
    (?:
        (?:\{\{)
        |
        (?:==)
    )\s*

    (?:
        (?:
            sustantivo\s+(?P<gender_1>m|f).+?\n
            (?:
                [^{]*?
                \{\{
                    \s*inflect.es.sust.\s*(?P<number_trait>s|p|i)
            )?
        )
        |
        (?:
            =+\s*Forma\s+sustantiva\s+(?P<gender_2>m|f).+?
            \{\{\s*forma\s+sustantivo\s+plural\s*\|\s*(?P<singular_form>\w[\w.\-\ ]*\w)\s*
        )
    )
"""
)
def extract_noun(partial_term: PartialTerm, potential_match: PotentialTermMatch) -> Optional[Noun]:
    return Noun(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        gender=potential_match.group("gender_1") or potential_match.group("gender_2"),
        reference_entry=potential_match.group("singular_form"),
        number_trait=potential_match.group("number_trait"),
    )


@inspector(
    r"""(?x)(?i)
\{\{
    \s*verbo(?:\s+(?P<kind>\w+))?
"""
)
def extract_verb(partial_term: PartialTerm, potential_match: PotentialTermMatch) -> Optional[Verb]:
    return Verb(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        kind=potential_match.group(1),
    )


@inspector(
    r"""(?x)(?i)
    \{\{\s*
        (?:
            (?:forma\s+adjetivo\s*\|\s*[^|]+?\|\s*(?P<reference_entry>\w[\w.\-\ ]*\w)\s*\|)
            |
            (?:adjetivo\b)
        )
    """
)
def extract_adjective(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[Adjective]:
    return Adjective(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        reference_entry=potential_match.group("reference_entry"),
    )


@inspector(
    r"""(?i)(?x)
\{\{
    \s*adverbio
        (?:
            \s+de\s+(?P<kind>\w+)
            \s*
        )?
"""
)
def extract_adverb(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[Adverb]:
    kind = potential_match.group("kind")

    if kind in ["adjetivo", "sustantivo"]:
        return None

    return Adverb(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        kind=kind,
    )


@basic_term_inspector(r"(?i)\{\{\s*conjunción\b")
def extract_conjunction() -> Optional[Conjunction]:
    pass


@basic_term_inspector(r"(?i)\{\{\s*preposición\b")
def extract_preposition() -> Optional[Preposition]:
    pass


@inspector(
    r"""(?x)(?i)
    (?:
        (?:\{\{)
        |
        (?:==)
    )\s*

    (?:
        (?:
            forma\s+(?:de\s+)?pronombre(?:\s+(?P<kind_1>\w{4,}))?
        )

        |

        (?:
            pronombre\s*

            (?:
                (?P<kind_2>\w{4,})
                |
                (?:\|\s*[^|}]+(\|\s*(?P<kind_3>\w{4,}))?)
                |
                [=\}]
            )
        )
    )
    """
)
def extract_pronoun(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[Pronoun]:
    return Pronoun(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        kind=potential_match.group("kind_1")
        or potential_match.group("kind_2")
        or potential_match.group("kind_3"),
    )


@inspector(
    r"""(?i)(?x)
\{\{
    \s*artículo
    (?:\s+(?P<kind>\w+?)\s*[|}])?
"""
)
def extract_article(
    partial_term: PartialTerm, potential_match: PotentialTermMatch
) -> Optional[Article]:
    return Article(
        entry=partial_term.entry,
        pronunciation=partial_term.pronunciation,
        kind=potential_match.group("kind"),
    )


@basic_term_inspector(r"(?i)\{\{\s*interjección\b")
def extract_interjection() -> Optional[Interjection]:
    pass
