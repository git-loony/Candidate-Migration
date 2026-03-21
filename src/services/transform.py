def map_candidate(manatal_candidate):
    return {
        "full_name": manatal_candidate.get("full_name"),
        "email": manatal_candidate.get("email"),
        "notes": build_notes(manatal_candidate),
        "tags": extract_tags(manatal_candidate),
        "resume_url": manatal_candidate.get("resume")
    }


def build_notes(c):
    """Combine useful fields into Ashby notes"""
    notes = []

    if c.get("current_company"):
        notes.append(f"Company: {c['current_company']}")

    if c.get("current_position"):
        notes.append(f"Position: {c['current_position']}")

    if c.get("latest_degree"):
        notes.append(f"Education: {c['latest_degree']} ({c.get('latest_university','')})")

    if c.get("description"):
        notes.append(f"Summary: {c['description']}")

    if c.get("phone_number"):
        notes.append(f"Phone: {c['phone_number']}")

    if c.get("custom_fields", {}).get("linkedin_url"):
        notes.append(f"LinkedIn: {c['custom_fields']['linkedin_url']}")

    return "\n".join(notes)


def extract_tags(c):
    tags = []

    if c.get("source_type"):
        tags.append(c["source_type"])

    if c.get("current_department"):
        tags.append(c["current_department"])

    skills = c.get("custom_fields", {}).get("skills", [])
    tags.extend(skills)

    return tags