# import requests
# import os
# from src.config import MANATAL_API_KEY, PER_PAGE, RESUME_FOLDER

# def fetch_candidates(page=1):
#     url = f"https://api.manatal.com/open/v3/candidates?page={page}&per_page={PER_PAGE}"
#     headers = {"Authorization": f"Bearer {MANATAL_API_KEY}"}

#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     return response.json()


# def download_resume(url, candidate_id):
#     if not url:
#         return None

#     try:
#         response = requests.get(url)
#         response.raise_for_status()

#         os.makedirs(RESUME_FOLDER, exist_ok=True)
#         file_path = os.path.join(RESUME_FOLDER, f"{candidate_id}.pdf")

#         with open(file_path, "wb") as f:
#             f.write(response.content)

#         return file_path

#     except Exception as e:
#         print(f"Resume download failed for {candidate_id}: {e}")
#         return None


#    -test-
from src.config import MOCK_MODE
import json
import requests
import os
from src.config import MANATAL_API_KEY, PER_PAGE, RESUME_FOLDER


def fetch_candidates(page=1):
    if MOCK_MODE:
        with open("data/candidates.json") as f:
            data = json.load(f)

        # simulate pagination
        page_size = 2
        start = (page - 1) * page_size
        end = start + page_size

        return data[start:end]

    url = f"https://api.manatal.com/open/v3/candidates?page={page}&per_page={PER_PAGE}"
    headers = {"Authorization": f"Bearer {MANATAL_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def download_resume(url, candidate_id):
    if MOCK_MODE:
        return None  # no resumes in mock mode

    if not url:
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()

        os.makedirs(RESUME_FOLDER, exist_ok=True)
        file_path = os.path.join(RESUME_FOLDER, f"{candidate_id}.pdf")

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    except Exception as e:
        print(f"Resume download failed for {candidate_id}: {e}")
        return None