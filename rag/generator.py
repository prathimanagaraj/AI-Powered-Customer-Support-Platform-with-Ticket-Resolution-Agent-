def generate_resolution(ticket_title, ticket_description, retrieved_documents):
    """
    Generate a troubleshooting resolution using
    the retrieved enterprise knowledge-base documents.
    """

    if not retrieved_documents:
        return (
            "No relevant troubleshooting information was found "
            "in the enterprise knowledge base."
        )

    resolution_steps = []

    for document in retrieved_documents:
        content = document["content"]

        if content not in resolution_steps:
            resolution_steps.append(content)

    response = f"Troubleshooting Resolution for: {ticket_title}\n\n"

    response += (
        "Based on the enterprise knowledge base, "
        "follow these troubleshooting steps:\n\n"
    )

    for number, step in enumerate(resolution_steps, start=1):
        response += f"{number}. {step}\n\n"

    response += (
        "If the issue persists after following these steps, "
        "escalate the ticket to the appropriate IT support team."
    )

    return response