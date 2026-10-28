"""Data models for the Mini Search Engine."""
from dataclasses import dataclass
from pathlib import Path
from typing import Set


@dataclass
class Document:
    name: str
    path: Path
    content: str
    words: list[str]
    word_counts: dict[str, int]
    unique_words: Set[str]


@dataclass
class SearchResult:
    document: Document
    score: float
    matched_terms: list[str]
