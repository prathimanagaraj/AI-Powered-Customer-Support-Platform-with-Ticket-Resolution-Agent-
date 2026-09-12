def analyze_ticket(ticket_title, ticket_description):
    """
    Analyze the support ticket and generate a search query.
    """

    text = f"{ticket_title} {ticket_description}".lower()

    keywords = []

    possible_keywords = [
        "vpn",
        "network",
        "firewall",
        "connection",
        "authentication",
        "login",
        "password",
        "server",
        "internet",
        "email",
        "printer"
    ]

    for keyword in possible_keywords:
        if keyword in text:
            keywords.append(keyword)

    query = " ".join(keywords)

    if not query:
        query = ticket_title

    return {
        "ticket_title": ticket_title,
        "ticket_description": ticket_description,
        "keywords": keywords,
        "query": query
    }