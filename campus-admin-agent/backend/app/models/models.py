from pydantic import BaseModel
from typing import List, Optional

class Student(BaseModel):
    id: int
    name: str
    email: str
    enrolled_courses: List[str]

class Course(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    credits: int

class Faculty(BaseModel):
    id: int
    name: str
    department: str
    email: str

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    semester: str
    grade: Optional[str] = None