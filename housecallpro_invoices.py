#!/usr/bin/env python3
"""
Housecall Pro Invoices MCP Server

This server provides invoice management functionality for Housecall Pro,
including CRUD operations for invoices.
"""

import json
import os
from typing import Optional, Dict, Any, List

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# FastMCP server
mcp = FastMCP("Housecall Pro Invoices")

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


# Invoice Management Tools

@mcp.tool()
async def get_job_invoices(
    job_id: str,
    include_line_items: Optional[bool] = None,
    include_attachments: Optional[bool] = None
) -> str:
    """
    Retrieve all invoices for a specific job.
    
    Args:
        job_id: The ID of the job to get invoices for
        include_line_items: Include line items in the response
        include_attachments: Include attachments in the response
    """
    params = {}
    
    if include_line_items is not None:
        params["include_line_items"] = str(include_line_items).lower()
    if include_attachments is not None:
        params["include_attachments"] = str(include_attachments).lower()
    
    try:
        result = make_api_request("GET", f"/jobs/{job_id}/invoices", params=params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting job invoices: {str(e)}"


@mcp.tool()
async def get_invoices(
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    due_date_start: Optional[str] = None,
    due_date_end: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    updated_after: Optional[str] = None,
    updated_before: Optional[str] = None,
    sent: Optional[bool] = None,
    past_due: Optional[bool] = None,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    include_line_items: Optional[bool] = None,
    include_attachments: Optional[bool] = None
) -> str:
    """
    Retrieve a list of invoices with optional filtering.
    
    Args:
        customer_id: Filter by customer ID
        status: Filter by invoice status (open, paid, voided, etc.)
        due_date_start: Start date filter for due dates (YYYY-MM-DD format)
        due_date_end: End date filter for due dates (YYYY-MM-DD format)
        created_after: Return invoices created after this date (ISO 8601)
        created_before: Return invoices created before this date (ISO 8601)
        updated_after: Return invoices updated after this date (ISO 8601)
        updated_before: Return invoices updated before this date (ISO 8601)
        sent: Filter by whether invoice has been sent to customer
        past_due: Filter by whether invoice is past due
        page: Page number to retrieve
        page_size: Number of results per page (default 25, max 100)
        sort_by: Field to sort by (created_at, due_date, amount, etc.)
        sort_direction: Sort direction (asc or desc)
        include_line_items: Include line items in response
        include_attachments: Include attachments in response
    """
    params = {}
    
    if customer_id:
        params["customer_id"] = customer_id
    if status:
        params["status"] = status
    if due_date_start:
        params["due_date_start"] = due_date_start
    if due_date_end:
        params["due_date_end"] = due_date_end
    if created_after:
        params["created_after"] = created_after
    if created_before:
        params["created_before"] = created_before
    if updated_after:
        params["updated_after"] = updated_after
    if updated_before:
        params["updated_before"] = updated_before
    if sent is not None:
        params["sent"] = str(sent).lower()
    if past_due is not None:
        params["past_due"] = str(past_due).lower()
    if page:
        params["page"] = page
    if page_size:
        params["page_size"] = page_size
    if sort_by:
        params["sort_by"] = sort_by
    if sort_direction:
        params["sort_direction"] = sort_direction
    if include_line_items is not None:
        params["include_line_items"] = str(include_line_items).lower()
    if include_attachments is not None:
        params["include_attachments"] = str(include_attachments).lower()
    
    try:
        result = make_api_request("GET", "/invoices", params=params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoices: {str(e)}"


@mcp.tool()
async def get_invoice_by_id(
    invoice_id: str,
    include_line_items: Optional[bool] = None,
    include_attachments: Optional[bool] = None
) -> str:
    """
    Get detailed information about a specific invoice.
    
    Args:
        invoice_id: The ID of the invoice to retrieve
        include_line_items: Include line items in the response
        include_attachments: Include attachments in the response
    """
    params = {}
    
    if include_line_items is not None:
        params["include_line_items"] = str(include_line_items).lower()
    if include_attachments is not None:
        params["include_attachments"] = str(include_attachments).lower()
    
    try:
        result = make_api_request("GET", f"/invoices/{invoice_id}", params=params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoice: {str(e)}"


@mcp.tool()
async def create_invoice(
    job_id: str,
    amount: Optional[float] = None,
    due_date: Optional[str] = None,
    due_terms: Optional[str] = None,
    message: Optional[str] = None,
    notes: Optional[str] = None,
    payment_methods: Optional[List[str]] = None,
    send_immediately: Optional[bool] = None,
    include_line_items: Optional[bool] = None
) -> str:
    """
    Create a new invoice for a job.
    
    Args:
        job_id: The ID of the job to create an invoice for
        amount: Invoice amount (if not specified, uses full job amount)
        due_date: Invoice due date (YYYY-MM-DD format)
        due_terms: Payment terms (net_15, net_30, due_on_completion, etc.)
        message: Message to include on the invoice
        notes: Internal notes for the invoice
        payment_methods: List of accepted payment methods
        send_immediately: Whether to send the invoice immediately
        include_line_items: Whether to include job line items
    """
    invoice_data = {"job_id": job_id}
    
    if amount is not None:
        invoice_data["amount"] = amount
    if due_date:
        invoice_data["due_date"] = due_date
    if due_terms:
        invoice_data["due_terms"] = due_terms
    if message:
        invoice_data["message"] = message
    if notes:
        invoice_data["notes"] = notes
    if payment_methods:
        invoice_data["payment_methods"] = payment_methods
    if send_immediately is not None:
        invoice_data["send_immediately"] = send_immediately
    if include_line_items is not None:
        invoice_data["include_line_items"] = include_line_items
    
    try:
        result = make_api_request("POST", "/invoices", json_data=invoice_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error creating invoice: {str(e)}"


@mcp.tool()
async def update_invoice(
    invoice_id: str,
    amount: Optional[float] = None,
    due_date: Optional[str] = None,
    due_terms: Optional[str] = None,
    message: Optional[str] = None,
    notes: Optional[str] = None,
    payment_methods: Optional[List[str]] = None
) -> str:
    """
    Update an existing invoice.
    
    Args:
        invoice_id: The ID of the invoice to update
        amount: Updated invoice amount
        due_date: Updated due date (YYYY-MM-DD format)
        due_terms: Updated payment terms
        message: Updated message on the invoice
        notes: Updated internal notes
        payment_methods: Updated accepted payment methods
    """
    update_data = {}
    
    if amount is not None:
        update_data["amount"] = amount
    if due_date:
        update_data["due_date"] = due_date
    if due_terms:
        update_data["due_terms"] = due_terms
    if message:
        update_data["message"] = message
    if notes:
        update_data["notes"] = notes
    if payment_methods:
        update_data["payment_methods"] = payment_methods
    
    try:
        result = make_api_request("PATCH", f"/invoices/{invoice_id}", json_data=update_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error updating invoice: {str(e)}"


@mcp.tool()
async def send_invoice(
    invoice_id: str,
    delivery_method: str = "email",
    message: Optional[str] = None,
    include_attachments: Optional[bool] = None
) -> str:
    """
    Send an invoice to the customer.
    
    Args:
        invoice_id: The ID of the invoice to send
        delivery_method: How to send the invoice (email, sms, print)
        message: Custom message to include with the invoice
        include_attachments: Whether to include job attachments
    """
    send_data = {"delivery_method": delivery_method}
    
    if message:
        send_data["message"] = message
    if include_attachments is not None:
        send_data["include_attachments"] = include_attachments
    
    try:
        result = make_api_request("POST", f"/invoices/{invoice_id}/send", json_data=send_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error sending invoice: {str(e)}"


@mcp.tool()
async def void_invoice(
    invoice_id: str,
    reason: Optional[str] = None
) -> str:
    """
    Void an invoice (makes it unpayable).
    
    Args:
        invoice_id: The ID of the invoice to void
        reason: Reason for voiding the invoice
    """
    void_data = {}
    
    if reason:
        void_data["reason"] = reason
    
    try:
        result = make_api_request("POST", f"/invoices/{invoice_id}/void", json_data=void_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error voiding invoice: {str(e)}"


@mcp.tool()
async def mark_invoice_paid(
    invoice_id: str,
    amount_paid: float,
    payment_method: str = "cash",
    payment_date: Optional[str] = None,
    reference_number: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Mark an invoice as paid.
    
    Args:
        invoice_id: The ID of the invoice to mark as paid
        amount_paid: Amount that was paid
        payment_method: Method of payment (cash, check, credit_card, ach, etc.)
        payment_date: Date payment was received (YYYY-MM-DD format)
        reference_number: Payment reference number
        notes: Payment notes
    """
    payment_data = {
        "amount_paid": amount_paid,
        "payment_method": payment_method
    }
    
    if payment_date:
        payment_data["payment_date"] = payment_date
    if reference_number:
        payment_data["reference_number"] = reference_number
    if notes:
        payment_data["notes"] = notes
    
    try:
        result = make_api_request("POST", f"/invoices/{invoice_id}/payments", json_data=payment_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error marking invoice as paid: {str(e)}"


@mcp.tool()
async def get_invoice_payments(invoice_id: str) -> str:
    """
    Get all payments for a specific invoice.
    
    Args:
        invoice_id: The ID of the invoice to get payments for
    """
    try:
        result = make_api_request("GET", f"/invoices/{invoice_id}/payments")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoice payments: {str(e)}"


@mcp.tool()
async def download_invoice_pdf(
    invoice_id: str,
    include_attachments: Optional[bool] = None
) -> str:
    """
    Get a download URL for the invoice PDF.
    
    Args:
        invoice_id: The ID of the invoice to download
        include_attachments: Whether to include job attachments in PDF
    """
    params = {}
    
    if include_attachments is not None:
        params["include_attachments"] = str(include_attachments).lower()
    
    try:
        result = make_api_request("GET", f"/invoices/{invoice_id}/download", params=params)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoice download URL: {str(e)}"


@mcp.tool()
async def get_invoice_line_items(invoice_id: str) -> str:
    """
    Get line items for a specific invoice.
    
    Args:
        invoice_id: The ID of the invoice to get line items for
    """
    try:
        result = make_api_request("GET", f"/invoices/{invoice_id}/line_items")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoice line items: {str(e)}"


@mcp.tool()
async def add_invoice_line_item(
    invoice_id: str,
    name: str,
    quantity: float,
    price: float,
    unit: Optional[str] = None,
    description: Optional[str] = None,
    sku: Optional[str] = None,
    taxable: Optional[bool] = None
) -> str:
    """
    Add a line item to an invoice.
    
    Args:
        invoice_id: The ID of the invoice to add line item to
        name: Name of the line item
        quantity: Quantity of the item
        price: Price per unit
        unit: Unit of measurement
        description: Description of the line item
        sku: SKU or product code
        taxable: Whether the item is taxable
    """
    line_item_data = {
        "name": name,
        "quantity": quantity,
        "price": price
    }
    
    if unit:
        line_item_data["unit"] = unit
    if description:
        line_item_data["description"] = description
    if sku:
        line_item_data["sku"] = sku
    if taxable is not None:
        line_item_data["taxable"] = taxable
    
    try:
        result = make_api_request("POST", f"/invoices/{invoice_id}/line_items", json_data=line_item_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error adding invoice line item: {str(e)}"


@mcp.tool()
async def update_invoice_line_item(
    invoice_id: str,
    line_item_id: str,
    name: Optional[str] = None,
    quantity: Optional[float] = None,
    price: Optional[float] = None,
    unit: Optional[str] = None,
    description: Optional[str] = None,
    sku: Optional[str] = None,
    taxable: Optional[bool] = None
) -> str:
    """
    Update a line item on an invoice.
    
    Args:
        invoice_id: The ID of the invoice
        line_item_id: The ID of the line item to update
        name: Updated name of the line item
        quantity: Updated quantity
        price: Updated price per unit
        unit: Updated unit of measurement
        description: Updated description
        sku: Updated SKU or product code
        taxable: Updated taxable status
    """
    update_data = {}
    
    if name:
        update_data["name"] = name
    if quantity is not None:
        update_data["quantity"] = quantity
    if price is not None:
        update_data["price"] = price
    if unit:
        update_data["unit"] = unit
    if description:
        update_data["description"] = description
    if sku:
        update_data["sku"] = sku
    if taxable is not None:
        update_data["taxable"] = taxable
    
    try:
        result = make_api_request("PATCH", f"/invoices/{invoice_id}/line_items/{line_item_id}", json_data=update_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error updating invoice line item: {str(e)}"


@mcp.tool()
async def delete_invoice_line_item(
    invoice_id: str,
    line_item_id: str
) -> str:
    """
    Delete a line item from an invoice.
    
    Args:
        invoice_id: The ID of the invoice
        line_item_id: The ID of the line item to delete
    """
    try:
        result = make_api_request("DELETE", f"/invoices/{invoice_id}/line_items/{line_item_id}")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error deleting invoice line item: {str(e)}"


@mcp.tool()
async def get_invoice_attachments(invoice_id: str) -> str:
    """
    Get attachments for a specific invoice.
    
    Args:
        invoice_id: The ID of the invoice to get attachments for
    """
    try:
        result = make_api_request("GET", f"/invoices/{invoice_id}/attachments")
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting invoice attachments: {str(e)}"


@mcp.tool()
async def add_invoice_attachment(
    invoice_id: str,
    name: str,
    file_data: str,
    content_type: str = "application/octet-stream"
) -> str:
    """
    Add an attachment to an invoice.
    
    Args:
        invoice_id: The ID of the invoice to add attachment to
        name: Name of the attachment
        file_data: Base64 encoded file data
        content_type: MIME type of the file
    """
    attachment_data = {
        "name": name,
        "file_data": file_data,
        "content_type": content_type
    }
    
    try:
        result = make_api_request("POST", f"/invoices/{invoice_id}/attachments", json_data=attachment_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error adding invoice attachment: {str(e)}"


if __name__ == "__main__":
    mcp.run() 