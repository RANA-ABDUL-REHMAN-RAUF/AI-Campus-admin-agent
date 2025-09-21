from fastapi import APIRouter

router = APIRouter()

@router.get("/students")
async def get_students():
    return {"message": "List of students"}

@router.post("/students")
async def create_student(student: dict):
    return {"message": "Student created", "student": student}

@router.get("/courses")
async def get_courses():
    return {"message": "List of courses"}

@router.post("/courses")
async def create_course(course: dict):
    return {"message": "Course created", "course": course}