from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class JobRecord(BaseModel):
    positionTitle: str = Field(..., description="The title of the position")
    department: str = Field(..., description="The department the position belongs to")
    careerFamily: str = Field(..., description="The functional job family")
    jobLevel: Optional[str] = Field(default=None, description="Seniority level of the job")
    
    # Auto-filled fields
    key_duties_responsibilities: Optional[str] = Field(default=None)
    position_complexity: Optional[str] = Field(default=None)
    organizational_impact: Optional[str] = Field(default=None)
    career_progression_path: Optional[str] = Field(default=None)
    
    # Optional freeform fields
    minimum_qualifications: Optional[str] = Field(default=None)
    preferred_qualifications: Optional[str] = Field(default=None)
    technical_skills: Optional[str] = Field(default=None)
    soft_skills: Optional[str] = Field(default=None)
    FLSA_status: Optional[str] = Field(default=None)
    SOC_code: Optional[str] = Field(default=None)

    model_config = ConfigDict(extra="allow")  # Allow extra fields present in JSON but not in schema
