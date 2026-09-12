from rag.pipeline import run_rag_pipeline


# Example support ticket
title = "VPN Connection Failing on Corporate Network"

description = (
    "Unable to connect to the corporate VPN since this morning. "
    "The VPN connection keeps failing."
)


# Run the Milestone 2 RAG pipeline
result = run_rag_pipeline(title, description)


print("\n========== TICKET ANALYSIS ==========")
print(result["analysis"])


print("\n========== RETRIEVED DOCUMENTS ==========")

for document in result["retrieved_documents"]:
    print(
        f"\nID: {document['id']}"
        f"\nTitle: {document['title']}"
        f"\nCategory: {document['category']}"
        f"\nSimilarity Score: {document['score']}"
    )


print("\n========== CONTEXT ==========")
print(result["context"])


print("\n========== GENERATED RESOLUTION ==========")
print(result["resolution"])


print("\n========== WORKFLOW STATUS ==========")
print(result["workflow"])