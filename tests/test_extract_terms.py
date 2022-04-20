from pytest import mark

from info.gianlucacosta.cervantes import extract_terms

from .pages import get_expected_terms, get_expected_terms_by_test_page, read_page_from_file


@mark.parametrize("title", get_expected_terms_by_test_page().keys())
def test_extract_terms(title: str):
    expected_terms = get_expected_terms(title)

    raw_page_contents = read_page_from_file(title)

    extracted_terms = set(extract_terms(raw_page_contents))

    assert extracted_terms == expected_terms
