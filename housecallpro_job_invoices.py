#!/usr/bin/env python3
"""
Housecall Pro Job Invoices MCP Server

This server provides job invoice management functionality for Housecall Pro,
including operations for job-related invoices.
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
mcp = FastMCP("Housecall Pro Job Invoices")

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
async def get_job_invoices(
    job_id: str,
    include_line_items: Optional[bool] = None,
    include_attachments: Optional[bool] = None,
    include_payments: Optional[bool] = None,
    status: Optional[str] = None
) -> str:
    """
    Retrieve all invoices for a specific job.
    
    This endpoint returns all invoices associated with a particular job,
    including their current status, amounts, due dates, and other invoice details.
    
    Args:
        job_id: The ID of the job to get invoices for (required)
        include_line_items: Include detailed line items in the response (optional)
        include_attachments: Include invoice attachments in the response (optional)
        include_payments: Include payment information in the response (optional)
        status: Filter invoices by status (e.g., 'open', 'paid', 'voided', 'draft') (optional)
    
    Returns:
        JSON string containing the list of invoices for the specified job
    """
    params = {}
    
    if include_line_items is not None:
        params["include_line_items"] = str(include_line_items).lower()
    if include_attachments is not None:
        params["include_attachments"] = str(include_attachments).lower()
    if include_payments is not None:
        params["include_payments"] = str(include_payments).lower()
    if status:
        params["status"] = status
    
    try:
        result = await make_api_request("GET", f"/jobs/{job_id}/invoices", params=params)
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Error: Job with ID '{job_id}' not found"
        elif e.response.status_code == 403:
            return f"Error: Access denied to job '{job_id}' - check permissions"
        else:
            return f"Error getting job invoices: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error getting job invoices: {str(e)}"


if __name__ == "__main__":
    import asyncio
    mcp.run() 