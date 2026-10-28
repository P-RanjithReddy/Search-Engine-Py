# Mini Search Engine (Console-Based Python)

## Overview
A small object-oriented search engine that reads `.txt` files from `documents/`, ranks matching files by relevance, ignores common stop words, suggests similar words when nothing matches, keeps session-only search history, and reports document statistics.

## Requirements
- Python 3.9 or newer (no third-party packages required)
- No database or API required

## Run
1. Extract `mini_search_engine.zip`.
2. Open a terminal in the extracted `mini_search_engine` folder.
3. Run:
   ```bash
   python main.py
   ```
   On Windows, `py main.py` also works if the Python launcher is installed.

## Menu
1. Search
2. View Search History
3. Clear Search History
4. View All Documents
5. Document Statistics
6. Exit

## Search examples
- `python`
- `python backend`
- `FASTAPI development` (case-insensitive)
- `python AND backend` (only documents containing both terms)
- `python OR django` (documents containing either term)

Stop words such as `the`, `is`, `a`, `an`, `of`, `to`, `in`, `and`, `for`, `with`, and `on` are ignored. In Boolean queries, `AND` and `OR` are treated as operators rather than stop words.

## Relevance scoring
For every matched query term, the engine adds a TF-IDF-like value:
- Term frequency (TF): repeated occurrences in a document increase its contribution.
- Inverse document frequency (IDF): terms appearing in fewer documents receive more weight.
- Query coverage bonus: documents matching a larger fraction of query terms receive a higher score.
Results are sorted by descending score, then by filename.

This is a lightweight educational ranking formula, not a full production search index.

## Search suggestions
When there are no matching documents, Python's built-in `difflib.get_close_matches` compares query terms with the vocabulary found in the loaded documents and suggests similar words.

## Data structures / OOP
- `Document` and `SearchResult` dataclasses model data.
- `DocumentLoader` handles file discovery, reading, and tokenization.
- `SearchEngine` performs searching, ranking, suggestions, and statistics.
- `SearchHistory` stores searches in memory for this execution.
- Lists hold documents/results/history; dictionaries hold term counts and statistics; sets hold unique words/vocabulary.

## Exceptions and edge cases
- Missing folder: created with an explanatory message; add `.txt` files and restart.
- Empty files: skipped with a warning.
- File read errors: reported and skipped.
- Empty query: rejected with a friendly message.
- Invalid menu choice: prompts the user again.
- Empty document collection: handled without crashing.

## Complexity
Let `D` be the number of documents, `V` the total number of tokens, and `Q` the number of unique query terms.
- Loading: approximately O(V).
- This simple implementation scans documents for each query term; ranking is roughly O(D × Q) plus the cost of document-frequency counting.
- Sorting R matching results: O(R log R).
- For one million documents, use an inverted index (term -> document IDs), persistent indexing, efficient tokenization, and possibly a search library such as Whoosh, Elasticsearch, or OpenSearch. Batch indexing and caching would avoid rescanning every document for each query.

## Screenshots for submission
Capture three screenshots from your terminal:
1. Search results: choose `1`, enter `python backend`.
2. Search suggestion: choose `1`, enter `pyhtonxyz` (if no suggestion appears, try a misspelling such as `pyhton`).
3. Statistics: choose `5`.
Use Windows Snipping Tool (`Win + Shift + S`) and save the images for your submission.

## Project structure
```text
mini_search_engine/
├── main.py
├── search_engine.py
├── document_loader.py
├── models.py
├── search_history.py
├── documents/
│   ├── python.txt
│   ├── fastapi.txt
│   └── ... (10 sample documents)
└── README.md
```
