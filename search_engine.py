"""Search, relevance ranking, Boolean operators, and suggestions."""
from collections import Counter
from difflib import get_close_matches
import math
from document_loader import DocumentLoader
from models import Document, SearchResult


class SearchEngine:
    STOP_WORDS = {
        "the", "is", "a", "an", "of", "to", "in", "and", "for", "with",
        "on", "are", "was", "were", "be", "as", "at", "by", "from", "it",
        "this", "that", "or", "if", "into", "your", "you", "can", "will",
    }

    def __init__(self, documents: list[Document]):
        self.documents = documents
        self.vocabulary = set()
        self.term_frequency = Counter()
        for doc in documents:
            self.vocabulary.update(doc.unique_words)
            self.term_frequency.update(doc.word_counts)

    def _terms(self, query: str) -> list[str]:
        return [
            word for word in DocumentLoader.tokenize(query)
            if word not in self.STOP_WORDS
        ]

    def search(self, query: str) -> list[SearchResult]:
        raw = query.strip()
        if not raw:
            raise ValueError("Search query cannot be empty.")

        # Boolean mode is activated only for explicit AND/OR syntax.
        upper = raw.upper()
        operator = None
        if " AND " in upper:
            operator = "AND"
            parts = raw.split()
            terms = self._terms(" ".join(p for p in parts if p.upper() != "AND"))
        elif " OR " in upper:
            operator = "OR"
            parts = raw.split()
            terms = self._terms(" ".join(p for p in parts if p.upper() != "OR"))
        else:
            terms = self._terms(raw)

        # Remove duplicates while preserving query order.
        terms = list(dict.fromkeys(terms))
        if not terms:
            return []

        results = []
        total_docs = max(len(self.documents), 1)
        for doc in self.documents:
            present = [term for term in terms if doc.word_counts.get(term, 0) > 0]
            if operator == "AND" and len(present) != len(terms):
                continue
            if operator == "OR" and not present:
                continue
            if operator is None and not present:
                continue

            # TF-IDF-like score: query-term frequency in the document, weighted
            # by inverse document frequency. A small exact-match bonus rewards
            # documents containing more of the query terms.
            score = 0.0
            for term in present:
                tf = doc.word_counts[term]
                df = sum(1 for other in self.documents if term in other.unique_words)
                idf = math.log(1 + total_docs / (1 + df)) + 1
                score += (1 + math.log(tf)) * idf
            coverage = len(present) / len(terms)
            score *= (1 + coverage)
            results.append(SearchResult(doc, round(score, 2), present))

        return sorted(results, key=lambda item: (-item.score, item.document.name.lower()))

    def suggestions(self, query: str, limit: int = 3) -> list[str]:
        terms = self._terms(query)
        if not terms:
            return []
        vocab = sorted(self.vocabulary)
        suggestions = []
        for term in terms:
            matches = get_close_matches(term, vocab, n=limit, cutoff=0.55)
            for match in matches:
                if match not in suggestions:
                    suggestions.append(match)
        # Add common two-word phrases from the vocabulary where helpful.
        if not suggestions and vocab:
            suggestions = sorted(vocab, key=lambda word: abs(len(word) - len(terms[0])))[:limit]
        return suggestions[:limit]

    def statistics(self) -> dict:
        if not self.documents:
            return {
                "total_documents": 0, "total_words": 0, "unique_words": 0,
                "largest": None, "smallest": None,
            }
        largest = max(self.documents, key=lambda doc: len(doc.words))
        smallest = min(self.documents, key=lambda doc: len(doc.words))
        return {
            "total_documents": len(self.documents),
            "total_words": sum(len(doc.words) for doc in self.documents),
            "unique_words": len(self.vocabulary),
            "largest": (largest.name, len(largest.words)),
            "smallest": (smallest.name, len(smallest.words)),
        }
