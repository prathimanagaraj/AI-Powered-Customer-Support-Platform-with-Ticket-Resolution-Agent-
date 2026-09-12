from rag.analyzer import analyze_ticket
from rag.retriever import retrieve_documents
from rag.generator import generate_resolution
import time


def run_rag_pipeline(ticket_title, ticket_description):
    """
    Run the complete Milestone 2 RAG workflow.
    """

    # Start response timer
    start_time = time.perf_counter()

    # =========================================================
    # Stage 1: Ticket Analysis & Query Generation
    # =========================================================

    analysis = analyze_ticket(
        ticket_title,
        ticket_description
    )

    # =========================================================
    # Stage 2: Knowledge Base Retrieval
    # =========================================================

    retrieved_documents = retrieve_documents(
        analysis["query"],
        top_k=3
    )

    # =========================================================
    # Stage 3: Context Augmentation
    # =========================================================

    context_parts = []

    for document in retrieved_documents:
        context_parts.append(
            f"Document: {document['title']}\n"
            f"Category: {document['category']}\n"
            f"Content: {document['content']}"
        )

    context = "\n\n".join(context_parts)

    # =========================================================
    # Stage 4: Response Generation
    # =========================================================

    resolution = generate_resolution(
        ticket_title,
        ticket_description,
        retrieved_documents
    )

    # =========================================================
    # Workflow Status
    # =========================================================

    workflow = {
        "ticket_analysis": "completed",
        "knowledge_retrieval": "completed",
        "context_augmentation": "completed",
        "response_generation": "completed"
    }

    # =========================================================
    # Performance Metrics
    # =========================================================

    # Calculate actual response time
    response_time = round(
        time.perf_counter() - start_time,
        3
    )

    # Retrieval accuracy proxy
    if retrieved_documents:
        retrieval_accuracy = round(
            retrieved_documents[0]["score"] * 100,
            2
        )
    else:
        retrieval_accuracy = 0

    # Resolution rate
    if retrieved_documents and resolution:
        resolution_rate = 100
    else:
        resolution_rate = 0

    # =========================================================
    # Final Result
    # =========================================================

    return {
        "analysis": analysis,

        "retrieved_documents": retrieved_documents,

        "context": context,

        "resolution": resolution,

        "workflow": workflow,

        "metrics": {
            "retrieval_accuracy": retrieval_accuracy,
            "resolution_rate": resolution_rate,
            "response_time": response_time
        }
    }