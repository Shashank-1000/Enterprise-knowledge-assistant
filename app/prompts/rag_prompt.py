from typing import Dict, List


def build_rag_prompt(
    question: str,
    retrieved_chunks: List[Dict],
) -> str:
    context_blocks = []

    for idx, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        context_blocks.append(
            f"""
[Source {idx}]
Document: {metadata.get("document_name")}
Page: {metadata.get("page_number")}
Section: {metadata.get("section_title")}

Content:
{chunk["content"]}
"""
        )

    context = "\n".join(context_blocks)

    return f"""
You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the provided context.

Important rules:
1. Use only facts present in the context.
2. Do not invent or assume information.
3. If the answer is partially present, answer with the available information and do not claim it is unavailable.
4. If the answer is completely absent from the context, say:
   "The provided documents do not contain enough information to answer this question."
5. Prefer complete, useful answers over very short answers.
6. When the question asks for a list, return all relevant items found in the context.
7. Cite source numbers naturally, for example: "According to Source 1..." or "(Source 1, Page 2)."

Context:
{context}

User Question:
{question}

Answer:
"""