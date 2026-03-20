import time
import requests
import io

from src.api.manatal import fetch_candidates
from src.api.ashby import create_candidate, upload_resume_stream, add_tags
from src.services.transform import map_candidate
from src.db.operations import log_candidate, get_last_processed_id
from src.config import API_SLEEP

def migrate():
    last_processed = get_last_processed_id()
    page = 1

    while True:
        candidates = fetch_candidates(page)

        if not candidates:
            print("No more candidates.")
            break

        for m in candidates:
            manatal_id = m.get("id")

            if last_processed and manatal_id <= last_processed:
                continue

            candidate = map_candidate(m)

            try:
                ashby_id = create_candidate(candidate)

                # Resume streaming
                cv_status = False
                if candidate["resume_url"]:
                    try:
                        response = requests.get(candidate["resume_url"])
                        response.raise_for_status()

                        file_bytes = io.BytesIO(response.content)
                        cv_status = upload_resume_stream(ashby_id, file_bytes)

                    except Exception as e:
                        print(f"Resume error: {e}")

                notes_status = bool(candidate["notes"])
                tags_status = add_tags(ashby_id, candidate["tags"])

                log_candidate(manatal_id, ashby_id, cv_status, notes_status, tags_status)

                print(f"Migrated {manatal_id} → {ashby_id}")
                time.sleep(API_SLEEP)

            except Exception as e:
                print(f"Error {manatal_id}: {e}")
                log_candidate(manatal_id, "", False, False, False, str(e))

        page += 1