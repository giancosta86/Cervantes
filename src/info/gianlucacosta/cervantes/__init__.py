import re
from logging import getLogger
from sqlite3 import Connection

from info.gianlucacosta.wikiprism.page import Page

from .inspectors import extract_terms_from_spanish_block
from .sqlite.dictionary import SpanishSqliteDictionary
from .terms import SpanishTerm

logger = getLogger(__name__)


language_header_beginning_pattern = re.compile(r"(?m)^\s*==\s*\{\{lengua\|")


def extract_terms(page: Page) -> list[SpanishTerm]:
    """
    Given a wiki page, extracts its Spanish terms.

    In WikiPrism's model, this is a TermExtractor[SpanishTerm].
    """
    if ":" in page.title:
        if __debug__:
            logger.info(
                "Skipping page '%s', as its title contains metainfo characters",
                page.title,
            )
        return []

    result: list[SpanishTerm] = []

    spanish_blocks = [
        block
        for block in language_header_beginning_pattern.split(page.text)
        if block.startswith("es")
    ]

    for spanish_block in spanish_blocks:
        terms_in_block = extract_terms_from_spanish_block(page.title, spanish_block)
        result.extend(terms_in_block)

    return result


def create_sqlite_dictionary(connection: Connection) -> SpanishSqliteDictionary:
    """
    Creates a SqliteDictionary containing Spanish terms.

    In WikiPrism's model, this is a SqliteDictionaryFactory[SpanishTerm].
    """
    return SpanishSqliteDictionary(connection)


def get_wiki_url() -> str:
    return get_wiktionary_url()


def get_wiktionary_url() -> str:
    """
    Returns the url to official Wikcionario download file - or a local URL when in __debug__.

    The local URL is precisely the one available by running "python -m http.server".
    """
    return (
        (
            "https://dumps.wikimedia.org/"
            "eswiktionary/latest/"
            "eswiktionary-latest-pages-articles.xml.bz2"
        )
        if not __debug__
        else ("http://localhost:8000/eswiktionary-latest-pages-articles.xml.bz2")
    )
