#!/usr/bin/env python3
"""
Housecall Pro Events MCP Server

This server provides event management functionality for Housecall Pro,
including retrieving a list of events and fetching a specific event by its ID.
"""

import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Events")

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
async def get_events(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    event_ids: Optional[List[str]] = None,
    last_polled_at: Optional[str] = None,
    event_names: Optional[List[str]] = None,
    resource_names: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Retrieves a list of events with optional filtering and pagination.

    Args:
        page: The page number to retrieve.
        page_size: The number of events per page (max 50).
        event_ids: A list of event IDs to filter by.
        last_polled_at: ISO 8601 timestamp to get events since a certain time.
        event_names: A list of event names to filter by (e.g., 'job.created').
        resource_names: A list of resource names to filter by (e.g., 'customer').

    Returns:
        A dictionary containing a list of events and pagination information.
    """
    headers = get_headers()
    params = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size
    if event_ids:
        params["id"] = ",".join(event_ids)
    if last_polled_at:
        params["last_polled_at"] = last_polled_at
    if event_names:
        params["event_name"] = ",".join(event_names)
    if resource_names:
        params["resource_name"] = ",".join(resource_names)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/events", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_event_by_id(event_id: str) -> Dict[str, Any]:
    """
    Retrieves a single event by its ID.

    Args:
        event_id: The unique identifier for the event.

    Returns:
        A dictionary containing the event details.
    """
    headers = get_headers()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/events/{event_id}", headers=headers
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run() 