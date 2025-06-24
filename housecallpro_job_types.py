#!/usr/bin/env python3
"""
Housecall Pro Job Types MCP Server

This server provides job type management functionality for Housecall Pro,
including CRUD operations for job types.
"""

import os
from typing import Optional, Dict, Any, List
import json

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Job Types")

# Configuration
API_KEY = os.getenv("HOUSECALL_PRO_API_KEY")
API_BASE_URL = "https://api.housecallpro.com"

if not API_KEY:
    raise ValueError("HOUSECALL_PRO_API_KEY environment variable is required")


def get_headers() -> Dict[str, str]:
    """Get headers for API requests."""
    return {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def make_api_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Make an API request to Housecall Pro."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = get_headers()
    
    with httpx.Client() as client:
        response = client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_job_types(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    active: Optional[bool] = None,
    name: Optional[str] = None
) -> str:
    """
    Retrieve job types from Housecall Pro.
    
    This endpoint returns a list of job types configured in your Housecall Pro account,
    which can be used when creating jobs to categorize the type of work being performed.
    
    Args:
        page: Page number for pagination (optional)
        page_size: Number of results per page (optional, typically 1-100)
        sort_by: Field to sort by (e.g., 'name', 'created_at') (optional)
        sort_direction: Sort direction ('asc' or 'desc') (optional)
        active: Filter by active status (true/false) (optional)
        name: Filter by job type name (partial match) (optional)
    
    Returns:
        JSON string containing the list of job types
    """
    params = {}
    
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if sort_by:
        params["sort_by"] = sort_by
    if sort_direction:
        params["sort_direction"] = sort_direction
    if active is not None:
        params["active"] = str(active).lower()
    if name:
        params["name"] = name
    
    try:
        result = make_api_request("GET", "/job_types", params=params)
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return json.dumps({"error": "Unauthorized - check your API credentials"}, indent=2)
        elif e.response.status_code == 403:
            return json.dumps({"error": "Access denied - insufficient permissions"}, indent=2)
        else:
            return json.dumps({"error": f"Error getting job types: {e.response.status_code} - {e.response.text}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting job types: {str(e)}"}, indent=2)


@mcp.tool()
async def create_job_type(
    name: str,
    color: Optional[str] = None,
    description: Optional[str] = None,
    active: Optional[bool] = True,
    default_duration_hours: Optional[float] = None,
    requires_technician: Optional[bool] = None,
    default_price: Optional[float] = None
) -> str:
    """
    Create a new job type in Housecall Pro.
    
    This endpoint allows you to create a new job type that can be used when
    creating jobs to categorize the type of work being performed.
    
    Args:
        name: Name of the job type (required)
        color: Hex color code for the job type (e.g., '#FF0000') (optional)
        description: Description of the job type (optional)
        active: Whether the job type is active (default: true) (optional)
        default_duration_hours: Default duration in hours for jobs of this type (optional)
        requires_technician: Whether jobs of this type require a technician (optional)
        default_price: Default price for jobs of this type (optional)
    
    Returns:
        JSON string containing the created job type details
    """
    data = {"name": name}
    
    if color is not None:
        data["color"] = color
    if description is not None:
        data["description"] = description
    if active is not None:
        data["active"] = active
    if default_duration_hours is not None:
        data["default_duration_hours"] = default_duration_hours
    if requires_technician is not None:
        data["requires_technician"] = requires_technician
    if default_price is not None:
        data["default_price"] = default_price
    
    try:
        result = make_api_request("POST", "/job_types", json_data=data)
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return json.dumps({"error": f"Bad request - check your input data: {e.response.text}"}, indent=2)
        elif e.response.status_code == 401:
            return json.dumps({"error": "Unauthorized - check your API credentials"}, indent=2)
        elif e.response.status_code == 403:
            return json.dumps({"error": "Access denied - insufficient permissions"}, indent=2)
        elif e.response.status_code == 409:
            return json.dumps({"error": f"Job type with name '{name}' already exists"}, indent=2)
        else:
            return json.dumps({"error": f"Error creating job type: {e.response.status_code} - {e.response.text}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error creating job type: {str(e)}"}, indent=2)


@mcp.tool()
async def update_job_type(
    job_type_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    description: Optional[str] = None,
    active: Optional[bool] = None,
    default_duration_hours: Optional[float] = None,
    requires_technician: Optional[bool] = None,
    default_price: Optional[float] = None
) -> str:
    """
    Update an existing job type in Housecall Pro.
    
    This endpoint allows you to modify the properties of an existing job type.
    Only the fields you provide will be updated; others will remain unchanged.
    
    Args:
        job_type_id: ID of the job type to update (required)
        name: Updated name of the job type (optional)
        color: Updated hex color code for the job type (e.g., '#FF0000') (optional)
        description: Updated description of the job type (optional)
        active: Updated active status (optional)
        default_duration_hours: Updated default duration in hours (optional)
        requires_technician: Updated technician requirement (optional)
        default_price: Updated default price (optional)
    
    Returns:
        JSON string containing the updated job type details
    """
    data = {}
    
    if name is not None:
        data["name"] = name
    if color is not None:
        data["color"] = color
    if description is not None:
        data["description"] = description
    if active is not None:
        data["active"] = active
    if default_duration_hours is not None:
        data["default_duration_hours"] = default_duration_hours
    if requires_technician is not None:
        data["requires_technician"] = requires_technician
    if default_price is not None:
        data["default_price"] = default_price
    
    if not data:
        return "Error: No fields provided to update"
    
    try:
        result = make_api_request("PUT", f"/job_types/{job_type_id}", json_data=data)
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return f"Error: Bad request - check your input data: {e.response.text}"
        elif e.response.status_code == 401:
            return "Error: Unauthorized - check your API credentials"
        elif e.response.status_code == 403:
            return "Error: Access denied - insufficient permissions"
        elif e.response.status_code == 404:
            return f"Error: Job type with ID '{job_type_id}' not found"
        elif e.response.status_code == 409:
            return f"Error: Conflict - job type name may already exist"
        else:
            return f"Error updating job type: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error updating job type: {str(e)}"


@mcp.tool()
async def get_job_type_by_id(job_type_id: str) -> str:
    """
    Retrieve a specific job type by its ID.
    
    Args:
        job_type_id: The ID of the job type to retrieve (required)
    
    Returns:
        JSON string containing the job type details
    """
    try:
        result = make_api_request("GET", f"/job_types/{job_type_id}")
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Job type with ID '{job_type_id}' not found"
        elif e.response.status_code == 401:
            return "Error: Unauthorized - check your API credentials"
        elif e.response.status_code == 403:
            return "Error: Access denied - insufficient permissions"
        else:
            return f"Error getting job type: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error getting job type: {str(e)}"


if __name__ == "__main__":
    import asyncio
    mcp.run() 