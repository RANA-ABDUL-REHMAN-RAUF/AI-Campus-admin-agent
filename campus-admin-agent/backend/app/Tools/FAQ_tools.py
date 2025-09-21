# Import required dependencies
from typing import Dict, Any, Optional
import uuid
import logging

# Try to import function_tool and ApiResponse, with fallback to handle import errors
try:
    from agents import function_tool
except ImportError as e:
    logging.error(f"Failed to import agents module: {str(e)}")
    raise ImportError("Ensure the 'agents' package is installed and correctly configured.")

# Configure logging
logger = logging.getLogger(__name__)

# Import ApiResponse from pydentic_model.py
try:
    from ..utils.pydentic_model import ApiResponse
except ImportError:
    # Fallback: define ApiResponse locally if import fails
    from pydantic import BaseModel, Field
    
    class ApiResponse(BaseModel):
        """Standard API response format for agent consumption"""
        success: bool = Field(..., description="Operation success status")
        message: str = Field(..., description="Response message")
        data: Optional[Dict[str, Any]] = Field(None, description="Response data")
        request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request identifier")

# =============================================================================
# CAMPUS FAQ TOOLS
# =============================================================================
@function_tool
async def get_library_name() -> Dict[str, Any]:
    """Get the name of the campus library"""
    request_id = str(uuid.uuid4())
    logger.info(f"Agent request {request_id}: Getting library name")
    return ApiResponse(
        success=True,
        message="Library name retrieved successfully",
        data={"library_name": "Saylani Library"},
        request_id=request_id
    ).dict()

@function_tool
async def get_cafeteria_name() -> Dict[str, Any]:
    """Get the name of the campus cafeteria"""
    request_id = str(uuid.uuid4())
    logger.info(f"Agent request {request_id}: Getting cafeteria name")
    return ApiResponse(
        success=True,
        message="Cafeteria name retrieved successfully",
        data={"cafeteria_name": "Campus Cafeteria"},
        request_id=request_id
    ).dict()
# =============================================================================

@function_tool
async def get_cafeteria_timings() -> Dict[str, Any]:
    """Get cafeteria operating hours"""
    request_id = str(uuid.uuid4())
    logger.info(f"Agent request {request_id}: Getting cafeteria timings")
    return ApiResponse(
        success=True,
        message="Cafeteria timings retrieved successfully. The cafeteria name is 'Campus Cafeteria'.",
        data={
            "cafeteria_timings": {
                "campus_name": "Saylani Campus",
                "cafeteria_name": "Campus Cafeteria",
                "hours": "8:00 AM - 8:00 PM",
                "breakfast": "7:00 AM - 10:00 AM",
                "lunch": "11:30 AM - 2:30 PM",
                "dinner": "6:00 PM - 9:00 PM",
                "weekend_hours": "10:00 AM - 8:00 PM"
            }
        },
        request_id=request_id
    ).dict()

@function_tool
async def get_library_hours() -> Dict[str, Any]:
    """Get library operating hours"""
    request_id = str(uuid.uuid4())
    logger.info(f"Agent request {request_id}: Getting library hours")
    return ApiResponse(
        success=True,
        message="Library hours retrieved successfully. The library name is 'Saylani Library'.",
        data={
            "library_hours": {
                "campus_name": "Saylani Campus",
                "library_name": "Saylani Library",
                "monday_friday": "8:00 AM - 10:00 PM",
                "saturday": "9:00 AM - 8:00 PM",
                "sunday": "10:00 AM - 6:00 PM",
                "study_rooms": "24/7 access with student ID"
            }
        },
        request_id=request_id
    ).dict()

@function_tool
async def get_lunch_timing() -> Dict[str, Any]:
    """Get lunch timing information specifically"""
    request_id = str(uuid.uuid4())
    logger.info(f"Agent request {request_id}: Getting lunch timing")
    return ApiResponse(
        success=True,
        message="Lunch timing retrieved successfully",
        data={
            "lunch_timing": {
                "campus_name": "Saylani Campus",
                "lunch_hours": "11:30 AM - 2:30 PM",
                "service_type": "Lunch Service",
                "days": "Monday - Friday",
                "weekend_lunch": "Available during weekend cafeteria hours"
            }
        },
        request_id=request_id
    ).dict()

