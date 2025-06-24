#!/usr/bin/env python3
"""
Housecall Pro Estimates MCP Server

This server provides estimate management functionality for Housecall Pro,
including CRUD operations for estimates.
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
mcp = FastMCP("Housecall Pro Estimates")

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
def get_estimates(
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    customer_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Retrieve estimates from Housecall Pro.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of results per page (default: 50, max: 200)
        customer_id: Filter by customer ID
        start_date: Filter estimates created after this date (YYYY-MM-DD format)
        end_date: Filter estimates created before this date (YYYY-MM-DD format)
    
    Returns:
        JSON string containing the estimates data
    """
    params = {
        "page": page,
        "page_size": min(page_size, 200)  # API max is 200
    }
    
    if customer_id:
        params["customer_id"] = customer_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    result = make_api_request("GET", "estimates", params=params)
    return json.dumps(result, indent=2)


@mcp.tool()
def create_estimate(
    customer_id: str,
    employee_id: str,
    line_items: List[Dict[str, Any]],
    notes: Optional[str] = None,
    work_status: Optional[str] = None
) -> str:
    """
    Create a new estimate in Housecall Pro.
    
    Args:
        customer_id: ID of the customer (required)
        employee_id: ID of the employee creating the estimate (required)
        line_items: List of line items for the estimate (required)
        notes: Additional notes for the estimate
        work_status: Status of the work (e.g., "pending", "approved", "declined")
    
    Returns:
        JSON string containing the created estimate data
    """
    data = {
        "customer_id": customer_id,
        "employee_id": employee_id,
        "line_items": line_items
    }
    
    if notes:
        data["notes"] = notes
    if work_status:
        data["work_status"] = work_status
    
    result = make_api_request("POST", "estimates", json=data)
    return json.dumps(result, indent=2)


@mcp.tool()
def update_estimate(
    estimate_id: str,
    notes: Optional[str] = None,
    work_status: Optional[str] = None,
    line_items: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Update an existing estimate in Housecall Pro.
    
    Args:
        estimate_id: ID of the estimate to update (required)
        notes: Updated notes for the estimate
        work_status: Updated status of the work
        line_items: Updated list of line items
    
    Returns:
        JSON string containing the updated estimate data
    """
    data = {}
    
    if notes is not None:
        data["notes"] = notes
    if work_status is not None:
        data["work_status"] = work_status
    if line_items is not None:
        data["line_items"] = line_items
    
    result = make_api_request("PUT", f"estimates/{estimate_id}", json=data)
    return json.dumps(result, indent=2)


@mcp.tool()
def delete_estimate(estimate_id: str) -> str:
    """
    Delete an estimate from Housecall Pro.
    
    Args:
        estimate_id: ID of the estimate to delete (required)
    
    Returns:
        JSON string confirming deletion
    """
    result = make_api_request("DELETE", f"estimates/{estimate_id}")
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run() 