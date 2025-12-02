import json
from typing import List, Dict, Any
from datetime import datetime


def load_json(file_obj) -> List[Dict[str, Any]]:
    """Loads JSON from a file-like object."""
    try:
        data = json.load(file_obj)
        if not isinstance(data, list):
            raise ValueError("Top-level JSON element must be an array/list.")
        return data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file format.")


def save_json_str(records: List[Dict[str, Any]]) -> str:
    """Dumps records to a formatted JSON string."""
    return json.dumps(records, indent=2, ensure_ascii=False)


def generate_changelog(changes: List[Dict[str, Any]]) -> str:
    """Generates a JSON string for the changelog."""
    return json.dumps(changes, indent=2, ensure_ascii=False)


def deduplicate_data(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicate records using a richer identity key to reduce false positives.

    Key components:
    - positionTitle
    - department
    - careerFamily
    - jobLevel
    - a short hash of duties text (if present)

    Keeps the first occurrence of each unique key.
    """
    seen = set()
    unique_records = []

    def canonicalize(value: Any) -> str:
        return str(value).strip().lower() if value is not None else ""

    for r in records:
        duties = canonicalize(r.get("key_duties_responsibilities"))
        duties_hash = duties[:64]  # lightweight signature to distinguish similar titles

        key = (
            canonicalize(r.get("positionTitle")),
            canonicalize(r.get("department")),
            canonicalize(r.get("careerFamily")),
            canonicalize(r.get("jobLevel")),
            duties_hash,
        )

        if key not in seen:
            seen.add(key)
            unique_records.append(r)

    return unique_records
