# GoodStewards Treasurer Dashboard UX

## 1. Document Purpose

This document provides a comprehensive plan for the user experience (UX) and user flows for the Treasurer Dashboard. This web-based application is the central hub for designated treasurers to manage their organization's finances, review submissions, and generate state tax refund reports.

## 2. Target Persona

### The Non-Profit Treasurer

*   **Who they are:** The financial administrator for the non-profit, often a volunteer. They are responsible for collecting all receipts, ensuring compliance, managing reimbursements, and filing for tax refunds.
*   **Core Motivation:** To maximize the organization's tax refund by capturing every eligible expense, while minimizing the administrative burden on themselves and the members.
*   **Key Pain Points:**
    *   Chasing members for physical receipts.
    *   Manually entering data from dozens or hundreds of receipts is tedious, time-consuming, and error-prone.
    *   Keeping track of which receipts have been approved, rejected, or reimbursed.
    *   The process of filling out the state-specific tax forms (like the E-585) is complex and requires careful data aggregation.
*   **Primary Goals:**
    *   A centralized dashboard to see the organization's financial health at a glance.
    *   A fast, streamlined way to review and approve member submissions.
    *   A one-click process to generate accurate, ready-to-file tax reports.
    *   A simple way to manage the organization's members.

## 3. UI/UX Principles

*   **Clarity & Simplicity:** The interface must be clean, with clear labels and intuitive navigation. Financial data should be presented in an easily understandable way.
*   **Efficiency & Speed:** Workflows are designed to minimize clicks and streamline the most common and repetitive tasks, like receipt approval.
*   **Data-Driven:** Key financial data is front and center, empowering treasurers to make informed decisions and track progress toward their refund goals.
*   **Responsive Design:** The dashboard must be fully functional and easy to use on desktops, tablets, and mobile devices, allowing treasurers to work from anywhere.

## 4. Screen-by-Screen Breakdown & Mockups

### Screen A: The Main Dashboard (Financial Overview)

*   **Purpose:** To provide an at-a-glance summary of the organization's financial status and highlight urgent tasks.
*   **Key Elements:** Data widgets for key metrics, a primary call-to-action to review pending receipts, and a feed of recent activity.

```ascii
+------------------------------------------------------------------------------------------------+
| Treasurer Dashboard: [Hope Foundation]                                          [User Avatar]  |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|  +---------------------------+  +---------------------------+  +----------------------------+   |
|  | Current Estimated Refund  |  | Approved (Ready to Pay)   |  | YTD Refund Received        |   |
|  |      $1,234.56            |  |      $5,678.90            |  |      $9,876.54             |   |
|  +---------------------------+  +---------------------------+  +----------------------------+   |
|                                                                                                |
|  You have 15 receipts pending review. [ Review Now ]                                           |
|                                                                                                |
|  +--------------------------------------------------+  +-------------------------------------+ |
|  | Refund Progress (Quarterly Goal: $2,000)         |  | Recent Activity                     | |
|  |                                                  |  | ----------------------------------- | |
|  |  [|||||||||||||||||||     ] 62%                  |  | J. Doe submitted receipt for $25.50 | |
|  |                                                  |  | Receipt #123 (Staples) approved     | |
|  |                                                  |  | E-585 Report (Q2) generated         | |
|  +--------------------------------------------------+  +-------------------------------------+ |
+------------------------------------------------------------------------------------------------+
```

### Screen B: Receipt Management (Pending Queue)

*   **Purpose:** To provide a dedicated, efficient interface for reviewing and processing all member-submitted receipts.
*   **Key Elements:** A table-based queue of pending receipts with key information. Tabs allow switching between Pending, Approved, and Rejected views.

```ascii
+------------------------------------------------------------------------------------------------+
| < Back      Receipt Management                                                                 |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|  [ Pending (15) ]  [ Approved ]  [ Rejected ]   Search: [ Staples... ]  Filter by Member: [All v] |
|                                                                                                |
|  |--------------------|------------|------------------|------------|----------|--------------| |
|  | MEMBER             | DATE       | VENDOR           | CATEGORY   | AMOUNT   | ACTION       | |
|  |--------------------|------------|------------------|------------|----------|--------------| |
|  | John Doe           | 2025-07-22 | Staples          | Supplies   | $45.21   | [ Review ]   | |
|  | Jane Smith         | 2025-07-22 | Home Depot       | Materials  | $112.89  | [ Review ]   | |
|  | John Doe           | 2025-07-21 | Costco           | Groceries  | $250.10  | [ Review ]   | |
|  | ...                | ...        | ...              | ...        | ...      | ...          | |
|  |--------------------|------------|------------------|------------|----------|--------------| |
|                                                                                                |
+------------------------------------------------------------------------------------------------+
```

### Screen C: Receipt Detail & Approval View

*   **Purpose:** To allow the treasurer to view a receipt image alongside the AI-extracted data, make corrections, and approve or reject it.
*   **Key Elements:** A two-panel layout. The left panel displays the receipt image, zoomable. The right panel contains the editable data fields and action buttons.

```ascii
+------------------------------------------------------------------------------------------------+
| < Back to Queue      Reviewing Receipt from John Doe                                           |
+------------------------------------------------------------------------------------------------+
|  +--------------------------------------------------+  +-------------------------------------+ |
|  |                                                  |  | Vendor: [ Staples               ]   | |
|  |                                                  |  | Date:   [ 2025-07-22            ]   | |
|  |                                                  |  | ----------------------------------- | |
|  |                                                  |  | Subtotal:  [ 42.00              ]   | |
|  |  [   Uploaded Receipt Image   ]                  |  | Sales Tax: [ 3.21               ]   | |
|  |  [       (Zoomable)         ]                  |  | Total:     [ 45.21              ]   | |
|  |                                                  |  | ----------------------------------- | |
|  |                                                  |  | Category: [ Office Supplies  v ]   | |
|  |                                                  |  | Notes:    [ Printer paper...    ]   | |
|  |                                                  |  |                                     | |
|  |                                                  |  | [ Reject ]       [ Approve ]        | |
|  +--------------------------------------------------+  +-------------------------------------+ |
+------------------------------------------------------------------------------------------------+
```

### Screen D: Report Generation

*   **Purpose:** To provide a simple, one-click process for generating the official E-585 and supplementary tax forms.
*   **Key Elements:** Date range selectors and a clear "Generate" button. After generation, it provides download links for the completed PDF forms.

```ascii
+------------------------------------------------------------------------------------------------+
| < Back      Report Generation                                                                  |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|  Generate E-585 Sales Tax Refund Report                                                        |
|  --------------------------------------------------------------------------------------------  |
|                                                                                                |
|  Select a reporting period:                                                                    |
|                                                                                                |
|  Start Date: [ 2025-04-01 ]   End Date: [ 2025-06-30 ]                                          |
|                                                                                                |
|  [ Generate Report for Q2 2025 ]                                                               |
|                                                                                                |
|  --------------------------------------------------------------------------------------------  |
|  Previous Reports:                                                                             |
|  - Q1 2025 Report (Generated on 2025-04-05) [ Download PDF ]                                   |
|  - Q4 2024 Report (Generated on 2025-01-08) [ Download PDF ]                                   |
|                                                                                                |
+------------------------------------------------------------------------------------------------+
```