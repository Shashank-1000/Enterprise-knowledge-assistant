from app.config.logging_config import setup_logging
from app.services.knowledge_assistant import KnowledgeAssistantService


setup_logging()

assistant = KnowledgeAssistantService()

questions = [
    "What is this assignment about?",
    "What are the functional requirements?",
    "What should be submitted?",
    "What are the evaluation criteria?",
]

for question in questions:
    print("\n" + "#" * 80)
    print(f"QUESTION: {question}")
    print("#" * 80)

    response = assistant.answer_question(question)

    print("\nANSWER:")
    print(response.answer)

    print("\nSOURCES:")
    for source in response.sources:
        print(source)

    print("\nCONFIDENCE:")
    print(response.confidence)