#!/usr/bin/env python3
"""
Housecall Pro Jobs MCP Server

This server provides comprehensive job management functionality for Housecall Pro,
including job CRUD operations, line item management, scheduling, attachments,
notes, tags, and more.
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
mcp = FastMCP("Housecall Pro Jobs")

# Configuration
API_KEY = os.getenv("HOUSECALL_PRO_API_KEY")
API_BASE_URL = "https://api.housecallpro.com"


def get_headers() -> Dict[str, str]:
    """Get headers for API requests."""
    if not API_KEY:
        raise ValueError("Missing HOUSECALL_PRO_API_KEY environment variable")
    
    return {
        "Authorization": f"Token {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


async def make_api_request(
    method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None
) -> Dict[str, Any]:
    """Make an authenticated API request to Housecall Pro."""
    headers = get_headers()
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            headers=headers,
            params=params,
            json=json_data,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


# Job Management Tools

@mcp.tool()
async def get_jobs(
    customer_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    status: Optional[str] = None,
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
    work_status: Optional[str] = None,
    tags: Optional[str] = None,
    include_notes: Optional[bool] = None,
    include_line_items: Optional[bool] = None,
    include_photos: Optional[bool] = None,
    page_size: Optional[int] = None,
    page: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    updated_after: Optional[str] = None,
    updated_before: Optional[str] = None,
    scheduled_start_min: Optional[str] = None,
    scheduled_start_max: Optional[str] = None,
    scheduled_end_min: Optional[str] = None,
    scheduled_end_max: Optional[str] = None,
) -> str:
    """
    Retrieve a list of jobs with optional filtering.
    
    Args:
        customer_id: Filter by customer ID
        employee_id: Filter by employee ID
        status: Filter by job status (scheduled, in_progress, completed, cancelled)
        date_start: Start date filter (YYYY-MM-DD format)
        date_end: End date filter (YYYY-MM-DD format)
        work_status: Filter by work status
        tags: Filter by tags (comma-separated)
        include_notes: Include job notes in response
        include_line_items: Include line items in response
        include_photos: Include photos in response
        page_size: Number of results per page (default 25, max 100)
        page: Page number to retrieve
        sort_by: Field to sort by
        sort_direction: Sort direction (asc or desc)
        created_after: Return jobs created after this date (ISO 8601)
        created_before: Return jobs created before this date (ISO 8601)
        updated_after: Return jobs updated after this date (ISO 8601)
        updated_before: Return jobs updated before this date (ISO 8601)
        scheduled_start_min: Minimum scheduled start time (ISO 8601)
        scheduled_start_max: Maximum scheduled start time (ISO 8601)
        scheduled_end_min: Minimum scheduled end time (ISO 8601)
        scheduled_end_max: Maximum scheduled end time (ISO 8601)
    """
    params = {}
    
    if customer_id:
        params["customer_id"] = customer_id
    if employee_id:
        params["employee_id"] = employee_id
    if status:
        params["status"] = status
    if date_start:
        params["date_start"] = date_start
    if date_end:
        params["date_end"] = date_end
    if work_status:
        params["work_status"] = work_status
    if sort_by:
        params["sort_by"] = sort_by
    if sort_direction:
        params["sort_direction"] = sort_direction
    if page:
        params["page"] = page
    if page_size:
        params["page_size"] = page_size
    if tags:
        params["tags"] = tags
    if created_after:
        params["created_after"] = created_after
    if created_before:
        params["created_before"] = created_before
    if updated_after:
        params["updated_after"] = updated_after
    if updated_before:
        params["updated_before"] = updated_before
    if scheduled_start_min:
        params["scheduled_start_min"] = scheduled_start_min
    if scheduled_start_max:
        params["scheduled_start_max"] = scheduled_start_max
    if scheduled_end_min:
        params["scheduled_end_min"] = scheduled_end_min
    if scheduled_end_max:
        params["scheduled_end_max"] = scheduled_end_max
    
    try:
        result = await make_api_request("GET", "/jobs", params=params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting jobs: {str(e)}"}, indent=2)


@mcp.tool()
async def get_job_by_id(job_id: str) -> str:
    """
    Get detailed information about a specific job.
    
    Args:
        job_id: The ID of the job to retrieve
    """
    try:
        result = await make_api_request("GET", f"/jobs/{job_id}")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def create_job(
    customer_id: str,
    work_status: str = "needs_scheduling",
    description: Optional[str] = None,
    tags: Optional[List[str]] = None,
    lead_source: Optional[str] = None,
    note_to_customer: Optional[str] = None,
    scheduled_start: Optional[str] = None,
    scheduled_end: Optional[str] = None,
    employee_ids: Optional[List[str]] = None,
) -> str:
    """
    Create a new job.
    
    Args:
        customer_id: ID of the customer for this job (required)
        work_status: Status of the job (needs_scheduling, scheduled, in_progress, completed, cancelled)
        description: Description of the job
        tags: List of tags to apply to the job
        lead_source: Source of the lead
        note_to_customer: Note visible to the customer
        scheduled_start: Scheduled start time (ISO 8601)
        scheduled_end: Scheduled end time (ISO 8601)
        employee_ids: List of employee IDs to assign to the job
    """
    data = {
        "customer_id": customer_id,
        "work_status": work_status,
    }
    
    if description:
        data["description"] = description
    if tags:
        data["tags"] = tags
    if lead_source:
        data["lead_source"] = lead_source
    if note_to_customer:
        data["note_to_customer"] = note_to_customer
    if scheduled_start:
        data["scheduled_start"] = scheduled_start
    if scheduled_end:
        data["scheduled_end"] = scheduled_end
    if employee_ids:
        data["employee_ids"] = employee_ids
    
    try:
        result = await make_api_request("POST", "/jobs", json_data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error creating job: {str(e)}"}, indent=2)


# Job Attachments

@mcp.tool()
async def add_job_attachment(
    job_id: str,
    name: str,
    file_data: str,
    content_type: str = "application/octet-stream",
) -> str:
    """
    Add an attachment to a job.
    
    Args:
        job_id: ID of the job
        name: Name of the attachment
        file_data: Base64 encoded file data
        content_type: MIME type of the file
    """
    try:
        import base64
        file_bytes = base64.b64decode(file_data)
        
        files = {
            "attachment": (name, file_bytes, content_type)
        }
        
        result = await make_api_request("POST", f"/jobs/{job_id}/attachments", files=files)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error adding attachment to job {job_id}: {str(e)}"}, indent=2)


# Job Line Items

@mcp.tool()
async def get_job_line_items(job_id: str) -> str:
    """
    Get all line items for a job.
    
    Args:
        job_id: ID of the job
    """
    try:
        result = await make_api_request("GET", f"/jobs/{job_id}/line_items")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting line items for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def add_job_line_item(
    job_id: str,
    name: str,
    quantity: float,
    price: float,
    unit: Optional[str] = None,
    description: Optional[str] = None,
    sku: Optional[str] = None,
) -> str:
    """
    Add a line item to a job.
    
    Args:
        job_id: ID of the job
        name: Name of the line item
        quantity: Quantity of the item
        price: Price per unit
        unit: Unit of measurement
        description: Description of the line item
        sku: SKU of the item
    """
    data = {
        "name": name,
        "quantity": quantity,
        "price": price,
    }
    
    if unit:
        data["unit"] = unit
    if description:
        data["description"] = description
    if sku:
        data["sku"] = sku
    
    try:
        result = await make_api_request("POST", f"/jobs/{job_id}/line_items", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error adding line item to job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def bulk_update_job_line_items(
    job_id: str,
    line_items: List[Dict[str, Any]],
) -> str:
    """
    Bulk update line items for a job.
    
    Args:
        job_id: ID of the job
        line_items: List of line item objects with updates
    """
    data = {
        "line_items": line_items
    }
    
    try:
        result = await make_api_request("PUT", f"/jobs/{job_id}/line_items", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error bulk updating line items for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def update_job_line_item(
    job_id: str,
    line_item_id: str,
    name: Optional[str] = None,
    quantity: Optional[float] = None,
    price: Optional[float] = None,
    unit: Optional[str] = None,
    description: Optional[str] = None,
    sku: Optional[str] = None,
) -> str:
    """
    Update a single line item for a job.
    
    Args:
        job_id: ID of the job
        line_item_id: ID of the line item to update
        name: Name of the line item
        quantity: Quantity of the item
        price: Price per unit
        unit: Unit of measurement
        description: Description of the line item
        sku: SKU of the item
    """
    data = {}
    
    if name is not None:
        data["name"] = name
    if quantity is not None:
        data["quantity"] = quantity
    if price is not None:
        data["price"] = price
    if unit is not None:
        data["unit"] = unit
    if description is not None:
        data["description"] = description
    if sku is not None:
        data["sku"] = sku
    
    try:
        result = await make_api_request("PUT", f"/jobs/{job_id}/line_items/{line_item_id}", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error updating line item {line_item_id} for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def delete_job_line_item(job_id: str, line_item_id: str) -> str:
    """
    Delete a line item from a job.
    
    Args:
        job_id: ID of the job
        line_item_id: ID of the line item to delete
    """
    try:
        result = await make_api_request("DELETE", f"/jobs/{job_id}/line_items/{line_item_id}")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error deleting line item {line_item_id} from job {job_id}: {str(e)}"}, indent=2)


# Job Scheduling

@mcp.tool()
async def update_job_schedule(
    job_id: str,
    scheduled_start: str,
    scheduled_end: str,
    employee_ids: Optional[List[str]] = None,
) -> str:
    """
    Update the schedule for a job.
    
    Args:
        job_id: ID of the job
        scheduled_start: Scheduled start time (ISO 8601)
        scheduled_end: Scheduled end time (ISO 8601)
        employee_ids: List of employee IDs to assign to the job
    """
    data = {
        "scheduled_start": scheduled_start,
        "scheduled_end": scheduled_end,
    }
    
    if employee_ids:
        data["employee_ids"] = employee_ids
    
    try:
        result = await make_api_request("PUT", f"/jobs/{job_id}/schedule", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error updating schedule for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def delete_job_schedule(job_id: str) -> str:
    """
    Remove the schedule from a job.
    
    Args:
        job_id: ID of the job
    """
    try:
        result = await make_api_request("DELETE", f"/jobs/{job_id}/schedule")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error deleting schedule for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def dispatch_job_to_employees(
    job_id: str,
    employee_ids: List[str],
) -> str:
    """
    Dispatch a job to specific employees.
    
    Args:
        job_id: ID of the job
        employee_ids: List of employee IDs to dispatch the job to
    """
    data = {
        "employee_ids": employee_ids
    }
    
    try:
        result = await make_api_request("POST", f"/jobs/{job_id}/dispatch", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error dispatching job {job_id}: {str(e)}"}, indent=2)


# Job Input Materials

@mcp.tool()
async def get_job_input_materials(job_id: str) -> str:
    """
    Get all input materials for a job.
    
    Args:
        job_id: ID of the job
    """
    try:
        result = await make_api_request("GET", f"/jobs/{job_id}/input_materials")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error getting input materials for job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def bulk_update_job_input_materials(
    job_id: str,
    input_materials: List[Dict[str, Any]],
) -> str:
    """
    Bulk update input materials for a job.
    
    Args:
        job_id: ID of the job
        input_materials: List of input material objects with updates
    """
    data = {
        "input_materials": input_materials
    }
    
    try:
        result = await make_api_request("PUT", f"/jobs/{job_id}/input_materials", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error bulk updating input materials for job {job_id}: {str(e)}"}, indent=2)


# Job Tags

@mcp.tool()
async def add_job_tag(job_id: str, tag: str) -> str:
    """
    Add a tag to a job.
    
    Args:
        job_id: ID of the job
        tag: Tag to add to the job
    """
    data = {
        "tag": tag
    }
    
    try:
        result = await make_api_request("POST", f"/jobs/{job_id}/tags", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error adding tag to job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def remove_job_tag(job_id: str, tag: str) -> str:
    """
    Remove a tag from a job.
    
    Args:
        job_id: ID of the job
        tag: Tag to remove from the job
    """
    try:
        result = await make_api_request("DELETE", f"/jobs/{job_id}/tags/{tag}")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error removing tag from job {job_id}: {str(e)}"}, indent=2)


# Job Notes

@mcp.tool()
async def add_job_note(
    job_id: str,
    note: str,
    note_type: str = "internal",
) -> str:
    """
    Add a note to a job.
    
    Args:
        job_id: ID of the job
        note: Note content
        note_type: Type of note (internal, customer_visible)
    """
    data = {
        "note": note,
        "note_type": note_type,
    }
    
    try:
        result = await make_api_request("POST", f"/jobs/{job_id}/notes", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error adding note to job {job_id}: {str(e)}"}, indent=2)


@mcp.tool()
async def delete_job_note(job_id: str, note_id: str) -> str:
    """
    Delete a note from a job.
    
    Args:
        job_id: ID of the job
        note_id: ID of the note to delete
    """
    try:
        result = await make_api_request("DELETE", f"/jobs/{job_id}/notes/{note_id}")
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error deleting note {note_id} from job {job_id}: {str(e)}"}, indent=2)


# Job Links

@mcp.tool()
async def create_job_link(
    job_id: str,
    url: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """
    Create a link associated with a job.
    
    Args:
        job_id: ID of the job
        url: URL of the link
        name: Name/title for the link
        description: Description of the link
    """
    data = {
        "url": url,
    }
    
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    
    try:
        result = await make_api_request("POST", f"/jobs/{job_id}/links", data=data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error creating link for job {job_id}: {str(e)}"}, indent=2)


if __name__ == "__main__":
    # Verify environment variables
    if not API_KEY:
        print("Error: HOUSECALL_PRO_API_KEY environment variable is required")
        exit(1)
    
    # Run the server
    mcp.run() 