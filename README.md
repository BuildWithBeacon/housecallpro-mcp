# 🏠 Housecall Pro MCP Servers

A comprehensive collection of **Model Context Protocol (MCP) servers** for the Housecall Pro API, enabling Claude Desktop and other LLM with MCP capability to seamlessly interact with your Housecall Pro field service management system. Each server is specialized for a specific domain, providing modular access to customers, jobs, scheduling, invoicing, materials, and more.

## 🚀 Overview

This project provides **20+ specialized MCP servers** that expose the full Housecall Pro API through Claude Desktop or other LLMs. Whether you're managing customers, scheduling jobs, processing invoices, or tracking materials, these servers give you powerful AI-assisted access to your field service operations.

## 🏗️ Architecture

Each Housecall Pro API domain has its own dedicated MCP server for focused, efficient operations:

### 📋 Core Business Operations
- **`housecallpro_customers.py`** - Customer & address management
- **`housecallpro_jobs.py`** - Job management, scheduling & dispatch
- **`housecallpro_employees.py`** - Employee management & filtering
- **`housecallpro_appointments.py`** - Appointment scheduling & status management

### 💰 Financial Management
- **`housecallpro_invoices.py`** - Invoice management & payments
- **`housecallpro_invoices_query.py`** - Advanced invoice querying
- **`housecallpro_job_invoices.py`** - Job-specific invoice operations
- **`housecallpro_estimates.py`** - Estimate creation & management

### 📦 Inventory & Materials
- **`housecallpro_materials.py`** - Materials management & pricing
- **`housecallpro_material_categories.py`** - Material category organization
- **`housecallpro_price_forms.py`** - Price book & form management

### 🎯 Sales & Marketing
- **`housecallpro_leads.py`** - Lead management & conversion
- **`housecallpro_lead_sources.py`** - Lead source tracking
- **`housecallpro_tags.py`** - Tag management & organization

### ⚙️ System & Configuration
- **`housecallpro_company.py`** - Company information & settings
- **`housecallpro_job_types.py`** - Job type configuration
- **`housecallpro_schedule.py`** - Schedule management
- **`housecallpro_events.py`** - Event & calendar management
- **`housecallpro_webhooks.py`** - Webhook configuration & management
- **`housecallpro_application.py`** - Application settings & preferences
- **`housecallpro.py`** - Unified server with core functionality

## 🌟 Key Features

### 📋 Customer Management (`housecallpro_customers.py`)

**Customer Operations**
- **Get Customers** - List customers with advanced filtering (search, date ranges, pagination)
- **Get Customer by ID** - Retrieve detailed customer profiles
- **Create Customer** - Add new customers with complete information
- **Update Customer** - Modify existing customer details

**Address Management**
- **Get Customer Addresses** - List all addresses for customers
- **Get Customer Address by ID** - Retrieve specific address details
- **Create Customer Address** - Add service locations to customers

### 👥 Employee Management (`housecallpro_employees.py`)

**Employee Operations**
- **Get Employees** - List employees with filtering by:
  - Active status, role, tags
  - Name, email, phone search
  - Custom pagination and sorting
- **Get Employee by ID** - Detailed employee profiles including:
  - Personal details (contact info, avatar)
  - Employment info (role, hire date, status)
  - Permissions and access levels
  - Tags and metadata

### 💼 Job Management (`housecallpro_jobs.py`)

**Core Job Operations**
- **Get Jobs** - Advanced job listing with filters for:
  - Status (scheduled, in_progress, completed, cancelled)
  - Customer, employee, date ranges
  - Job number, description, address search
  - Work status, business unit, tags
- **Get Job by ID** - Complete job details including line items, scheduling, attachments
- **Create Job** - Full job creation with customer assignment, scheduling, dispatch

**Job Scheduling & Dispatch**
- **Update Job Schedule** - Modify timing and appointments
- **Delete Job Schedule** - Remove scheduled appointments
- **Dispatch Job to Employees** - Assign technicians and crews

**Line Item Management**
- **Get/Add/Update/Delete Job Line Items** - Complete line item operations
- **Bulk Update Line Items** - Efficient batch updates
- **Get/Update Job Input Materials** - Material usage tracking

**Job Documentation**
- **Add Job Attachments** - Upload files, photos, documents
- **Add/Delete Job Notes** - Internal communication and tracking
- **Create Job Links** - External resource management
- **Add/Remove Job Tags** - Organization and categorization

### 📅 Appointment Management (`housecallpro_appointments.py`)

**Core Appointment Operations**
- **Get Appointments** - List with filtering by customer, employee, status, dates
- **Get Appointment by ID** - Detailed appointment information
- **Create/Update/Delete Appointments** - Full appointment lifecycle management

**Scheduling & Management**
- **Reschedule Appointment** - Move appointments with customer notifications
- **Get Appointment Availability** - Find available scheduling slots
- **Send Appointment Reminder** - Customer communication automation

**Status Management**
- **Mark Appointment Arrived/Started/Completed** - Real-time status tracking
- **Mark Appointment No Show** - Handle customer no-shows

### 💰 Invoice Management (`housecallpro_invoices.py`)

**Invoice Operations**
- **Get Invoices** - Advanced filtering by status, customer, dates, payment status
- **Get Invoice by ID** - Complete invoice details with line items and attachments
- **Create Invoice** - Generate invoices from jobs with custom terms
- **Update Invoice** - Modify amounts, due dates, terms, messages

