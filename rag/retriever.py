import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_knowledge_base():
    """Load documents from the enterprise knowledge base."""

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_path = os.path.join(base_dir, "data", "knowledge_base.json")

    with open(kb_path, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_documents(query, top_k=3):
    """
    Search the knowledge base and return the most relevant documents.
    """

    documents = load_knowledge_base()

    document_texts = [
        f"{doc['title']} {doc['category']} {doc['content']}"
        for doc in documents
    ]

    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(
        document_texts + [query]
    )

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "id": documents[index]["id"],
            "title": documents[index]["title"],
            "category": documents[index]["category"],
            "content": documents[index]["content"],
            "score": round(float(similarities[index]), 3)
        })

    return results