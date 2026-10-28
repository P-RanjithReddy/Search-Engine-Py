"""In-memory search history for the current program session."""
from datetime import datetime


class SearchHistory:
    def __init__(self):
        self.entries: list[dict] = []

    def add(self, query: str, result_count: int) -> None:
        self.entries.append({
            "query": query,
            "result_count": result_count,
            "time": datetime.now().strftime("%H:%M:%S"),
        })

    def show(self) -> None:
        if not self.entries:
            print("\nSearch history is empty.")
            return
        print("\n========== SEARCH HISTORY ==========")
        for index, entry in enumerate(self.entries, start=1):
            print(f"{index}. [{entry['time']}] {entry['query']} "
                  f"({entry['result_count']} result(s))")

    def clear(self) -> None:
        self.entries.clear()
