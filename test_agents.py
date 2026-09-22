from agents import MultiAgentOrchestrator


orchestrator = MultiAgentOrchestrator()
title = "Quantum printer synchronization failure"
description = "The office printer is experiencing an unusual synchronization problem with an unknown system."
result = orchestrator.run(
    title,
    description,
    "test@example.com"
)


print("\n========== M3 MULTI-AGENT TEST ==========")

print("\n1. DIAGNOSIS AGENT")
print(result["diagnosis"]["analysis"])

print("\n2. RETRIEVAL AGENT")
for document in result["retrieval"]["documents"]:
    print(
        document["id"],
        "-",
        document["title"],
        "- Score:",
        document["score"]
    )

print("\n3. RESOLUTION AGENT")
print(result["resolution"]["resolution"])

print("\n4. VALIDATION AGENT")
print(
    "Confidence:",
    result["validation"]["confidence"],
    "%"
)

print(
    "Decision:",
    result["validation"]["decision"]

)
print("\n5. ACTION")
print(result["action"])

print("\n==========================================")