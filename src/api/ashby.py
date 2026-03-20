from src.config import MOCK_MODE
import random

def create_candidate(candidate):
    if MOCK_MODE:
        return f"mock_{random.randint(1000,9999)}"

    import requests
    from src.config import ASHBY_API_KEY

    url = "https://api.ashbyhq.com/v1/candidates"
    headers = {
        "Authorization": f"Bearer {ASHBY_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=candidate, headers=headers)
    response.raise_for_status()

    return response.json()["id"]


def upload_resume_stream(ashby_id, file_bytes):
    if MOCK_MODE:
        return True

    import requests
    from src.config import ASHBY_API_KEY

    url = f"https://api.ashbyhq.com/v1/candidates/{ashby_id}/resume"
    headers = {"Authorization": f"Bearer {ASHBY_API_KEY}"}

    files = {"file": ("resume.pdf", file_bytes)}

    response = requests.post(url, files=files, headers=headers)

    return response.status_code == 200


def add_tags(ashby_id, tags):
    if MOCK_MODE:
        return True
    return True