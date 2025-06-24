#!/usr/bin/env python3
"""
Housecall Pro Appointments MCP Server

This server provides appointment management functionality for Housecall Pro,
including CRUD operations for appointments.
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
mcp = FastMCP("Housecall Pro Appointments")

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
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    
    # Add headers
    headers = get_headers()
    if 'headers' in kwargs:
        headers.update(kwargs.pop('headers'))
    
    try:
        with httpx.Client() as client:
            response = client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
    except httpx.HTTPStatusError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Request failed: {str(e)}"}, indent=2)


@mcp.tool()
def get_appointments(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    customer_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    Retrieve appointments from Housecall Pro.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of results per page (default: 50, max: 200)
        customer_id: Filter by customer ID
        employee_id: Filter by employee ID
        start_date: Filter appointments after this date (YYYY-MM-DD format)
        end_date: Filter appointments before this date (YYYY-MM-DD format)
        status: Filter by appointment status
    
    Returns:
        JSON string containing the appointments data
    """
    params = {
        "page": page,
        "page_size": min(page_size, 200)  # API max is 200
    }
    
    if customer_id:
        params["customer_id"] = customer_id
    if employee_id:
        params["employee_id"] = employee_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if status:
        params["status"] = status
    
    result = make_api_request("GET", "appointments", params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
def create_appointment(
    customer_id: str,
    employee_id: str,
    start_time: str,
    end_time: str,
    service_id: Optional[str] = None,
    notes: Optional[str] = None,
    address: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a new appointment in Housecall Pro.
    
    Args:
        customer_id: ID of the customer (required)
        employee_id: ID of the employee (required)
        start_time: Start time of the appointment (ISO 8601 format)
        end_time: End time of the appointment (ISO 8601 format)
        service_id: ID of the service to be performed
        notes: Additional notes for the appointment
        address: Address object for the appointment location
    
    Returns:
        JSON string containing the created appointment data
    """
    data = {
        "customer_id": customer_id,
        "employee_id": employee_id,
        "start_time": start_time,
        "end_time": end_time
    }
    
    if service_id:
        data["service_id"] = service_id
    if notes:
        data["notes"] = notes
    if address:
        data["address"] = address
    
    result = make_api_request("POST", "appointments", json=data)
    return json.dumps(result, indent=2)


@mcp.tool()
def update_appointment(
    appointment_id: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    employee_id: Optional[str] = None,
    notes: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    Update an existing appointment in Housecall Pro.
    
    Args:
        appointment_id: ID of the appointment to update (required)
        start_time: Updated start time (ISO 8601 format)
        end_time: Updated end time (ISO 8601 format)
        employee_id: Updated employee ID
        notes: Updated notes
        status: Updated appointment status
    
    Returns:
        JSON string containing the updated appointment data
    """
    data = {}
    
    if start_time is not None:
        data["start_time"] = start_time
    if end_time is not None:
        data["end_time"] = end_time
    if employee_id is not None:
        data["employee_id"] = employee_id
    if notes is not None:
        data["notes"] = notes
    if status is not None:
        data["status"] = status
    
    result = make_api_request("PUT", f"appointments/{appointment_id}", json=data)
    return json.dumps(result, indent=2)


@mcp.tool()
def delete_appointment(appointment_id: str) -> str:
    """
    Delete an appointment from Housecall Pro.
    
    Args:
        appointment_id: ID of the appointment to delete (required)
    
    Returns:
        JSON string confirming deletion
    """
    result = make_api_request("DELETE", f"appointments/{appointment_id}")
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run() 