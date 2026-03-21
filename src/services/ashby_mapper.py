import uuid
from datetime import datetime


def generate_uuid():
    return str(uuid.uuid4())


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def map_to_ashby_format(candidate):
    """
    Convert internal candidate format → Ashby response format
    """

    candidate_id = generate_uuid()

    ashby_data = {
        "success": True,
        "results": {
            "id": candidate_id,
            "createdAt": now_iso(),
            "updatedAt": now_iso(),

            "name": candidate.get("full_name"),

            "primaryEmailAddress": {
                "value": candidate.get("email"),
                "type": "Work",
                "isPrimary": True
            },

            "emailAddresses": [
                {
                    "value": candidate.get("email"),
                    "type": "Work",
                    "isPrimary": True
                }
            ],

            "primaryPhoneNumber": None,
            "phoneNumbers": [],

            "socialLinks": build_social_links(candidate),

            "tags": build_tags(candidate),

            "position": extract_from_notes(candidate, "Position"),
            "company": extract_from_notes(candidate, "Company"),
            "school": extract_from_notes(candidate, "Education"),

            "applicationIds": [],

            "resumeFileHandle": build_resume(candidate),
            "fileHandles": [],

            "customFields": [],

            "profileUrl": None,

            "source": build_source(candidate),

            "creditedToUser": None,

            "timezone": None,

            "location": None
        }
    }

    return ashby_data


# -----------------------------
# HELPERS
# -----------------------------

def build_social_links(candidate):
    links = []
    notes = candidate.get("notes", "")

    for line in notes.split("\n"):
        if "linkedin.com" in line.lower():
            links.append({
                "url": line.split("LinkedIn:")[-1].strip(),
                "type": "LinkedIn"
            })

    return links


def build_tags(candidate):
    tags = []
    for tag in candidate.get("tags", []):
        tags.append({
            "id": generate_uuid(),
            "title": tag,
            "isArchived": False
        })
    return tags


def build_resume(candidate):
    if not candidate.get("resume_url"):
        return None

    return {
        "id": generate_uuid(),
        "name": "resume.pdf",
        "handle": "fake_handle_" + generate_uuid()
    }


def extract_from_notes(candidate, key):
    """
    Extract structured fields from notes
    Example: "Position: Engineer"
    """
    notes = candidate.get("notes", "")

    for line in notes.split("\n"):
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()

    return None


def build_source(candidate):
    if not candidate.get("tags"):
        return None

    return {
        "id": generate_uuid(),
        "title": candidate["tags"][0],
        "isArchived": False,
        "sourceType": {
            "id": generate_uuid(),
            "title": "Inbound",
            "isArchived": False
        }
    }