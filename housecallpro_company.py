#!/usr/bin/env python3
"""
Housecall Pro Company MCP Server

This server provides company information functionality for Housecall Pro.
"""

import os
from typing import Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Company")

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
async def get_company() -> Dict[str, Any]:
    """
    Retrieves the company information.

    Returns:
        A dictionary containing the company information.
    """
    headers = get_headers()
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/company", headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    mcp.run() 