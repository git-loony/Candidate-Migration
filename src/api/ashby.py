import uuid
import os
import shutil

FAKE_DB = {
    "candidates": {}
}

RESUME_STORAGE = "resumes"
os.makedirs(RESUME_STORAGE, exist_ok=True)


def create_candidate(candidate):
    """Simulate creating a candidate in Ashby"""
    fake_id = str(uuid.uuid4())

    FAKE_DB["candidates"][fake_id] = {
        "id": fake_id,
        "full_name": candidate["full_name"],
        "email": candidate["email"],
        "notes": candidate["notes"],
        "tags": [],
        "resume": None
    }

    print(f"[FAKE ASHBY] Created candidate {fake_id}")
    return fake_id


def upload_resume(ashby_id, resume_file):
    """Simulate resume upload"""
    if not resume_file or ashby_id not in FAKE_DB["candidates"]:
        return False

    try:
        dest_path = os.path.join(RESUME_STORAGE, f"{ashby_id}.pdf")
        shutil.copy(resume_file, dest_path)

        FAKE_DB["candidates"][ashby_id]["resume"] = dest_path

        print(f"[FAKE ASHBY] Resume uploaded for {ashby_id}")
        return True

    except Exception as e:
        print(f"[FAKE ASHBY] Resume upload failed: {e}")
        return False


def add_tags(ashby_id, tags):
    """Simulate adding tags"""
    if ashby_id not in FAKE_DB["candidates"]:
        return False

    FAKE_DB["candidates"][ashby_id]["tags"].extend(tags)

    print(f"[FAKE ASHBY] Tags added to {ashby_id}: {tags}")
    return True


def get_all_candidates():
    """Inspect stored data"""
    return FAKE_DB["candidates"]