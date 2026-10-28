"""Loads text documents from the documents/ folder."""
from collections import Counter
from pathlib import Path
import re
from models import Document


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+(?:'[a-zA-Z0-9]+)?")


class DocumentLoader:
    def __init__(self, folder: str = "documents"):
        self.folder = Path(folder)

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return [token.lower() for token in TOKEN_PATTERN.findall(text)]

    def load_documents(self) -> list[Document]:
        if not self.folder.exists():
            self.folder.mkdir(parents=True, exist_ok=True)
            raise FileNotFoundError(
                f"Documents folder was missing. Created it at: {self.folder.resolve()}. "
                "Add .txt files and run again."
            )
        if not self.folder.is_dir():
            raise NotADirectoryError(f"Not a folder: {self.folder}")

        documents = []
        for path in sorted(self.folder.glob("*.txt")):
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                print(f"Warning: Could not read {path.name}: {exc}")
                continue
            if not content.strip():
                print(f"Warning: Skipping empty file: {path.name}")
                continue
            words = self.tokenize(content)
            counts = Counter(words)
            documents.append(Document(
                name=path.name,
                path=path,
                content=content,
                words=words,
                word_counts=dict(counts),
                unique_words=set(words),
            ))
        return documents
