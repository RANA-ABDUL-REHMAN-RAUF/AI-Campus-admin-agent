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
    RecentStudentsRequest, 
    ApiResponse, 
    student_to_response, 
    get_pkt_time
)

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('campus_analytics_tools.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# CAMPUS ANALYTICS TOOLS
# =============================================================================

@function_tool
async def get_total_students() -> Dict[str, Any]:
    """Get total number of students with active/inactive breakdown"""
    request_id = str(uuid.uuid4())
    try:
        logger.info(f"Agent request {request_id}: Getting total student count")
        with SessionLocal() as db:
            total = db.query(Student).count()
            active = db.query(Student).filter(Student.is_active == True).count()
            
            return ApiResponse(
                success=True,
                message="Student count retrieved successfully",
                data={
                    "total_students": total,
                    "active_students": active,
                    "inactive_students": total - active
                },
                request_id=request_id
            ).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error getting student count: {str(e)}")
        return ApiResponse(success=False, message=f"Error getting student count: {str(e)}", request_id=request_id).dict()

@function_tool
async def get_students_by_department() -> Dict[str, Any]:
    """Get student count grouped by department"""
    request_id = str(uuid.uuid4())
    try:
        logger.info(f"Agent request {request_id}: Getting student count by department")
        with SessionLocal() as db:
            dept_counts = db.query(
                Student.department,
                func.count(Student.id).label('count')
            ).group_by(Student.department).all()
            
            department_data = [{"department": dept, "count": count} for dept, count in dept_counts]
            
            return ApiResponse(
                success=True,
                message="Department counts retrieved successfully",
                data={"departments": department_data},
                request_id=request_id
            ).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error getting department data: {str(e)}")
        return ApiResponse(success=False, message=f"Error getting department data: {str(e)}", request_id=request_id).dict()

@function_tool
async def get_recent_onboarded_students(limit: int = 5) -> Dict[str, Any]:
    """Get recently onboarded students
    
    Args:
        limit: Maximum number of recent students to return (default: 5)
    """
    request_id = str(uuid.uuid4())
    try:
        request = RecentStudentsRequest(limit=limit)
        logger.info(f"Agent request {request_id}: Getting recent students (limit: {request.limit})")
        
        with SessionLocal() as db:
            recent_students = db.query(Student).order_by(
                desc(Student.created_at)
            ).limit(request.limit).all()
            students = [student_to_response(s) for s in recent_students]
            return ApiResponse(
                success=True,
                message="Recent students retrieved successfully",
                data={"recent_students": students, "limit": request.limit},
                request_id=request_id
            ).dict()
    except ValueError as e:
        logger.error(f"Agent request {request_id}: Validation error getting recent students: {str(e)}")
        return ApiResponse(success=False, message=f"Validation error: {str(e)}", request_id=request_id).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error getting recent students: {str(e)}")
        return ApiResponse(success=False, message=f"Error getting recent students: {str(e)}", request_id=request_id).dict()

@function_tool
async def get_active_students_last_7_days() -> Dict[str, Any]:
    """Get students who were active in the last 7 days (based on activity logs)"""
    request_id = str(uuid.uuid4())
    try:
        logger.info(f"Agent request {request_id}: Getting active students for last 7 days")
        with SessionLocal() as db:
            seven_days_ago = get_pkt_time() - timedelta(days=7)
            
            active_students = db.query(ActivityLog.student_id).filter(
                ActivityLog.timestamp >= seven_days_ago
            ).distinct().all()
            
            student_ids = [student[0] for student in active_students]
            
            students = db.query(Student).filter(
                Student.student_id.in_(student_ids)
            ).all()
            
            student_list = [student_to_response(s) for s in students]
            return ApiResponse(
                success=True,
                message="Active students retrieved successfully",
                data={
                    "active_students": student_list,
                    "count": len(student_list),
                    "period": "last_7_days"
                },
                request_id=request_id
            ).dict()
    except Exception as e:
        logger.error(f"Agent request {request_id}: Error getting active students: {str(e)}")
        return ApiResponse(success=False, message=f"Error getting active students: {str(e)}", request_id=request_id).dict()

