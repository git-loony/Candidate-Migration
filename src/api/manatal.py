from src.config import MOCK_MODE

def fetch_candidates(page=1):
    if MOCK_MODE:
        if page > 3:
            return []

        return [
            {
                "id": page * 10 + i,
                "full_name": f"Test User {i}",
                "email": f"user{i}@test.com",
                "description": "Mock candidate",
                "resume": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "custom_fields": {
                    "skills": ["Python", "SQL"]
                }
            }
            for i in range(5)
        ]

    import requests
    from src.config import MANATAL_API_KEY, PER_PAGE

    url = f"https://api.manatal.com/open/v3/candidates?page={page}&per_page={PER_PAGE}"
    headers = {"Authorization": f"Bearer {MANATAL_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()