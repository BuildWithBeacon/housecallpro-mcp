#!/usr/bin/env python3
"""
Housecall Pro Price Forms MCP Server

This server provides price forms functionality for Housecall Pro,
including creating price forms for leads.
"""

import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Price Forms")

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
async def create_price_form(
    lead_id: str,
    customer_name: str,
    customer_phone_number: Optional[str] = None,
    customer_email: Optional[str] = None,
    line_items: Optional[List[Dict[str, Any]]] = None,
    expiration_date: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new price form for a customer.
    
    Args:
        lead_id: The ID of the lead to create the price form for (required)
        customer_name: Name of the customer (required)
        customer_phone_number: Phone number of the customer
        customer_email: Email address of the customer  
        line_items: List of line items to include in the price form
                   Each item should have: material_id, quantity, unit_price
        expiration_date: When the price form expires (ISO 8601 format)
        notes: Additional notes for the price form
    
    Returns:
        Dict containing the created price form data
    
    Raises:
        ValueError: If required parameters are missing or invalid
        httpx.HTTPStatusError: If the API request fails
    """
    # Input validation
    if not lead_id or not lead_id.strip():
        raise ValueError("lead_id is required and cannot be empty")
    
    if not customer_name or not customer_name.strip():
        raise ValueError("customer_name is required and cannot be empty")
    
    # Prepare the request data
    price_form_data = {
        "lead_id": lead_id.strip(),
        "customer_name": customer_name.strip(),
    }
    
    if customer_phone_number:
        price_form_data["customer_phone_number"] = customer_phone_number.strip()
    
    if customer_email:
        price_form_data["customer_email"] = customer_email.strip()
    
    if line_items:
        price_form_data["line_items"] = line_items
    
    if expiration_date:
        price_form_data["expiration_date"] = expiration_date
    
    if notes:
        price_form_data["notes"] = notes.strip()
    
    try:
        result = await make_api_request(
            method="POST",
            endpoint="/price_forms",
            json_data=price_form_data
        )
        return {
            "success": True,
            "data": result,
            "message": f"Price form created successfully for customer '{customer_name}'"
        }
    except httpx.HTTPStatusError as e:
        error_detail = "Unknown error"
        try:
            error_response = e.response.json()
            error_detail = error_response.get("message", str(e))
        except:
            error_detail = str(e)
        
        return {
            "success": False,
            "error": f"Failed to create price form: {error_detail}",
            "status_code": e.response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error creating price form: {str(e)}"
        }


if __name__ == "__main__":
    mcp.run() 