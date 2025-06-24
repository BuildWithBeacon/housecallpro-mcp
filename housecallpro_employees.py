#!/usr/bin/env python3
"""
Housecall Pro Employees MCP Server

This server provides employee management functionality for Housecall Pro,
including CRUD operations for employees.
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
mcp = FastMCP("Housecall Pro Employees")

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


async def make_api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an API request to Housecall Pro."""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=get_headers(),
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return json.dumps({"error": f"HTTP error occurred: {str(e)}"}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"}, indent=2)

# Employee Management Tools

@mcp.tool()
async def get_employees(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    tag_ids: Optional[str] = None,
    employee_type: Optional[str] = None,
    mobile_user: Optional[bool] = None,
    include_tags: Optional[bool] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of employees from Housecall Pro.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of employees per page (max 100, default: 50)
        role: Filter by employee role
        is_active: Filter by active status (true/false)
        tag_ids: Comma-separated list of tag IDs to filter by
        employee_type: Filter by employee type
        mobile_user: Filter by mobile user status (true/false)
        include_tags: Include employee tags in response (true/false)
        sort_by: Field to sort by (e.g., 'first_name', 'last_name', 'email')
        sort_direction: Sort direction ('asc' or 'desc')
    
    Returns:
        List of employees with their details including names, roles, contact info, and status.
    """
    
    params = {}
    
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = min(page_size, 100)  # API max is 100
    if role is not None:
        params["role"] = role
    if is_active is not None:
        params["is_active"] = str(is_active).lower()
    if tag_ids is not None:
        params["tag_ids"] = tag_ids
    if employee_type is not None:
        params["employee_type"] = employee_type
    if mobile_user is not None:
        params["mobile_user"] = str(mobile_user).lower()
    if include_tags is not None:
        params["include_tags"] = str(include_tags).lower()
    if sort_by is not None:
        params["sort_by"] = sort_by
    if sort_direction is not None:
        params["sort_direction"] = sort_direction

    return await make_api_request("GET", "employees", params=params)

@mcp.tool()
async def get_employee_by_id(
    employee_id: str,
    include_tags: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get a specific employee by their ID.
    
    Args:
        employee_id: The unique ID of the employee
        include_tags: Include employee tags in response (true/false)
    
    Returns:
        Employee details including personal info, role, contact details, and employment status.
    """
    
    params = {}
    if include_tags is not None:
        params["include_tags"] = str(include_tags).lower()
    
    return await make_api_request("GET", f"employees/{employee_id}", params=params)

@mcp.tool()
async def search_employees(
    search_term: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    is_active: Optional[bool] = None,
    include_tags: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search employees by name, email, or phone number.
    
    Args:
        search_term: Search term to find employees (searches name, email, phone)
        page: Page number for pagination (default: 1)
        page_size: Number of employees per page (max 100, default: 50)
        is_active: Filter by active status (true/false)
        include_tags: Include employee tags in response (true/false)
    
    Returns:
        List of employees matching the search criteria.
    """
    
    params = {"search": search_term}
    
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = min(page_size, 100)
    if is_active is not None:
        params["is_active"] = str(is_active).lower()
    if include_tags is not None:
        params["include_tags"] = str(include_tags).lower()

    return await make_api_request("GET", "employees", params=params)

@mcp.tool()
async def get_employees_by_role(
    role: str,
    is_active: Optional[bool] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get employees filtered by their role.
    
    Args:
        role: Employee role to filter by (e.g., 'technician', 'admin', 'manager')
        is_active: Filter by active status (true/false)
        page: Page number for pagination (default: 1)
        page_size: Number of employees per page (max 100, default: 50)
    
    Returns:
        List of employees with the specified role.
    """
    
    params = {"role": role}
    
    if is_active is not None:
        params["is_active"] = str(is_active).lower()
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = min(page_size, 100)

    return await make_api_request("GET", "employees", params=params)

@mcp.tool()
async def get_active_employees(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    include_tags: Optional[bool] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get only active employees.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of employees per page (max 100, default: 50)
        include_tags: Include employee tags in response (true/false)
        sort_by: Field to sort by (e.g., 'first_name', 'last_name', 'email')
        sort_direction: Sort direction ('asc' or 'desc')
    
    Returns:
        List of active employees.
    """
    
    params = {"is_active": "true"}
    
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = min(page_size, 100)
    if include_tags is not None:
        params["include_tags"] = str(include_tags).lower()
    if sort_by is not None:
        params["sort_by"] = sort_by
    if sort_direction is not None:
        params["sort_direction"] = sort_direction

    return await make_api_request("GET", "employees", params=params)

@mcp.tool()
async def get_mobile_employees(
    is_active: Optional[bool] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get employees who are mobile users.
    
    Args:
        is_active: Filter by active status (true/false)
        page: Page number for pagination (default: 1)
        page_size: Number of employees per page (max 100, default: 50)
    
    Returns:
        List of employees who are mobile users.
    """
    
    params = {"mobile_user": "true"}
    
    if is_active is not None:
        params["is_active"] = str(is_active).lower()
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = min(page_size, 100)

    return await make_api_request("GET", "employees", params=params)

@mcp.tool()
async def summarize_employees() -> str:
    """
    Get a summary of all employees including counts by role and status.
    
    Returns:
        A human-readable summary of employees including total count, active/inactive breakdown, and role distribution.
    """
    
    try:
        # Get all employees with minimal pagination
        response = await make_api_request("GET", "employees", params={"page_size": 100})
        
        if "error" in response:
            return f"Error fetching employees: {response.get('message', 'Unknown error')}"
        
        employees = response.get("employees", [])
        total_count = len(employees)
        
        if total_count == 0:
            return "No employees found."
        
        # Count by status
        active_count = sum(1 for emp in employees if emp.get("is_active", False))
        inactive_count = total_count - active_count
        
        # Count by role
        role_counts = {}
        mobile_users = 0
        
        for emp in employees:
            role = emp.get("role", "Unknown")
            role_counts[role] = role_counts.get(role, 0) + 1
            
            if emp.get("mobile_user", False):
                mobile_users += 1
        
        # Build summary
        summary = f"Employee Summary:\\n"
        summary += f"Total Employees: {total_count}\\n"
        summary += f"Active: {active_count} | Inactive: {inactive_count}\\n"
        summary += f"Mobile Users: {mobile_users}\\n\\n"
        
        if role_counts:
            summary += "Employees by Role:\\n"
            for role, count in sorted(role_counts.items()):
                summary += f"  {role}: {count}\\n"
        
        return summary
        
    except Exception as e:
        return f"Error generating employee summary: {str(e)}"

if __name__ == "__main__":
    mcp.run() 