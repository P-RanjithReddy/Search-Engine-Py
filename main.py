"""Console entry point for the Mini Search Engine."""
from document_loader import DocumentLoader
from search_engine import SearchEngine
from search_history import SearchHistory


def print_banner():
    print("\n" + "=" * 40)
    print("          MINI SEARCH ENGINE")
    print("=" * 40)


def show_results(engine: SearchEngine, history: SearchHistory, query: str):
    try:
        results = engine.search(query)
    except ValueError as exc:
        print(f"\nError: {exc}")
        return
    history.add(query, len(results))
    print("\n========== SEARCH RESULTS ==========")
    if not results:
        print("No exact results found.")
        suggestions = engine.suggestions(query)
        if suggestions:
            print("\nDid you mean:")
            for number, suggestion in enumerate(suggestions, start=1):
                print(f"{number}. {suggestion}")
        else:
            print("No suggestions available. Try a different keyword.")
        return

    for number, result in enumerate(results, start=1):
        print(f"\n{number}. {result.document.name}")
        print(f"   Score: {result.score}")
        print(f"   Matched keywords: {', '.join(result.matched_terms)}")
        excerpt = " ".join(result.document.content.split())
        if len(excerpt) > 160:
            excerpt = excerpt[:157] + "..."
        print(f"   Preview: {excerpt}")


def show_documents(documents):
    print("\n========== ALL DOCUMENTS ==========")
    if not documents:
        print("No readable .txt documents found in the documents folder.")
        return
    for number, doc in enumerate(documents, start=1):
        print(f"{number}. {doc.name} ({len(doc.words)} words)")


def show_statistics(engine: SearchEngine):
    stats = engine.statistics()
    print("\n========== DOCUMENT STATISTICS ==========")
    print(f"Total Documents : {stats['total_documents']}")
    print(f"Total Words     : {stats['total_words']}")
    print(f"Unique Words    : {stats['unique_words']}")
    if stats["largest"]:
        print(f"Largest Document: {stats['largest'][0]} ({stats['largest'][1]} words)")
        print(f"Smallest Document: {stats['smallest'][0]} ({stats['smallest'][1]} words)")
    else:
        print("Largest Document: N/A")
        print("Smallest Document: N/A")


def main():
    try:
        loader = DocumentLoader("documents")
        documents = loader.load_documents()
    except (OSError, FileNotFoundError) as exc:
        print(f"Could not load documents: {exc}")
        print("Add .txt files to the documents folder and restart.")
        return

    engine = SearchEngine(documents)
    history = SearchHistory()
    print_banner()
    print(f"Loaded {len(documents)} document(s).")

    while True:
        print("\n1. Search")
        print("2. View Search History")
        print("3. Clear Search History")
        print("4. View All Documents")
        print("5. Document Statistics")
        print("6. Exit")
        choice = input("\nEnter Choice: ").strip()

        if choice == "1":
            query = input("Enter search query (e.g. python backend, python AND backend): ")
            show_results(engine, history, query)
        elif choice == "2":
            history.show()
        elif choice == "3":
            history.clear()
            print("Search history cleared.")
        elif choice == "4":
            show_documents(documents)
        elif choice == "5":
            show_statistics(engine)
        elif choice == "6":
            print("Thank you for using Mini Search Engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
