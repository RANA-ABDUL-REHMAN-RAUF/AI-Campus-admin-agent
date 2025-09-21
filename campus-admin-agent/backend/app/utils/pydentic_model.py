from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr, validator
import logging
import re
import uuid

load_dotenv()

def student_to_response(student):
    return {
        "id": student.id,
        "student_id": student.student_id,
        "name": student.name,
        "department": student.department,
        "email": student.email,
        "is_active": student.is_active,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None,
    }

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('student_management_tools.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# PKT timezone (UTC+5)
PKT_OFFSET = timedelta(hours=5)
def get_pkt_time():
    """Get current time in PKT (UTC+5)"""
    return datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(PKT_OFFSET))

# Fix database session management - remove async context manager that conflicts with sync operations
# Input sanitization helper
def sanitize_input(value: str) -> str:
    """Sanitize input strings to prevent injection attacks"""
    if not isinstance(value, str):
        return value
    value = re.sub(r'[<>;{}]', '', value)
    return ' '.join(value.strip().split())

# =============================================================================
# PYDANTIC VALIDATION MODELS
# =============================================================================

class AddStudentRequest(BaseModel):
    """Validation model for adding a new student"""
    name: str = Field(..., min_length=2, max_length=100, description="Student's full name")
    student_id: str = Field(..., min_length=3, max_length=50, description="Unique student identifier")
    department: str = Field(..., min_length=2, max_length=100, description="Academic department")
    email: EmailStr = Field(..., description="Student's email address")
    
    @validator('name')
    def validate_name(cls, v):
        v = sanitize_input(v)
        if not v:
            raise ValueError('Name cannot be empty')
        return v.title()
    
    @validator('student_id')
    def validate_student_id(cls, v):
        v = sanitize_input(v)
        if not v or not re.match(r'^[A-Za-z0-9_-]+$', v):
            raise ValueError('Invalid student ID format')
        return v.upper()
    
    @validator('department')
    def validate_department(cls, v):
        v = sanitize_input(v)
        if not v:
            raise ValueError('Department cannot be empty')
        return v.title()

class GetStudentRequest(BaseModel):
    """Validation model for retrieving student information"""
    student_id: str = Field(..., min_length=3, max_length=50, description="Unique student identifier")
    
    @validator('student_id')
    def validate_student_id(cls, v):
        v = sanitize_input(v)
        if not v:
            raise ValueError('Student ID cannot be empty')
        return v.upper()

class UpdateStudentRequest(BaseModel):
    """Validation model for updating student information"""
    student_id: str = Field(..., min_length=3, max_length=50, description="Unique student identifier")
    field: str = Field(..., description="Field to update (name, department, email, is_active)")
    new_value: str = Field(..., description="New value for the field")
    
    @validator('student_id')
    def validate_student_id(cls, v):
        v = sanitize_input(v)
        if not v:
            raise ValueError('Student ID cannot be empty')
        return v.upper()
    
    @validator('field')
    def validate_field(cls, v):
        valid_fields = ["name", "department", "email", "is_active"]
        if v not in valid_fields:
            raise ValueError(f'Invalid field. Valid fields: {valid_fields}')
        return v
    
    @validator('new_value')
    def validate_new_value(cls, v, values):
        v = sanitize_input(v)
        if 'field' in values:
            field = values['field']
            if field == 'name' and len(v) < 2:
                raise ValueError('Name must be at least 2 characters')
            elif field == 'department' and len(v) < 2:
                raise ValueError('Department must be at least 2 characters')
            elif field == 'email' and '@' not in v:
                raise ValueError('Invalid email format')
        return v

class DeleteStudentRequest(BaseModel):
    """Validation model for deleting a student"""
    student_id: str = Field(..., min_length=3, max_length=50, description="Unique student identifier")
    
    @validator('student_id')
    def validate_student_id(cls, v):
        v = sanitize_input(v)
        if not v:
            raise ValueError('Student ID cannot be empty')
        return v.upper()

class RecentStudentsRequest(BaseModel):
    """Validation model for getting recent students"""
    limit: int = Field(default=5, ge=1, le=100, description="Maximum number of students to return")

class StudentResponse(BaseModel):
    """Response model for student data"""
    id: int = Field(..., description="Database ID")
    student_id: str = Field(..., description="Unique student identifier")
    name: str = Field(..., description="Student's full name")
    department: str = Field(..., description="Academic department")
    email: str = Field(..., description="Student's email")
    is_active: Optional[bool] = Field(None, description="Active status")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")

class ApiResponse(BaseModel):
    """Standard API response format for agent consumption"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")

