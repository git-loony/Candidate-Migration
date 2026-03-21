import json
import os
import requests
from src.config import RESUME_FOLDER

def fetch_candidates_from_file(file_path, page=1, per_page=10):
    with open(file_path, "r") as f:
        data = json.load(f)

    # Simple pagination simulation
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]


def download_resume(url, candidate_id):
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