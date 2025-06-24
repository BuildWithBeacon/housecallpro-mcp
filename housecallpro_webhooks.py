#!/usr/bin/env python3
"""
Housecall Pro Webhooks MCP Server

This server provides webhook management functionality for Housecall Pro,
including creating and deleting webhook subscriptions.
"""

import os
from typing import Optional, Dict, Any, List
import re

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Webhooks")

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


@mcp.tool()
async def create_webhook_subscription(
    url: str,
    events: List[str],
    description: Optional[str] = None,
    is_active: Optional[bool] = True
) -> dict:
    """
    Create a new webhook subscription.
    
    Args:
        url: The URL where webhook events will be sent (required)
        events: List of event types to subscribe to (required)
        description: Optional description for the webhook subscription
        is_active: Whether the webhook subscription is active (default: true)
    
    Available event types include:
        - appointment.created
        - appointment.updated
        - appointment.deleted
        - job.created
        - job.updated
        - job.completed
        - customer.created
        - customer.updated
        - estimate.created
        - estimate.updated
        - invoice.created
        - invoice.updated
        - lead.created
        - lead.updated
    
    Returns:
        Dictionary containing created webhook subscription data or error message
    """
    try:
        if not url or not url.strip():
            return {"error": "url is required and cannot be empty"}
        
        if not events or len(events) == 0:
            return {"error": "events list is required and cannot be empty"}
        
        # Validate URL format (basic check)
        if not url.startswith(('http://', 'https://')):
            return {"error": "url must be a valid HTTP or HTTPS URL"}
        
        webhook_data = {
            "url": url.strip(),
            "events": events
        }
        
        if description is not None:
            webhook_data["description"] = description.strip()
        
        if is_active is not None:
            webhook_data["is_active"] = is_active
        
        result = await make_api_request("POST", "/webhooks", data=webhook_data)
        return result
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def delete_webhook_subscription(
    webhook_id: str
) -> dict:
    """
    Delete a webhook subscription.
    
    Args:
        webhook_id: The unique identifier of the webhook subscription to delete (required)
    
    Returns:
        Dictionary containing success confirmation or error message
    """
    try:
        if not webhook_id or not webhook_id.strip():
            return {"error": "webhook_id is required and cannot be empty"}
        
        result = await make_api_request("DELETE", f"/webhooks/{webhook_id.strip()}")
        return result
        
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run() 