#!/usr/bin/env python3
"""
Housecall Pro Customers MCP Server

This server provides customer management functionality for Housecall Pro,
including CRUD operations for customers and their addresses.
"""

import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Customers")

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


async def make_api_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Make an API request to Housecall Pro."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = get_headers()
    
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()


# CUSTOMER ENDPOINTS

@mcp.tool()
async def get_customers(
    page: Optional[int] = 1,
    per_page: Optional[int] = 20,
    search: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    company_name: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    tags: Optional[str] = None,
    created_start: Optional[str] = None,
    created_end: Optional[str] = None,
    updated_start: Optional[str] = None,
    updated_end: Optional[str] = None
) -> dict:
    """
    Get a list of customers with optional filtering.
    
    Args:
        page: Page number (default: 1)
        per_page: Number of customers per page (default: 20, max: 200)
        search: Search term for customer name, email, or phone
        email: Filter by customer email
        phone: Filter by customer phone number
        company_name: Filter by company name
        first_name: Filter by first name
        last_name: Filter by last name
        tags: Filter by customer tags (comma-separated)
        created_start: Filter by creation date start (ISO 8601 format)
        created_end: Filter by creation date end (ISO 8601 format)
        updated_start: Filter by update date start (ISO 8601 format)
        updated_end: Filter by update date end (ISO 8601 format)
    """
    params = {
        "page": page,
        "per_page": per_page,
        "search": search,
        "email": email,
        "phone": phone,
        "company_name": company_name,
        "first_name": first_name,
        "last_name": last_name,
        "tags": tags,
        "created_start": created_start,
        "created_end": created_end,
        "updated_start": updated_start,
        "updated_end": updated_end
    }
    
    # Remove None values from params
    clean_params = {k: v for k, v in params.items() if v is not None}
    
    return await make_api_request("GET", "/customers", params=clean_params)


@mcp.tool()
async def get_customer(customer_id: str) -> dict:
    """
    Get a specific customer by ID.
    
    Args:
        customer_id: The unique identifier for the customer
    """
    try:
        return await make_api_request("GET", f"/customers/{customer_id}")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"error": f"Customer {customer_id} not found"}
        raise


