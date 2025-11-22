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
    Simple deduplication based on positionTitle + department.
    Keeps the first occurrence.
    """
    seen = set()
    unique_records = []
    for r in records:
        # Create a key. Handle potential missing keys safely if data is raw.
        key = (r.get('positionTitle', '').strip(), r.get('department', '').strip())
        if key not in seen:
            seen.add(key)
            unique_records.append(r)
    return unique_records