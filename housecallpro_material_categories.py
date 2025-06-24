#!/usr/bin/env python3
"""
Housecall Pro Material Categories MCP Server

This server provides material categories management functionality for Housecall Pro,
including retrieving, creating, updating, and deleting material categories.
"""

import os
from typing import Optional, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Material Categories")

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


async def make_api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Makes an authenticated API request to Housecall Pro.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        params: Query parameters
        json_data: JSON data for request body
        
    Returns:
        API response as dictionary
        
    Raises:
        Exception: If the API request fails
    """
    url = f"{API_BASE_URL}/{endpoint.lstrip('/')}"
    headers = get_headers()
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_material_categories(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    name: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Retrieve material categories from Housecall Pro.
    
    Args:
        page: Page number for pagination (optional)
        page_size: Number of items per page (optional)
        name: Filter by category name (optional)
        is_active: Filter by active status (optional)
    
    Returns:
        Dict containing material categories data and pagination info
    """
    params = {}
    
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if name:
        params["name"] = name
    if is_active is not None:
        params["is_active"] = is_active
    
    try:
        result = await make_api_request("GET", "/material_categories", params=params)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def create_material_category(
    name: str,
    description: Optional[str] = None,
    is_active: bool = True
) -> Dict[str, Any]:
    """
    Create a new material category in Housecall Pro.
    
    Args:
        name: Name of the material category (required)
        description: Description of the material category (optional)
        is_active: Whether the category is active (default: true)
    
    Returns:
        Dict containing the created material category data
    """
    # Input validation
    if not name or not name.strip():
        return {
            "success": False,
            "error": "Material category name is required and cannot be empty"
        }
    
    data = {
        "name": name.strip(),
        "is_active": is_active
    }
    
    if description:
        data["description"] = description.strip()
    
    try:
        result = await make_api_request("POST", "/material_categories", data=data)
        return {
            "success": True,
            "data": result,
            "message": f"Material category '{name}' created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def update_material_category(
    category_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update an existing material category in Housecall Pro.
    
    Args:
        category_id: ID of the material category to update (required)
        name: New name for the category (optional)
        description: New description for the category (optional)
        is_active: New active status for the category (optional)
    
    Returns:
        Dict containing the updated material category data
    """
    # Input validation
    if not category_id or not category_id.strip():
        return {
            "success": False,
            "error": "Material category ID is required"
        }
    
    data = {}
    
    if name is not None:
        if not name.strip():
            return {
                "success": False,
                "error": "Material category name cannot be empty"
            }
        data["name"] = name.strip()
    
    if description is not None:
        data["description"] = description.strip() if description else ""
    
    if is_active is not None:
        data["is_active"] = is_active
    
    if not data:
        return {
            "success": False,
            "error": "At least one field must be provided for update"
        }
    
    try:
        result = await make_api_request("PUT", f"/material_categories/{category_id}", data=data)
        return {
            "success": True,
            "data": result,
            "message": f"Material category {category_id} updated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def delete_material_category(category_id: str) -> Dict[str, Any]:
    """
    Delete a material category from Housecall Pro.
    
    Args:
        category_id: ID of the material category to delete (required)
    
    Returns:
        Dict containing success confirmation or error details
    """
    # Input validation
    if not category_id or not category_id.strip():
        return {
            "success": False,
            "error": "Material category ID is required"
        }
    
    try:
        result = await make_api_request("DELETE", f"/material_categories/{category_id}")
        return {
            "success": True,
            "data": result,
            "message": f"Material category {category_id} deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    mcp.run() 