import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class PartialTerm:
    entry: str
    pronunciation: Optional[str]


pronunciation_pattern = re.compile(r"\|\s*fon(?:e|o)\s*=\s*([^-|}\n]+)")


def extract_partial_term(entry: str, content: str) -> PartialTerm:
    pronunciation_match = pronunciation_pattern.search(content)

    return PartialTerm(
        entry=entry,
        pronunciation=pronunciation_match.group(1).replace("\u02c8", "'")
        if pronunciation_match
        else None,
    )
