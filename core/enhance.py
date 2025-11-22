from typing import List, Tuple
import copy
from core.schema import JobRecord
from core.constants import (
    DUTIES_TEMPLATES,
    COMPLEXITY_TEMPLATES,
    IMPACT_TEMPLATES,
    PROGRESSION_TEMPLATES,
    FALLBACK_DUTIES,
    FALLBACK_COMPLEXITY,
    FALLBACK_IMPACT,
    FALLBACK_PROGRESSION
)

def needs_filling(value: str | None) -> bool:
    """Returns True if the value is None, empty, or whitespace only."""
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False

def get_family_value(template_map: dict, family: str, default: str) -> str:
    """Retrieves value from map based on family, or returns default."""
    return template_map.get(family, default)

def enhance_record(record: JobRecord) -> Tuple[JobRecord, bool]:
    """
    Fills missing fields in a JobRecord based on its careerFamily.
    Returns a tuple of (enhanced_record, changed_bool).
    """
    # Create a copy to avoid mutating the original in place immediately
    # (though Pydantic models are mutable by default, treating as immutable here helps tracking)
    new_record = record.model_copy()
    changed = False
    family = new_record.careerFamily

    # 1. Duties
    if needs_filling(new_record.key_duties_responsibilities):
        new_record.key_duties_responsibilities = get_family_value(DUTIES_TEMPLATES, family, FALLBACK_DUTIES)
        changed = True

    # 2. Complexity
    if needs_filling(new_record.position_complexity):
        new_record.position_complexity = get_family_value(COMPLEXITY_TEMPLATES, family, FALLBACK_COMPLEXITY)
        changed = True

    # 3. Impact
    if needs_filling(new_record.organizational_impact):
        new_record.organizational_impact = get_family_value(IMPACT_TEMPLATES, family, FALLBACK_IMPACT)
        changed = True

    # 4. Progression
    if needs_filling(new_record.career_progression_path):
        new_record.career_progression_path = get_family_value(PROGRESSION_TEMPLATES, family, FALLBACK_PROGRESSION)
        changed = True

    return new_record, changed

def bulk_enhance(records: List[JobRecord]) -> Tuple[List[JobRecord], int]:
    """
    Enhances a list of records.
    Returns (list of enhanced records, count of records modified).
    """
    enhanced_list = []
    modified_count = 0
    
    for rec in records:
        enhanced_rec, changed = enhance_record(rec)
        enhanced_list.append(enhanced_rec)
        if changed:
            modified_count += 1
            
    return enhanced_list, modified_count