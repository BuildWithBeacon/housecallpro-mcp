#!/usr/bin/env python3
"""
Housecall Pro Leads MCP Server

This server provides lead management functionality for Housecall Pro,
including CRUD operations for leads and related entities.
"""

import json
import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Leads")

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
async def get_leads(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    employee_id: Optional[str] = None,
    job_type_id: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    updated_after: Optional[str] = None,
    updated_before: Optional[str] = None,
    customer_name: Optional[str] = None,
    customer_email: Optional[str] = None,
    customer_phone: Optional[str] = None
) -> str:
    """
    Retrieve leads with optional filtering and pagination.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of leads per page (default: 25, max: 100)
        sort_by: Field to sort by (created_at, updated_at, status, source)
        sort_direction: Sort direction (asc, desc)
        status: Filter by lead status (new, contacted, qualified, unqualified, converted)
        source: Filter by lead source
        employee_id: Filter by assigned employee ID
        job_type_id: Filter by job type ID
        created_after: Filter leads created after this date (ISO 8601)
        created_before: Filter leads created before this date (ISO 8601)
        updated_after: Filter leads updated after this date (ISO 8601)
        updated_before: Filter leads updated before this date (ISO 8601)
        customer_name: Filter by customer name (partial match)
        customer_email: Filter by customer email
        customer_phone: Filter by customer phone number
    
    Returns:
        JSON string containing leads data or error message
    """
    try:
        params = {}
        
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = min(page_size, 100)  # API limit
        if sort_by:
            params["sort_by"] = sort_by
        if sort_direction:
            params["sort_direction"] = sort_direction
        if status:
            params["status"] = status
        if source:
            params["source"] = source
        if employee_id:
            params["employee_id"] = employee_id
        if job_type_id:
            params["job_type_id"] = job_type_id
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if updated_after:
            params["updated_after"] = updated_after
        if updated_before:
            params["updated_before"] = updated_before
        if customer_name:
            params["customer_name"] = customer_name
        if customer_email:
            params["customer_email"] = customer_email
        if customer_phone:
            params["customer_phone"] = customer_phone
        
        result = make_api_request("GET", "/leads", params=params)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def get_lead(lead_id: str) -> str:
    """
    Retrieve a specific lead by ID.
    
    Args:
        lead_id: The unique identifier of the lead
    
    Returns:
        JSON string containing lead data or error message
    """
    try:
        if not lead_id:
            return json.dumps({"error": "lead_id is required"}, indent=2)
        
        result = make_api_request("GET", f"/leads/{lead_id}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def create_lead(
    customer_name: str,
    customer_phone: Optional[str] = None,
    customer_email: Optional[str] = None,
    address_street: Optional[str] = None,
    address_city: Optional[str] = None,
    address_state: Optional[str] = None,
    address_zip: Optional[str] = None,
    job_type_id: Optional[str] = None,
    source: Optional[str] = None,
    description: Optional[str] = None,
    notes: Optional[str] = None,
    employee_id: Optional[str] = None,
    priority: Optional[str] = None,
    estimated_value: Optional[float] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a new lead.
    
    Args:
        customer_name: Name of the customer (required)
        customer_phone: Customer phone number
        customer_email: Customer email address
        address_street: Street address
        address_city: City
        address_state: State
        address_zip: ZIP code
        job_type_id: ID of the job type for this lead
        source: Lead source (website, referral, phone, etc.)
        description: Description of the lead/work needed
        notes: Additional notes about the lead
        employee_id: ID of employee to assign the lead to
        priority: Lead priority (low, medium, high)
        estimated_value: Estimated value of the lead in dollars
        custom_fields: Additional custom fields as key-value pairs
    
    Returns:
        JSON string containing created lead data or error message
    """
    try:
        if not customer_name:
            return json.dumps({"error": "customer_name is required"}, indent=2)
        
        lead_data = {
            "customer": {
                "name": customer_name
            }
        }
        
        # Add customer contact info
        if customer_phone:
            lead_data["customer"]["phone"] = customer_phone
        if customer_email:
            lead_data["customer"]["email"] = customer_email
        
        # Add address if provided
        if any([address_street, address_city, address_state, address_zip]):
            lead_data["address"] = {}
            if address_street:
                lead_data["address"]["street"] = address_street
            if address_city:
                lead_data["address"]["city"] = address_city
            if address_state:
                lead_data["address"]["state"] = address_state
            if address_zip:
                lead_data["address"]["zip"] = address_zip
        
        # Add lead details
        if job_type_id:
            lead_data["job_type_id"] = job_type_id
        if source:
            lead_data["source"] = source
        if description:
            lead_data["description"] = description
        if notes:
            lead_data["notes"] = notes
        if employee_id:
            lead_data["employee_id"] = employee_id
        if priority:
            lead_data["priority"] = priority
        if estimated_value is not None:
            lead_data["estimated_value"] = estimated_value
        if custom_fields:
            lead_data["custom_fields"] = custom_fields
        
        result = make_api_request("POST", "/leads", json=lead_data)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def update_lead(
    lead_id: str,
    status: Optional[str] = None,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    customer_email: Optional[str] = None,
    address_street: Optional[str] = None,
    address_city: Optional[str] = None,
    address_state: Optional[str] = None,
    address_zip: Optional[str] = None,
    job_type_id: Optional[str] = None,
    source: Optional[str] = None,
    description: Optional[str] = None,
    notes: Optional[str] = None,
    employee_id: Optional[str] = None,
    priority: Optional[str] = None,
    estimated_value: Optional[float] = None,
    custom_fields: Optional[Dict[str, Any]] = None
) -> str:
    """
    Update an existing lead.
    
    Args:
        lead_id: The unique identifier of the lead to update (required)
        status: Lead status (new, contacted, qualified, unqualified, converted)
        customer_name: Name of the customer
        customer_phone: Customer phone number
        customer_email: Customer email address
        address_street: Street address
        address_city: City
        address_state: State
        address_zip: ZIP code
        job_type_id: ID of the job type for this lead
        source: Lead source (website, referral, phone, etc.)
        description: Description of the lead/work needed
        notes: Additional notes about the lead
        employee_id: ID of employee to assign the lead to
        priority: Lead priority (low, medium, high)
        estimated_value: Estimated value of the lead in dollars
        custom_fields: Additional custom fields as key-value pairs
    
    Returns:
        JSON string containing updated lead data or error message
    """
    try:
        if not lead_id:
            return json.dumps({"error": "lead_id is required"}, indent=2)
        
        update_data = {}
        
        # Add status update
        if status:
            update_data["status"] = status
        
        # Add customer updates
        if any([customer_name, customer_phone, customer_email]):
            update_data["customer"] = {}
            if customer_name:
                update_data["customer"]["name"] = customer_name
            if customer_phone:
                update_data["customer"]["phone"] = customer_phone
            if customer_email:
                update_data["customer"]["email"] = customer_email
        
        # Add address updates
        if any([address_street, address_city, address_state, address_zip]):
            update_data["address"] = {}
            if address_street:
                update_data["address"]["street"] = address_street
            if address_city:
                update_data["address"]["city"] = address_city
            if address_state:
                update_data["address"]["state"] = address_state
            if address_zip:
                update_data["address"]["zip"] = address_zip
        
        # Add lead detail updates
        if job_type_id:
            update_data["job_type_id"] = job_type_id
        if source:
            update_data["source"] = source
        if description:
            update_data["description"] = description
        if notes:
            update_data["notes"] = notes
        if employee_id:
            update_data["employee_id"] = employee_id
        if priority:
            update_data["priority"] = priority
        if estimated_value is not None:
            update_data["estimated_value"] = estimated_value
        if custom_fields:
            update_data["custom_fields"] = custom_fields
        
        if not update_data:
            return json.dumps({"error": "At least one field must be provided for update"}, indent=2)
        
        result = make_api_request("PATCH", f"/leads/{lead_id}", json=update_data)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


@mcp.tool()
async def convert_lead_to_job(
    lead_id: str,
    job_type_id: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    scheduled_start: Optional[str] = None,
    scheduled_end: Optional[str] = None,
    employee_ids: Optional[list] = None
) -> str:
    """
    Convert a lead to a job.
    
    Args:
        lead_id: The unique identifier of the lead to convert (required)
        job_type_id: ID of the job type for the new job
        description: Description for the new job
        priority: Job priority (low, medium, high)
        scheduled_start: Scheduled start time (ISO 8601)
        scheduled_end: Scheduled end time (ISO 8601)
        employee_ids: List of employee IDs to assign to the job
    
    Returns:
        JSON string containing created job data or error message
    """
    try:
        if not lead_id:
            return json.dumps({"error": "lead_id is required"}, indent=2)
        
        conversion_data = {}
        
        if job_type_id:
            conversion_data["job_type_id"] = job_type_id
        if description:
            conversion_data["description"] = description
        if priority:
            conversion_data["priority"] = priority
        if scheduled_start:
            conversion_data["scheduled_start"] = scheduled_start
        if scheduled_end:
            conversion_data["scheduled_end"] = scheduled_end
        if employee_ids:
            conversion_data["employee_ids"] = employee_ids
        
        result = make_api_request("POST", f"/leads/{lead_id}/convert", json=conversion_data)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


if __name__ == "__main__":
    mcp.run() 