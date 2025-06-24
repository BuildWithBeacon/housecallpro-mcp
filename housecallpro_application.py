#!/usr/bin/env python3
"""
Housecall Pro Application MCP Server

This server provides application management functionality for Housecall Pro,
including enabling and disabling application access.
"""

import os
from typing import Optional, Dict, Any
import json

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Application")

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


async def make_api_request(
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an API request to Housecall Pro."""
    url = f"{API_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=get_headers(),
                params=params,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return json.dumps({"error": f"HTTP error occurred: {str(e)}"}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"An error occurred: {str(e)}"}, indent=2)


@mcp.tool()
async def get_application() -> dict:
    """
    Retrieve application details and status.
    
    This endpoint returns information about the current application,
    including its status, configuration, and permissions.
    
    Returns:
        Dictionary containing application data or error message
    """
    try:
        result = await make_api_request("GET", "/application")
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def enable_application() -> dict:
    """
    Enable the application.
    
    This endpoint enables the application, allowing it to access
    Housecall Pro services and data according to its configured permissions.
    
    Returns:
        Dictionary containing success confirmation or error message
    """
    try:
        result = await make_api_request("POST", "/application/enable")
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def disable_application() -> dict:
    """
    Disable the application.
    
    This endpoint disables the application, preventing it from accessing
    Housecall Pro services and data. The application can be re-enabled later.
    
    Returns:
        Dictionary containing success confirmation or error message
    """
    try:
        result = await make_api_request("POST", "/application/disable")
        return result
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run() 