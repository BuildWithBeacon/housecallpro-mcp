#!/usr/bin/env python3
"""
Housecall Pro Materials MCP Server

This server provides materials management functionality for Housecall Pro,
including retrieving, creating, updating, and deleting materials.
"""

import os
from typing import Optional, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Materials")

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
async def get_material_categories(parent_uuid: Optional[str] = None) -> dict:
    """
    Get material categories from the price book.
    
    Args:
        parent_uuid: UUID of parent category to get subcategories. 
                    If None, returns root level categories.
    
    Returns:
        Dictionary containing material categories data with their UUIDs or error message
    """
    try:
        params = {}
        if parent_uuid and parent_uuid.strip():
            params["parent_uuid"] = parent_uuid.strip()
            
        result = await make_api_request("GET", "/api/price_book/material_categories", params=params)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def find_category_by_name(category_name: str, parent_uuid: Optional[str] = None) -> dict:
    """
    Find a material category by name, optionally within a parent category.
    
    Args:
        category_name: Name of the category to search for (case-insensitive)
        parent_uuid: UUID of parent category to search within. 
                    If None, searches root level categories.
    
    Returns:
        Dictionary containing the found category data or error message
    """
    try:
        # Get categories at the specified level
        categories_result = await get_material_categories(parent_uuid=parent_uuid)
        
        if "error" in categories_result:
            return categories_result
            
        categories = categories_result.get('data', [])
        category_name_lower = category_name.lower()
        
        # Search for matching category
        for category in categories:
            if category_name_lower in category.get('name', '').lower():
                return {
                    "found": True,
                    "category": category,
                    "uuid": category.get('uuid'),
                    "name": category.get('name'),
                    "parent_uuid": parent_uuid
                }
        
        return {
            "found": False,
            "message": f"No category found containing '{category_name}'" + 
                      (f" under parent {parent_uuid}" if parent_uuid else " at root level")
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_materials(
    material_category_uuid: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 50,
    name: Optional[str] = None,
    sku: Optional[str] = None,
    is_active: Optional[bool] = None
) -> dict:
    """
    Retrieve materials with optional filtering and pagination.
    
    Args:
        material_category_uuid: The UUID of the material category (required)
        page: Page number for pagination (default: 1)
        page_size: Number of items per page (default: 50)
        name: Filter by material name
        sku: Filter by material SKU
        is_active: Filter by active status (true/false)
    
    Returns:
        Dictionary containing materials data with pagination info or error message
    """
    try:
        if not material_category_uuid or not material_category_uuid.strip():
            return {"error": "material_category_uuid is required and cannot be empty"}
        
        params = {
            "material_category_uuid": material_category_uuid.strip()
        }
        
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if name is not None:
            params["name"] = name.strip()
        if sku is not None:
            params["sku"] = sku.strip()
        if is_active is not None:
            params["is_active"] = is_active
        
        result = await make_api_request("GET", "/api/price_book/materials", params=params)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def create_material(
    name: str,
    sku: str,
    price: float,
    cost: Optional[float] = None,
    description: Optional[str] = None,
    unit: Optional[str] = None,
    is_active: Optional[bool] = True,
    is_taxable: Optional[bool] = True
) -> dict:
    """
    Create a new material.
    
    Args:
        name: Name of the material (required)
        sku: Stock Keeping Unit identifier (required)
        price: Selling price of the material (required)
        cost: Cost price of the material
        description: Description of the material
        unit: Unit of measurement (e.g., "each", "foot", "gallon")
        is_active: Whether the material is active (default: true)
        is_taxable: Whether the material is taxable (default: true)
    
    Returns:
        Dictionary containing created material data or error message
    """
    try:
        if not name or not name.strip():
            return {"error": "name is required and cannot be empty"}
        
        if not sku or not sku.strip():
            return {"error": "sku is required and cannot be empty"}
        
        if price is None:
            return {"error": "price is required"}
        
        if price < 0:
            return {"error": "price cannot be negative"}
        
        if cost is not None and cost < 0:
            return {"error": "cost cannot be negative"}
        
        material_data = {
            "name": name.strip(),
            "sku": sku.strip(),
            "price": price
        }
        
        if cost is not None:
            material_data["cost"] = cost
        if description is not None:
            material_data["description"] = description.strip()
        if unit is not None:
            material_data["unit"] = unit.strip()
        if is_active is not None:
            material_data["is_active"] = is_active
        if is_taxable is not None:
            material_data["is_taxable"] = is_taxable
        
        result = await make_api_request("POST", "/api/price_book/materials", json_data=material_data)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def update_material(
    material_id: str,
    name: Optional[str] = None,
    sku: Optional[str] = None,
    price: Optional[float] = None,
    cost: Optional[float] = None,
    description: Optional[str] = None,
    unit: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_taxable: Optional[bool] = None
) -> dict:
    """
    Update an existing material.
    
    Args:
        material_id: The unique identifier of the material to update (required)
        name: Updated name of the material
        sku: Updated Stock Keeping Unit identifier
        price: Updated selling price of the material
        cost: Updated cost price of the material
        description: Updated description of the material
        unit: Updated unit of measurement
        is_active: Updated active status
        is_taxable: Updated taxable status
    
    Returns:
        Dictionary containing updated material data or error message
    """
    try:
        if not material_id or not material_id.strip():
            return {"error": "material_id is required and cannot be empty"}
        
        material_data = {}
        
        if name is not None:
            if not name.strip():
                return {"error": "name cannot be empty when provided"}
            material_data["name"] = name.strip()
        
        if sku is not None:
            if not sku.strip():
                return {"error": "sku cannot be empty when provided"}
            material_data["sku"] = sku.strip()
        
        if price is not None:
            if price < 0:
                return {"error": "price cannot be negative"}
            material_data["price"] = price
        
        if cost is not None:
            if cost < 0:
                return {"error": "cost cannot be negative"}
            material_data["cost"] = cost
        
        if description is not None:
            material_data["description"] = description.strip()
        
        if unit is not None:
            material_data["unit"] = unit.strip()
        
        if is_active is not None:
            material_data["is_active"] = is_active
        
        if is_taxable is not None:
            material_data["is_taxable"] = is_taxable
        
        if not material_data:
            return {"error": "At least one field must be provided for update"}
        
        result = await make_api_request("PUT", f"/api/price_book/materials/{material_id.strip()}", json_data=material_data)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def delete_material(
    material_id: str
) -> dict:
    """
    Delete a material.
    
    Args:
        material_id: The unique identifier of the material to delete (required)
    
    Returns:
        Dictionary containing success confirmation or error message
    """
    try:
        if not material_id or not material_id.strip():
            return {"error": "material_id is required and cannot be empty"}
        
        result = await make_api_request("DELETE", f"/api/price_book/materials/{material_id.strip()}")
        return result
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run() 