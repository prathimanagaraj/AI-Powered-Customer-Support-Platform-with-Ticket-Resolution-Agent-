from rag.analyzer import analyze_ticket
from rag.retriever import retrieve_documents
from rag.generator import generate_resolution
from email_service import send_resolution_email
from jira_service import create_jira_ticket


class DiagnosisAgent:
    """Agent responsible for analyzing the support ticket."""

    def run(self, title, description):
        analysis = analyze_ticket(title, description)

        return {
            "agent": "Diagnosis Agent",
            "status": "completed",
            "analysis": analysis
        }


class RetrievalAgent:
    """Agent responsible for retrieving relevant knowledge."""

    def run(self, query):
        documents = retrieve_documents(query, top_k=3)

        return {
            "agent": "Retrieval Agent",
            "status": "completed",
            "documents": documents
        }


class ResolutionAgent:
    """Agent responsible for generating a troubleshooting resolution."""

    def run(self, title, description, documents):

        # Check whether the knowledge base contains
        # a relevant document.
        if not documents or documents[0]["score"] <= 0:
            resolution = (
                "No relevant troubleshooting information was found "
                "in the enterprise knowledge base. "
                "The ticket should be escalated to the IT support team."
            )

        else:
            resolution = generate_resolution(
                title,
                description,
                documents
            )

        return {
            "agent": "Resolution Agent",
            "status": "completed",
            "resolution": resolution
        }

class ValidationAgent:
    """Agent responsible for validating the generated resolution."""

    def run(self, documents, resolution):
        if not documents or not resolution:
            confidence = 0

        else:
            top_score = documents[0]["score"]

            # Evaluate retrieval quality.
            if top_score >= 0.50:
                confidence = 90
            elif top_score >= 0.30:
                confidence = 75
            elif top_score >= 0.20:
                confidence = 60
            else:
                confidence = 40

        if confidence >= 70:
            decision = "auto_resolution"
        else:
            decision = "escalation"

        return {
            "agent": "Validation Agent",
            "status": "completed",
            "confidence": confidence,
            "decision": decision
        }
class MultiAgentOrchestrator:
    """Coordinates the SupportPilot multi-agent workflow."""

    def __init__(self):
        self.diagnosis_agent = DiagnosisAgent()
        self.retrieval_agent = RetrievalAgent()
        self.resolution_agent = ResolutionAgent()
        self.validation_agent = ValidationAgent()

    def run(self, title, description, user_email=None):

        # 1. Diagnosis Agent
        diagnosis = self.diagnosis_agent.run(
            title,
            description
        )

        query = diagnosis["analysis"]["query"]

        # 2. Retrieval Agent
        retrieval = self.retrieval_agent.run(query)

        documents = retrieval["documents"]

        # 3. Resolution Agent
        resolution = self.resolution_agent.run(
            title,
            description,
            documents
        )

        # 4. Validation Agent
        validation = self.validation_agent.run(
            documents,
            resolution["resolution"]
        )

        confidence = validation["confidence"]
        decision = validation["decision"]

        # 5. Take action based on confidence
        action_result = None

        if decision == "auto_resolution":

            if user_email:
                action_result = send_resolution_email(
                    user_email,
                    title,
                    resolution["resolution"],
                    confidence
                )
            else:
                action_result = {
                    "status": "not_sent",
                    "message": "User email was not provided."
                }

        else:

            action_result = create_jira_ticket(
                title,
                description,
                confidence
            )

        return {
            "diagnosis": diagnosis,
            "retrieval": retrieval,
            "resolution": resolution,
            "validation": validation,
            "action": action_result
        }