from typing import List, Dict, Any, Tuple
from pydantic import ValidationError
from core.schema import JobRecord
from core.constants import CAREER_FAMILIES


class ValidationIssue:
    def __init__(self, index: int, field: str, message: str, severity: str = "Error"):
        self.index = index
        self.field = field
        self.message = message
        self.severity = severity

    def to_dict(self):
        return {
            "Index": self.index,
            "Severity": self.severity,
            "Field": self.field,
            "Message": self.message
        }


def _canonicalize(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def validate_dataset(records_data: List[Dict[str, Any]]) -> Tuple[List[JobRecord], List[ValidationIssue]]:
    """
    Parses raw JSON dictionaries into JobRecords and validates them.
    Returns valid JobRecord objects and a list of issues found.
    """
    valid_records = []
    issues = []
    duplicate_keys = set()

    for idx, raw_data in enumerate(records_data):
        # 1. Schema Validation (Pydantic)
        try:
            record = JobRecord(**raw_data)
            valid_records.append(record)

            # 2. Logical/Enum Validation on the object

            # Required text fields should not be blank strings
            if not str(record.positionTitle).strip():
                issues.append(ValidationIssue(
                    idx, "positionTitle",
                    "Position Title is required and cannot be empty.",
                    "Error"
                ))

            if not str(record.department).strip():
                issues.append(ValidationIssue(
                    idx, "department",
                    "Department is required and cannot be empty.",
                    "Error"
                ))

            # Check Career Family
            if record.careerFamily not in CAREER_FAMILIES:
                issues.append(ValidationIssue(
                    idx, "careerFamily",
                    f"Unknown Career Family: '{record.careerFamily}'. Fallbacks will be used.",
                    "Warning"
                ))

            # Check Logic: Seniority vs Complexity (Example rule)
            if record.jobLevel and "Senior" in record.jobLevel:
                if record.position_complexity and "Entry" in record.position_complexity:
                    issues.append(ValidationIssue(
                        idx, "Logical Consistency",
                        f"Job Level is '{record.jobLevel}' but Complexity mentions 'Entry'.",
                        "Warning"
                    ))

            # Check for missing narrative fields that enhancement should populate
            for field_name in [
                "key_duties_responsibilities",
                "position_complexity",
                "organizational_impact",
                "career_progression_path",
            ]:
                value = getattr(record, field_name, None)
                if value is None or (isinstance(value, str) and not value.strip()):
                    issues.append(ValidationIssue(
                        idx, field_name,
                        "Field is empty; enhancement templates may be needed.",
                        "Warning"
                    ))

            # Duplicate detection across enriched key fields
            dup_key = (
                _canonicalize(record.positionTitle),
                _canonicalize(record.department),
                _canonicalize(record.careerFamily),
                _canonicalize(record.jobLevel),
                _canonicalize(record.key_duties_responsibilities)[:64],
            )
            if dup_key in duplicate_keys:
                issues.append(ValidationIssue(
                    idx, "Duplicate",
                    "Potential duplicate record detected (matches an earlier entry).",
                    "Warning"
                ))
            else:
                duplicate_keys.add(dup_key)

        except ValidationError as e:
            # Extract missing field names from Pydantic error
            for error in e.errors():
                # Handle cases where 'loc' might be empty or not straightforward
                loc_path = ".".join(str(x) for x in error.get('loc', []))
                msg = error.get('msg', 'Unknown error')
                issues.append(ValidationIssue(idx, loc_path, msg, "Error"))

            # Strategy: Keep raw data in UI, but valid_records only has good ones.
            pass

    return valid_records, issues
