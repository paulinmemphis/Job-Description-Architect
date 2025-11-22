import pytest
from core.schema import JobRecord
from core.enhance import enhance_record
from core.validate import validate_dataset

@pytest.fixture
def sample_record():
    return JobRecord(
        positionTitle="Manager",
        department="HR",
        careerFamily="Leadership & Management",
        jobLevel="Director"
    )

def test_enhancement_fills_missing(sample_record):
    # Ensure fields are empty initially
    assert sample_record.key_duties_responsibilities is None
    
    enhanced, changed = enhance_record(sample_record)
    
    # Should be changed
    assert changed is True
    # Should contain leadership keywords
    assert "strategic leadership" in enhanced.key_duties_responsibilities
    assert "policies, procedures" in enhanced.key_duties_responsibilities

def test_enhancement_idempotency(sample_record):
    # First run
    enhanced_once, _ = enhance_record(sample_record)
    
    # Second run on the ALREADY enhanced record
    enhanced_twice, changed = enhance_record(enhanced_once)
    
    # Should NOT change
    assert changed is False
    assert enhanced_once.key_duties_responsibilities == enhanced_twice.key_duties_responsibilities

def test_validation_schema():
    data = [
        {
            "positionTitle": "Dev",
            "department": "IT",
            "careerFamily": "Information Technology"
        },
        {
            "positionTitle": "Bad Rec",
            # Missing department
            "careerFamily": "General"
        }
    ]
    
    valid, issues = validate_dataset(data)
    
    # One valid record
    assert len(valid) == 1
    assert valid[0].positionTitle == "Dev"
    
    # One error for the second record
    assert len(issues) >= 1
    assert issues[0].index == 1
    assert issues[0].severity == "Error"

def test_validation_logic():
    data = [{
        "positionTitle": "Boss",
        "department": "Ops",
        "careerFamily": "Unknown Family 123"
    }]
    
    valid, issues = validate_dataset(data)
    # It passes schema, so it is in valid list
    assert len(valid) == 1
    # But it generates a Warning issue
    assert len(issues) == 1
    assert issues[0].severity == "Warning"
    assert "Unknown Career Family" in issues[0].message