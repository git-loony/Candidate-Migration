# import requests
# import os
# from src.config import ASHBY_API_KEY

# def create_candidate(candidate):
#     url = "https://api.ashbyhq.com/v1/candidates"

#     headers = {
#         "Authorization": f"Bearer {ASHBY_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "full_name": candidate["full_name"],
#         "email": candidate["email"],
#         "notes": candidate["notes"]
#     }

#     response = requests.post(url, json=data, headers=headers)
#     response.raise_for_status()

#     return response.json()["id"]


# def upload_resume(ashby_id, resume_file):
#     if not resume_file:
#         return False

#     try:
#         url = f"https://api.ashbyhq.com/v1/candidates/{ashby_id}/resume"
#         headers = {"Authorization": f"Bearer {ASHBY_API_KEY}"}

#         with open(resume_file, "rb") as f:
#             files = {"file": (os.path.basename(resume_file), f)}
#             response = requests.post(url, files=files, headers=headers)

#         return response.status_code == 200

#     except Exception as e:
#         print(f"Resume upload failed for {ashby_id}: {e}")
#         return False


# def add_tags(ashby_id, tags):
#     # Placeholder
#     return True if tags else False


#                     -test-
from src.config import MOCK_MODE
import random

def create_candidate(candidate):
    if MOCK_MODE:
        return f"mock_{random.randint(1000,9999)}"

    # real API...


def upload_resume(ashby_id, resume_file):
    if MOCK_MODE:
        return True
    return True


def add_tags(ashby_id, tags):
    if MOCK_MODE:
        return True
    return True