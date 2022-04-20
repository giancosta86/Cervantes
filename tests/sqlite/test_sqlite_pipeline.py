from functools import wraps
from io import StringIO
from sqlite3 import Connection, connect
from typing import Optional

from info.gianlucacosta.eos.core.functional import Unit
from info.gianlucacosta.eos.core.io.files.temporary import Uuid4TemporaryPath
from info.gianlucacosta.eos.core.multiprocessing.pool import AnyProcessPool, InThreadPool
from info.gianlucacosta.wikiprism.dictionary.sqlite import SqliteDictionary
from info.gianlucacosta.wikiprism.pipeline import run_extraction_pipeline
from info.gianlucacosta.wikiprism.pipeline.protocol import TermExtractor, WikiFile
from info.gianlucacosta.wikiprism.pipeline.sqlite import SqlitePipelineStrategy

from info.gianlucacosta.cervantes import extract_terms
from info.gianlucacosta.cervantes.sqlite.dictionary import SpanishSqliteDictionary
from info.gianlucacosta.cervantes.terms import SpanishTerm

from ..pages import build_test_wiki, get_expected_terms, get_expected_terms_by_test_page
from .schema import count_terms_in_db


class SpanishTestSqlitePipelineStrategy(SqlitePipelineStrategy[SpanishTerm]):
    def __init__(
        self,
        target_db_path: str,
        wiki_file: WikiFile,
    ) -> None:
        super().__init__(target_db_path=target_db_path)
        self._wiki_file = wiki_file
        self.exception: Optional[Exception] = None

    def create_pool(self) -> AnyProcessPool:
        return InThreadPool()

    def get_wiki_file(self) -> WikiFile:
        return self._wiki_file

    def get_term_extractor(self) -> TermExtractor[SpanishTerm]:
        return extract_terms

    def on_message(self, message: str) -> None:
        pass

    def on_ended(self, exception: Optional[Exception]) -> None:
        self.exception = exception
        super().on_ended(exception)

    def create_dictionary_from_connection(
        self, connection: Connection
    ) -> SqliteDictionary[SpanishTerm]:
        return SpanishSqliteDictionary(connection)


def sqlite_pipeline(*page_titles: str):
    def decorator(test_function: Unit):
        @wraps(test_function)
        def wrapper() -> None:
            expected_terms = get_expected_terms(*page_titles)

            wiki_text = build_test_wiki(*page_titles)
            wiki_file = StringIO(wiki_text)

            with Uuid4TemporaryPath(extension_including_dot=".db") as temp_db_path:
                pipeline_strategy = SpanishTestSqlitePipelineStrategy(
                    wiki_file=wiki_file, target_db_path=temp_db_path
                )
                pipeline_handle = run_extraction_pipeline(pipeline_strategy)
                pipeline_handle.join()

                assert pipeline_strategy.exception is None

                with connect(temp_db_path) as asserting_connection:
                    terms_in_db_counter = count_terms_in_db(asserting_connection)

                    assert terms_in_db_counter == len(expected_terms)

        return wrapper

    return decorator


@sqlite_pipeline("también")
def test_single_page_with_one_term():
    pass


@sqlite_pipeline(*get_expected_terms_by_test_page().keys())
def test_with_all_the_test_pages():
    pass
