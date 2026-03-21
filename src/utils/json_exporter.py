import json
import os


def save_json(data, filename):
    os.makedirs("output", exist_ok=True)

    path = os.path.join("output", filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved JSON → {path}")