import time

from src.api.manatal import fetch_candidates_from_file, download_resume
from src.services.transform import map_candidate
from src.db.operations import log_candidate, get_last_processed_id
from src.config import API_SLEEP
from src.api.ashby import create_candidate, upload_resume, add_tags

from src.services.ashby_mapper import map_to_ashby_format
from src.utils.json_exporter import save_json


# Path to your JSON file
DATA_FILE = "data/candidates.json"


def migrate():
    last_processed = get_last_processed_id()
    page = 1
    per_page = 10

    print("🚀 Starting migration...")

    while True:
        candidates = fetch_candidates_from_file(DATA_FILE, page, per_page)

        if not candidates:
            print("✅ No more candidates.")
            break

        for m in candidates:
            manatal_id = m.get("id")

            # Skip already processed
            if last_processed and manatal_id <= last_processed:
                continue

            # -----------------------------
            # TRANSFORM DATA
            # -----------------------------
            candidate = map_candidate(m)

            try:
                # -----------------------------
                # CREATE IN ASHBY (FAKE/REAL)
                # -----------------------------
                ashby_id = create_candidate(candidate)

                # -----------------------------
                # RESUME UPLOAD
                # -----------------------------
                cv_status = False
                if candidate.get("resume_url"):
                    resume_file = download_resume(candidate["resume_url"], manatal_id)
                    cv_status = upload_resume(ashby_id, resume_file)

                # -----------------------------
                # TAGS
                # -----------------------------
                notes_status = bool(candidate.get("notes"))
                tags_status = add_tags(ashby_id, candidate.get("tags", []))

                # -----------------------------
                # SAVE LOG TO DB
                # -----------------------------
                log_candidate(
                    manatal_id,
                    ashby_id,
                    cv_status,
                    notes_status,
                    tags_status
                )

                # -----------------------------
                # GENERATE ASHBY JSON OUTPUT
                # -----------------------------
                ashby_json = map_to_ashby_format(candidate)

                # Save JSON for verification
                save_json(ashby_json, f"candidate_{manatal_id}.json")

                print(f"✅ Migrated {manatal_id} → {ashby_id}")

                time.sleep(API_SLEEP)

            except Exception as e:
                print(f"❌ Error migrating {manatal_id}: {e}")

                log_candidate(
                    manatal_id,
                    "",
                    False,
                    False,
                    False,
                    str(e)
                )

        page += 1

    print("🎉 Migration completed.")