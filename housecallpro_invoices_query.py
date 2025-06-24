#!/usr/bin/env python3
"""
Housecall Pro Invoices Query MCP Server

This server provides advanced invoice querying functionality for Housecall Pro,
allowing for filtering and sorting of invoices.
"""

import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Invoices Query")

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


def make_api_request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """Make an API request to Housecall Pro."""
    url = f"{API_BASE_URL}{endpoint}"
    headers = get_headers()
    
    with httpx.Client() as client:
        response = client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_invoices(
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    customer_id: Optional[str] = None,
    job_id: Optional[str] = None,
    status: Optional[str] = None,
    number: Optional[str] = None,
    invoice_date_start: Optional[str] = None,
    invoice_date_end: Optional[str] = None,
    due_date_start: Optional[str] = None,
    due_date_end: Optional[str] = None,
    paid_date_start: Optional[str] = None,
    paid_date_end: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Retrieves a list of invoices with extensive filtering and sorting options.

    Args:
        page: The page number to retrieve.
        page_size: The number of invoices per page.
        customer_id: Filter by customer ID.
        job_id: Filter by job ID.
        status: Filter by status (DRAFT, SENT, PAID, BAD_DEBT).
        number: Filter by invoice number.
        invoice_date_start: Start of invoice date range (YYYY-MM-DD).
        invoice_date_end: End of invoice date range (YYYY-MM-DD).
        due_date_start: Start of due date range (YYYY-MM-DD).
        due_date_end: End of due date range (YYYY-MM-DD).
        paid_date_start: Start of paid date range (YYYY-MM-DD).
        paid_date_end: End of paid date range (YYYY-MM-DD).
        sort_by: Field to sort by (invoice_date, due_date, etc.).
        sort_dir: Sort direction (asc, desc).

    Returns:
        A dictionary containing a list of invoices and pagination info.
    """
    params = {
        k: v
        for k, v in {
            "page": page,
            "page_size": page_size,
            "customer_id": customer_id,
            "job_id": job_id,
            "status": status,
            "number": number,
            "invoice_date_start": invoice_date_start,
            "invoice_date_end": invoice_date_end,
            "due_date_start": due_date_start,
            "due_date_end": due_date_end,
            "paid_date_start": paid_date_start,
            "paid_date_end": paid_date_end,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
        }.items()
        if v is not None
    }

    return make_api_request("GET", "/v1/invoices", params=params)


if __name__ == "__main__":
    mcp.run() 