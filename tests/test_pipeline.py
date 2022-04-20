from functools import wraps
from io import StringIO
from typing import Callable, Optional

from info.gianlucacosta.eos.core.multiprocessing.pool import AnyProcessPool, InThreadPool
from info.gianlucacosta.wikiprism.dictionary import Dictionary
from info.gianlucacosta.wikiprism.dictionary.memory import InMemoryDictionary
from info.gianlucacosta.wikiprism.pipeline import PipelineStrategy, run_extraction_pipeline
from info.gianlucacosta.wikiprism.pipeline.protocol import TermExtractor, WikiFile

from info.gianlucacosta.cervantes import extract_terms
from info.gianlucacosta.cervantes.terms import SpanishTerm

from .pages import build_test_wiki, get_expected_terms, get_expected_terms_by_test_page


class SpanishTestPipelineStrategy(PipelineStrategy[SpanishTerm]):
    def __init__(self, dictionary: Dictionary[SpanishTerm], wiki_file: WikiFile) -> None:
        super().__init__()
        self._dictionary = dictionary
        self._wiki_file = wiki_file
        self.exception: Optional[Exception] = None

    def create_pool(self) -> AnyProcessPool:
        return InThreadPool()

    def initialize_pipeline(self) -> None:
        pass

    def create_dictionary(self) -> Dictionary[SpanishTerm]:
        return self._dictionary

    def get_wiki_file(self) -> WikiFile:
        return self._wiki_file

    def get_term_extractor(self) -> TermExtractor[SpanishTerm]:
        return extract_terms

    def perform_last_successful_steps(self) -> None:
        pass

    def on_message(self, message: str) -> None:
        pass

    def on_ended(self, exception: Optional[Exception]) -> None:
        self.exception = exception


def pipeline(*page_titles: str):
    def decorator(test_function: Callable[[], None]):
        @wraps(test_function)
        def wrapper():
            expected_terms = get_expected_terms(*page_titles)
            dictionary = InMemoryDictionary()

            wiki_text = build_test_wiki(*page_titles)
            wiki_file = StringIO(wiki_text)

            pipeline_strategy = SpanishTestPipelineStrategy(
                dictionary=dictionary, wiki_file=wiki_file
            )

            pipeline_handle = run_extraction_pipeline(pipeline_strategy)
            pipeline_handle.join()

            assert pipeline_strategy.exception is None

            assert dictionary.terms == expected_terms

        return wrapper

    return decorator


@pipeline("naranja")
def test_pipeline_on_single_word():
    pass


@pipeline("también", "rápidamente", "aunque", "ah", "modo", "ésta", "hacia")
def test_combination_of_basic_pages():
    pass


@pipeline(*get_expected_terms_by_test_page().keys())
def test_combination_of_all_pages():
    pass