@mcp.tool()
async def create_customer(
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    mobile_number: Optional[str] = None,
    home_number: Optional[str] = None,
    work_number: Optional[str] = None,
    company_name: Optional[str] = None,
    is_commercial: Optional[bool] = False,
    notifications_enabled: Optional[bool] = True,
    lead_source: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Create a new customer.
    
    Args:
        first_name: Customer's first name (required)
        last_name: Customer's last name (required)
        email: Customer's email address
        mobile_number: Customer's mobile phone number
        home_number: Customer's home phone number
        work_number: Customer's work phone number
        company_name: Company name for commercial customers
        is_commercial: Whether this is a commercial customer (default: False)
        notifications_enabled: Whether notifications are enabled (default: True)
        lead_source: How the customer was acquired
        tags: List of tags to assign to the customer
        notes: Notes about the customer
    """
    customer_data = {
        "first_name": first_name,
        "last_name": last_name
    }
    
    # Add optional fields if provided
    if email:
        customer_data["email"] = email
    if mobile_number:
        customer_data["mobile_number"] = mobile_number
    if home_number:
        customer_data["home_number"] = home_number
    if work_number:
        customer_data["work_number"] = work_number
    if company_name:
        customer_data["company_name"] = company_name
    if is_commercial is not None:
        customer_data["is_commercial"] = is_commercial
    if notifications_enabled is not None:
        customer_data["notifications_enabled"] = notifications_enabled
    if lead_source:
        customer_data["lead_source"] = lead_source
    if tags:
        customer_data["tags"] = tags
    if notes:
        customer_data["notes"] = notes
    
    return await make_api_request("POST", "/customers", json=customer_data)


@mcp.tool()
async def update_customer(
    customer_id: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    mobile_number: Optional[str] = None,
    home_number: Optional[str] = None,
    work_number: Optional[str] = None,
    company_name: Optional[str] = None,
    is_commercial: Optional[bool] = None,
    notifications_enabled: Optional[bool] = None,
    lead_source: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: Optional[str] = None
) -> dict:
    """
    Update an existing customer.
    
    Args:
        customer_id: The unique identifier for the customer (required)
        first_name: Customer's first name
        last_name: Customer's last name
        email: Customer's email address
        mobile_number: Customer's mobile phone number
        home_number: Customer's home phone number
        work_number: Customer's work phone number
        company_name: Company name for commercial customers
        is_commercial: Whether this is a commercial customer
        notifications_enabled: Whether notifications are enabled
        lead_source: How the customer was acquired
        tags: List of tags to assign to the customer
        notes: Notes about the customer
    """
    customer_data = {}
    
    # Add fields that are provided (not None)
    if first_name is not None:
        customer_data["first_name"] = first_name
    if last_name is not None:
        customer_data["last_name"] = last_name
    if email is not None:
        customer_data["email"] = email
    if mobile_number is not None:
        customer_data["mobile_number"] = mobile_number
    if home_number is not None:
        customer_data["home_number"] = home_number
    if work_number is not None:
        customer_data["work_number"] = work_number
    if company_name is not None:
        customer_data["company_name"] = company_name
    if is_commercial is not None:
        customer_data["is_commercial"] = is_commercial
    if notifications_enabled is not None:
        customer_data["notifications_enabled"] = notifications_enabled
    if lead_source is not None:
        customer_data["lead_source"] = lead_source
    if tags is not None:
        customer_data["tags"] = tags
    if notes is not None:
        customer_data["notes"] = notes
    
    return await make_api_request("PUT", f"/customers/{customer_id}", json=customer_data)


@mcp.tool()
async def get_customer_addresses(customer_id: str) -> dict:
    """
    Get all addresses for a specific customer.
    
    Args:
        customer_id: The unique identifier for the customer
    """
    return await make_api_request("GET", f"/customers/{customer_id}/addresses")


@mcp.tool()
async def get_customer_address(customer_id: str, address_id: str) -> dict:
    """
    Get a specific address for a customer.
    
    Args:
        customer_id: The unique identifier for the customer
        address_id: The unique identifier for the address
    """
    try:
        return await make_api_request("GET", f"/customers/{customer_id}/addresses/{address_id}")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"error": f"Address {address_id} not found for customer {customer_id}"}
        raise


@mcp.tool()
async def create_customer_address(
    customer_id: str,
    street: str,
    city: str,
    state: str,
    zip: str,
    country: Optional[str] = "US",
    type: Optional[str] = "service",
    notes: Optional[str] = None,
    contact_name: Optional[str] = None,
    contact_phone: Optional[str] = None,
    is_primary: Optional[bool] = False
) -> dict:
    """
    Create a new address for a customer.
    
    Args:
        customer_id: The unique identifier for the customer (required)
        street: Street address (required)
        city: City (required)
        state: State (required)
        zip: ZIP code (required)
        country: Country code (default: "US")
        type: Address type (e.g., "service", "billing") (default: "service")
        notes: Notes about the address
        contact_name: Contact person at this address
        contact_phone: Contact phone for this address
        is_primary: Whether this is the primary address (default: False)
    """
    address_data = {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip,
        "country": country,
        "type": type,
        "is_primary": is_primary
    }
    
    # Add optional fields if provided
    if notes:
        address_data["notes"] = notes
    if contact_name:
        address_data["contact_name"] = contact_name
    if contact_phone:
        address_data["contact_phone"] = contact_phone
    
    return await make_api_request("POST", f"/customers/{customer_id}/addresses", json=address_data)


# Run the server
if __name__ == "__main__":
    mcp.run() 