import pytest
from core.schema import JobRecord
from core.enhance import enhance_record, bulk_enhance
from core.validate import validate_dataset
from core.io import deduplicate_data


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


def test_bulk_enhance_counts(sample_record):
    sample_record.key_duties_responsibilities = None
    other = JobRecord(
        positionTitle="Analyst",
        department="Finance",
        careerFamily="Finance & Accounting",
        jobLevel="Senior",
        key_duties_responsibilities="Existing duties"
    )

    enhanced, count = bulk_enhance([sample_record, other])

    assert count == 2  # both records receive template fills for missing narrative fields
    assert enhanced[0].key_duties_responsibilities is not None
    assert enhanced[1].key_duties_responsibilities == "Existing duties"


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

    # One error for the second record (may appear after warnings for record 0)
    assert any(issue.index == 1 and issue.severity == "Error" for issue in issues)


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
    assert any(issue.severity == "Warning" for issue in issues)
    assert any("Unknown Career Family" in issue.message for issue in issues)


def test_validation_empty_fields_and_duplicates():
    data = [
        {
            "positionTitle": " ",
            "department": "",
            "careerFamily": "General",
            "key_duties_responsibilities": "",
        },
        {
            "positionTitle": "Developer",
            "department": "IT",
            "careerFamily": "Information Technology",
            "key_duties_responsibilities": "Build stuff",
        },
        {
            "positionTitle": "Developer",
            "department": "IT",
            "careerFamily": "Information Technology",
            "key_duties_responsibilities": "Build stuff",
        },
    ]

    valid, issues = validate_dataset(data)

    # First record should produce errors for blank required fields and warnings for missing narratives
    fields = {issue.field for issue in issues if issue.index == 0}
    assert "positionTitle" in fields
    assert "department" in fields
    assert "key_duties_responsibilities" in fields

    # Duplicate detection should flag the third record as a warning
    duplicate_warnings = [issue for issue in issues if issue.field == "Duplicate"]
    assert duplicate_warnings
    assert duplicate_warnings[0].severity == "Warning"


def test_deduplication_uses_richer_key():
    records = [
        {
            "positionTitle": "Advisor",
            "department": "Student Success",
            "careerFamily": "General",
            "jobLevel": "Senior",
            "key_duties_responsibilities": "Guide students",
        },
        {
            "positionTitle": "Advisor",
            "department": "Student Success",
            "careerFamily": "General",
            "jobLevel": "Junior",
            "key_duties_responsibilities": "Guide students",
        },
        {
            "positionTitle": "Advisor",
            "department": "Student Success",
            "careerFamily": "General",
            "jobLevel": "Senior",
            "key_duties_responsibilities": "Guide students",
        },
    ]

    unique_records = deduplicate_data(records)

    # Different job levels should not be merged, but identical records should be removed
    assert len(unique_records) == 2
    assert any(r["jobLevel"] == "Junior" for r in unique_records)
    assert any(r["jobLevel"] == "Senior" for r in unique_records)