**Payment & Processing**
- **Send Invoice** - Email/SMS delivery with custom messages
- **Mark Invoice Paid** - Record payments with multiple methods
- **Void Invoice** - Cancel invoices with reason tracking
- **Get Invoice Payments** - Payment history and tracking

**Line Item Management**
- **Add/Update/Delete Invoice Line Items** - Detailed invoice composition
- **Get Invoice Attachments** - Supporting documentation
- **Download Invoice PDF** - Generate formatted invoices

### 📦 Materials Management (`housecallpro_materials.py`)

**Material Operations**
- **Get Materials** - List materials by category with filtering
- **Get Material Categories** - Hierarchical category browsing
- **Find Category by Name** - Search category structures
- **Create/Update/Delete Materials** - Complete material lifecycle

### 💡 Estimate Management (`housecallpro_estimates.py`)

**Estimate Operations**
- **Get Estimates** - Filter by status, customer, employee, dates
- **Get Estimate by ID** - Complete estimate details with options
- **Create Estimate** - Generate estimates with multiple options

**Estimate Option Management**
- **Create Estimate Option Attachments/Links** - Supporting documentation
- **Update Estimate Option Schedule** - Timeline management
- **Create/Delete Estimate Option Notes** - Internal tracking

### 🎯 Lead Management (`housecallpro_leads.py`)

**Lead Operations**
- **Get Leads** - Advanced filtering by source, status, employee, dates
- **Get Lead by ID** - Complete lead information and history
- **Create Lead** - Capture new prospects with full details
- **Update Lead** - Modify lead information and status
- **Convert Lead** - Transform leads into customers

**Lead Communication**
- **Add Lead Note** - Track communications and follow-ups
- **Delete Lead Note** - Clean up lead history

### 🏷️ Organization & Tagging (`housecallpro_tags.py`)

**Tag Management**
- **Get Tags** - List all available tags with filtering
- **Get Tag by ID** - Detailed tag information
- **Create Tag** - Add new organizational tags
- **Update Tag** - Modify tag properties
- **Delete Tag** - Remove unused tags

### ⚙️ System Configuration

**Company Management (`housecallpro_company.py`)**
- **Get Company Info** - Business details and settings

**Job Types (`housecallpro_job_types.py`)**
- **Get Job Types** - List available service types with pricing

**Schedule Management (`housecallpro_schedule.py`)**
- **Get Schedule** - View technician schedules and availability

**Events (`housecallpro_events.py`)**
- **Get Events** - Calendar events and scheduling conflicts

**Webhooks (`housecallpro_webhooks.py`)**
- **Get/Create/Update/Delete Webhooks** - Real-time integration management

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- Housecall Pro API key
- Claude Desktop application or other MCP LLM client

## Setup Instructions

### 1. Install uv (if not already installed)

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup Project

```bash
git clone <your-repo-url>
cd HousecallPro-mcp
uv sync
```

### 3. Get Housecall Pro API Key

1. Log into your Housecall Pro account
2. Go to Settings > Integrations > API
3. Generate your API key
4. Copy your API key (keep it secure!)

### 4. Environment Setup

Create a `.env` file in the project root:

```env
HOUSECALL_PRO_API_KEY=your_api_key_here
```

### 5. Configure Claude Desktop

#### Copy the template:
```bash
cp claude_desktop.json.template claude_desktop_config.json
```

#### Update paths in `claude_desktop_config.json`:

> **Note**: The API key will be automatically read from your `.env` file - no need to include it in the JSON configuration.

> **Important**: If `uv` is not in your system PATH, replace `"uv"` with the full path to the uv executable (e.g., `"C:\\Users\\YourUsername\\.cargo\\bin\\uv.exe"` on Windows).

**Windows:**
```json
{
  "mcpServers": {
    "housecall-pro-customers": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\\\Users\\\\YourUsername\\\\path\\\\to\\\\HousecallPro-mcp",
        "run",
        "housecallpro_customers.py"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "housecall-pro-customers": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourusername/path/to/HousecallPro-mcp",
        "run",
        "housecallpro_customers.py"
      ]
    }
  }
}
```

### 6. Restart Claude Desktop

After configuring, restart Claude Desktop to load the new MCP server.

## 🔧 Testing the Server

Test the customers server directly:

```bash
uv run housecallpro_customers.py
```

## 📝 Usage Examples

Once configured, you can ask Claude things like:

- "Show me all customers"
- "Get customer details for ID 12345"
- "Create a new customer named John Doe"
- "List all addresses for customer 12345"
- "Add a new address for customer 12345"

## 🛠️ Troubleshooting

### Common Issues:

1. **"Server not found"**
   - Check that the path in `claude_desktop_config.json` is correct
   - Ensure `uv` is installed and accessible
   - If `uv` command not found, either:
     - Add `uv` to your system PATH, or
     - Use the full path to `uv` in the configuration (e.g., `C:\\Users\\YourUsername\\.cargo\\bin\\uv.exe` on Windows)

2. **"Authentication failed"**
   - Verify your API key in the `.env` file
   - Check that your Housecall Pro API key has the necessary permissions

3. **"Permission denied"**
   - Make sure the Python file is executable
   - Check that uv has proper permissions

### Debug Mode:

Run the server with debug output:
```bash
uv run housecallpro_customers.py --debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📄 License

[Add your license here]

## 🔗 Related Links

- [Housecall Pro API Documentation](https://docs.housecallpro.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop) 