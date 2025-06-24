#!/usr/bin/env python3
"""
Housecall Pro Schedule MCP Server

This server provides schedule management functionality for Housecall Pro,
including retrieving and updating schedule windows, and getting booking windows.
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Schedule")

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
async def get_schedule_windows(start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Retrieves the schedule windows for a given date range.

    Args:
        start_date: The start date in YYYY-MM-DD format.
        end_date: The end date in YYYY-MM-DD format.

    Returns:
        A dictionary containing the schedule windows.
    """
    headers = get_headers()
    params = {"start_date": start_date, "end_date": end_date}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/schedules/windows", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def update_schedule_windows(windows: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Updates the company's schedule windows.

    Args:
        windows: A list of window dictionaries, each with 'start_time' and 'end_time'.
                 Example: [{"start_time": "08:00", "end_time": "12:00"}]

    Returns:
        A dictionary containing the updated schedule windows.
    """
    headers = get_headers()
    json_payload = {"windows": windows}
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_BASE_URL}/schedules/windows", headers=headers, json=json_payload
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_booking_windows(
    start_date: str, end_date: str, address: str, service_ids: List[str]
) -> Dict[str, Any]:
    """
    Retrieves available booking windows based on service and location.

    Args:
        start_date: The start date for availability search (YYYY-MM-DD).
        end_date: The end date for availability search (YYYY-MM-DD).
        address: The address for the job.
        service_ids: A list of service IDs to be scheduled.

    Returns:
        A dictionary containing available booking windows.
    """
    headers = get_headers()
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "address": address,
        "service_ids": ",".join(service_ids),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/schedules/booking-windows", headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run() 