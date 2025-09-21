# Import required dependencies
from dotenv import load_dotenv
from sqlalchemy import func, desc, or_
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, EmailStr, validator
from backend.db import Student, ActivityLog, SessionLocal
import logging
import re
import uuid

# Try to import function_tool, with fallback to handle import errors
try:
    from agents import function_tool
except ImportError as e:
    logging.error(f"Failed to import agents module: {str(e)}")
    raise ImportError("Ensure the 'agents' package is installed and correctly configured.")

# Import from pydentic_model.py
from ..utils.pydentic_model import (
    AddStudentRequest,
    GetStudentRequest, 
    UpdateStudentRequest,
    DeleteStudentRequest,
    ApiResponse, 
    student_to_response, 
    get_pkt_time,
    sanitize_input
)

load_dotenv()

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
# =============================================================================
# STUDENT MANAGEMENT TOOLS
# =============================================================================

@function_tool
def add_student(name: str, student_id: str, department: str, email: str) -> Dict[str, Any]:
    """Add a new student to the database
    
    Args:
        name: Full name of the student
        student_id: Unique student identifier
        department: Academic department
        email: Student's email address
    """
    request_id = str(uuid.uuid4())
    try:
        request = AddStudentRequest(name=name, student_id=student_id, department=department, email=email)
        logger.info(f"Agent request {request_id}: Adding student {request.student_id}")
        
        with SessionLocal() as db:
            existing_student = db.query(Student).filter(
                or_(Student.student_id == request.student_id, Student.email == request.email)
            ).first()
            
            if existing_student:
                return ApiResponse(
                    success=False,
                    message="Student with this ID or email already exists",
                    request_id=request_id
                ).dict()
            
            new_student = Student(
                name=request.name,
                student_id=request.student_id,
                department=request.department,
                email=request.email,
                created_at=get_pkt_time(),
                updated_at=get_pkt_time()
            )
            
            db.add(new_student)
            db.flush()
            
            activity = ActivityLog(
                student_id=request.student_id,
                activity_type="student_created",
                description=f"New student {request.name} added to {request.department}",
                timestamp=get_pkt_time()
            )
            db.add(activity)
            db.commit()
            
            return ApiResponse(
                success=True,
                message=f"Student {request.name} added successfully",
                    data={"student": student_to_response(new_student)},
                request_id=request_id
            ).dict()
    except ValueError as e:
        logger.error(f"Agent request {request_id}: Validation error adding student: {str(e)}")
        return ApiResponse(success=False, message=f"Validation error: {str(e)}", request_id=request_id).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error adding student: {str(e)}")
        return ApiResponse(success=False, message=f"Error adding student: {str(e)}", request_id=request_id).dict()

@function_tool
async def get_student(student_id: str) -> Dict[str, Any]:
    """Get student information by ID
    
    Args:
        student_id: Unique student identifier
    """
    request_id = str(uuid.uuid4())
    try:
        request = GetStudentRequest(student_id=student_id)
        logger.info(f"Agent request {request_id}: Retrieving student {request.student_id}")
        
        with SessionLocal() as db:
            student = db.query(Student).filter(Student.student_id == request.student_id).first()
            
            if not student:
                return ApiResponse(success=False, message="Student not found", request_id=request_id).dict()
            
            return ApiResponse(
                success=True,
                message="Student retrieved successfully",
                    data={"student": student_to_response(student)},
                request_id=request_id
            ).dict()
    except ValueError as e:
        logger.error(f"Agent request {request_id}: Validation error getting student: {str(e)}")
        return ApiResponse(success=False, message=f"Validation error: {str(e)}", request_id=request_id).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error getting student: {str(e)}")
        return ApiResponse(success=False, message=f"Error retrieving student: {str(e)}", request_id=request_id).dict()

@function_tool
async def update_student(student_id: str, field: str, new_value: str) -> Dict[str, Any]:
    """Update a specific field of a student
    
    Args:
        student_id: Unique student identifier
        field: Field to update (name, department, email, is_active)
        new_value: New value for the field
    """
    request_id = str(uuid.uuid4())
    try:
        request = UpdateStudentRequest(student_id=student_id, field=field, new_value=new_value)
        logger.info(f"Agent request {request_id}: Updating student {request.student_id}")
        
        with SessionLocal() as db:
            student = db.query(Student).filter(Student.student_id == request.student_id).first()
            
            if not student:
                return ApiResponse(success=False, message="Student not found", request_id=request_id).dict()
            
            if request.field == "is_active":
                request.new_value = request.new_value.lower() in ["true", "1", "yes", "active"]
            
            setattr(student, request.field, request.new_value)
            student.updated_at = get_pkt_time()
            
            activity = ActivityLog(
                student_id=request.student_id,
                activity_type="profile_update",
                description=f"Updated {request.field} to {request.new_value}",
                timestamp=get_pkt_time()
            )
            db.add(activity)
            db.commit()
            
            return ApiResponse(
                success=True,
                message=f"Student {request.student_id} updated successfully",
                data={"updated_field": request.field, "new_value": request.new_value},
                request_id=request_id
            ).dict()
    except ValueError as e:
        logger.error(f"Agent request {request_id}: Validation error updating student: {str(e)}")
        return ApiResponse(success=False, message=f"Validation error: {str(e)}", request_id=request_id).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error updating student: {str(e)}")
        return ApiResponse(success=False, message=f"Error updating student: {str(e)}", request_id=request_id).dict()

@function_tool
async def delete_student(student_id: str) -> Dict[str, Any]:
    """Delete a student from the database
    
    Args:
        student_id: Unique student identifier
    """
    request_id = str(uuid.uuid4())
    try:
        request = DeleteStudentRequest(student_id=student_id)
        logger.info(f"Agent request {request_id}: Deleting student {request.student_id}")
        
        with SessionLocal() as db:
            student = db.query(Student).filter(Student.student_id == request.student_id).first()
            
            if not student:
                return ApiResponse(success=False, message="Student not found", request_id=request_id).dict()
            
            student_name = student.name
            db.delete(student)
            
            activity = ActivityLog(
                student_id=request.student_id,
                activity_type="student_deleted",
                description=f"Student {student_name} deleted",
                timestamp=get_pkt_time()
            )
            db.add(activity)
            db.commit()
            
            return ApiResponse(
                success=True,
                message=f"Student {student_name} deleted successfully",
                request_id=request_id
            ).dict()
    except ValueError as e:
        logger.error(f"Agent request {request_id}: Validation error deleting student: {str(e)}")
        return ApiResponse(success=False, message=f"Validation error: {str(e)}", request_id=request_id).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error deleting student: {str(e)}")
        return ApiResponse(success=False, message=f"Error deleting student: {str(e)}", request_id=request_id).dict()

@function_tool
async def list_students() -> Dict[str, Any]:
    """Get list of all students"""
    request_id = str(uuid.uuid4())
    try:
        logger.info(f"Agent request {request_id}: Listing all students")
        with SessionLocal() as db:
            students = db.query(Student).all()
            student_list = [student_to_response(s) for s in students]
            return ApiResponse(
                success=True,
                message="List of all students retrieved successfully",
                data={"students": student_list, "total_count": len(student_list)},
                request_id=request_id
            ).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error listing students: {str(e)}")
        return ApiResponse(success=False, message=f"Error retrieving students: {str(e)}", request_id=request_id).dict()
