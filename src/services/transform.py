def map_candidate(m):
    custom_fields = m.get("custom_fields", {})

    return {
        "full_name": m.get("full_name", "").strip(),
        "email": m.get("email"),
        "notes": m.get("description", ""),
        "tags": custom_fields.get("skills", []),
        "resume_url": m.get("resume")
    }