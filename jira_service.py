import os
import requests
from dotenv import load_dotenv

load_dotenv()


def create_jira_ticket(
    ticket_title,
    ticket_description,
    confidence,
    priority="High"
):
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_project_key = os.getenv("JIRA_PROJECT_KEY")

    if not all([
        jira_url,
        jira_email,
        jira_api_token,
        jira_project_key
    ]):
        return {
            "status": "not_configured",
            "message": "Jira credentials are not configured."
        }

    issue_url = f"{jira_url.rstrip('/')}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {
                "key": jira_project_key
            },
            "summary": ticket_title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    f"{ticket_description}\n\n"
                                    f"SupportPilot confidence: "
                                    f"{confidence}%"
                                )
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            },
            "priority": {
                "name": priority
            }
        }
    }

    try:
        response = requests.post(
            issue_url,
            json=payload,
            auth=(jira_email, jira_api_token),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code in (200, 201):
            data = response.json()

            return {
                "status": "created",
                "issue_key": data.get("key"),
                "message": "Jira ticket created successfully."
            }

        return {
            "status": "failed",
            "message": response.text
        }

    except requests.RequestException as error:
        return {
            "status": "failed",
            "message": str(error)
        }