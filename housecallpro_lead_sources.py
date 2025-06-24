#!/usr/bin/env python3
"""
Housecall Pro Lead Sources MCP Server

This server provides lead sources management functionality for Housecall Pro,
including retrieving, creating, and updating lead sources.
"""

import os
from typing import Optional, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Lead Sources")

# Configuration
API_KEY = os.getenv("HOUSECALL_PRO_API_KEY")
API_BASE_URL = "https://api.housecallpro.com"

if not API_KEY:
    raise ValueError("HOUSECALL_PRO_API_KEY environment variable is required")


def get_headers() -> Dict[str, str]:
    """
    Returns the headers needed for API requests including authentication.
    """
    return {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


@mcp.tool()
async def get_lead_sources(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    is_active: Optional[bool] = None
) -> dict:
    """
    Retrieve lead sources with optional filtering and pagination.
    
    Args:
        page: Page number for pagination (default: 1)
        page_size: Number of lead sources per page (default: 25, max: 200)
        is_active: Filter by active status (true/false). If not provided, returns all lead sources.
    
    Returns:
        Dictionary containing lead sources data or error message
    """
    try:
        params = {}
        
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = min(page_size, 200)  # API limit
        if is_active is not None:
            params["is_active"] = is_active
        
        result = await make_api_request("GET", "/lead_sources", params=params)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def create_lead_source(
    name: str,
    is_active: Optional[bool] = True
) -> dict:
    """
    Create a new lead source.
    
    Args:
        name: Name of the lead source (required)
        is_active: Whether the lead source is active (default: true)
    
    Returns:
        Dictionary containing created lead source data or error message
    """
    try:
        if not name or not name.strip():
            return {"error": "name is required and cannot be empty"}
        
        lead_source_data = {
            "name": name.strip()
        }
        
        if is_active is not None:
            lead_source_data["is_active"] = is_active
        
        result = await make_api_request("POST", "/lead_sources", data=lead_source_data)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def update_lead_source(
    lead_source_id: str,
    name: Optional[str] = None,
    is_active: Optional[bool] = None
) -> dict:
    """
    Update an existing lead source.
    
    Args:
        lead_source_id: The unique identifier of the lead source to update (required)
        name: New name for the lead source
        is_active: Whether the lead source should be active
    
    Returns:
        Dictionary containing updated lead source data or error message
    """
    try:
        if not lead_source_id or not lead_source_id.strip():
            return {"error": "lead_source_id is required and cannot be empty"}
        
        # Build update data with only provided fields
        update_data = {}
        
        if name is not None:
            if not name.strip():
                return {"error": "name cannot be empty"}
            update_data["name"] = name.strip()
        
        if is_active is not None:
            update_data["is_active"] = is_active
        
        if not update_data:
            return {"error": "At least one field (name or is_active) must be provided for update"}
        
        result = await make_api_request("PUT", f"/lead_sources/{lead_source_id}", data=update_data)
        return result
        
    except Exception as e:
        return {"error": str(e)}


async def make_api_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
    """Make authenticated API request to Housecall Pro."""
    async with httpx.AsyncClient() as client:
        headers = get_headers()
        
        url = f"{API_BASE_URL}{endpoint}"
        
        if method.upper() == "GET":
            response = await client.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = await client.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code >= 400:
            error_msg = f"API request failed: {response.status_code} {response.text}"
            return {"error": error_msg, "status_code": response.status_code}
        
        return response.json() if response.content else {}


if __name__ == "__main__":
    mcp.run() 