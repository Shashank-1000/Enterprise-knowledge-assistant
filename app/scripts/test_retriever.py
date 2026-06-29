from app.config.logging_config import setup_logging
from app.retrieval.retriever import RetrieverService


setup_logging()

retriever = RetrieverService()

queries = [
    "What is the assignment about?",
    "What are the functional requirements?",
    "What should be submitted?",
    "What are the evaluation criteria?",
]


for query in queries:
    print("\n" + "#" * 80)
    print(f"QUERY: {query}")
    print("#" * 80)

    results = retriever.retrieve(query)

    for i, result in enumerate(results, start=1):
        print("=" * 60)
        print(f"Result {i}")
        print(f"distance: {result['distance']}")
        print(result["metadata"])
        print()
        print(result["content"][:500])