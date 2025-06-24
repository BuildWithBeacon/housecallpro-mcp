#!/usr/bin/env python3
"""
Housecall Pro Tags MCP Server

This server provides tags management functionality for Housecall Pro,
including retrieving, creating, and updating tags.
"""

import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Tags")

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
async def get_tags(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    name: Optional[str] = None,
    tag_type: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Retrieves a list of tags with optional filtering and pagination.

    Args:
        page: The page number to retrieve.
        page_size: The number of tags per page.
        name: Filter tags by name.
        tag_type: Filter tags by type (e.g., 'customer', 'job').
        is_active: Filter tags by active status.

    Returns:
        A dictionary containing a list of tags and pagination info.
    """
    headers = get_headers()
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if name:
        params["name"] = name
    if tag_type:
        params["tag_type"] = tag_type
    if is_active is not None:
        params["is_active"] = is_active

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/tags", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_tag(
    name: str, tag_type: str, is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Creates a new tag.

    Args:
        name: The name of the tag.
        tag_type: The type of tag (e.g., 'customer', 'job').
        is_active: Whether the tag is active. Defaults to true.

    Returns:
        A dictionary containing the created tag.
    """
    headers = get_headers()
    json_payload = {"name": name, "tag_type": tag_type}
    if is_active is not None:
        json_payload["is_active"] = is_active

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/tags", headers=headers, json=json_payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_tag(
    tag_id: str, name: Optional[str] = None, is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates an existing tag.

    Args:
        tag_id: The unique identifier of the tag to update.
        name: The new name for the tag.
        is_active: The new active status for the tag.

    Returns:
        A dictionary containing the updated tag.
    """
    headers = get_headers()
    json_payload = {}
    if name:
        json_payload["name"] = name
    if is_active is not None:
        json_payload["is_active"] = is_active

    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_BASE_URL}/tags/{tag_id}", headers=headers, json=json_payload
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run() 