# E-585 Report Generation Design

This document outlines the plan and prerequisite steps for calculating the required fields and generating a completed Form E-585 PDF.

## 1. Data Prerequisites

To accurately generate the E-585 form, the following data must be available in the system for a given reporting period (e.g., the last six months).

### From the `organizations` table:
*   `name`: The legal name of the non-profit organization.
*   `fein`: The Federal Employer ID Number.
*   `address`, `city`, `state`, `zip_code`: The organization's mailing address.
*   `ntee_code`: The National Taxonomy of Exempt Entities (NTEE) code.

### From the `users` table (for the treasurer):
*   `full_name`: The name of the treasurer or designated contact person.
*   `contact_telephone`: The contact telephone number for the treasurer.

### From the `receipts` and `receipt_tax_breakdowns` tables:
*   A collection of all `approved` receipts within the reporting period.
*   For each receipt, a clear breakdown of the tax amounts into `state`, `county`, `transit`, and `food` categories, stored in the `receipt_tax_breakdowns` table.

## 2. Calculation Logic for Form E-585 Fields

The following outlines the logic for calculating each key field on the form. This process will be executed by a backend service when the treasurer initiates a new report.

*   **Line 2: Total Qualifying Purchases**
    *   **State Column:** Sum the `subtotal_amount` for all `approved` receipts in the reporting period.
    *   **Food, County & Transit Column:** Sum the `subtotal_amount` for all `approved` receipts where the `receipt_tax_breakdowns` table contains an entry for `food`, `county`, or `transit` tax.

*   **Line 3: Amount of Sales and Use Tax Paid Directly**
    *   This is the sum of all tax amounts from the `receipt_tax_breakdowns` table for `approved` receipts.

*   **Line 4: Amount of Sales and Use Tax Paid Indirectly**
    *   This will be **0.00** for our initial implementation, as we are not handling certified statements from contractors at this time.

*   **Line 5: Amount of Use Tax Paid Directly to the Department**
    *   This will be **0.00** for our initial implementation.

*   **Line 6: Total Tax**
    *   Sum of Lines 3, 4, and 5.

*   **Line 7: Total Refund Requested**
    *   The value from Line 6.

*   **Line 8: Allocation of Food, County & Transit Tax**
    *   This section requires a detailed breakdown of the tax amounts by rate.
    *   **Food 2.00% Tax:** Sum of `amount` from `receipt_tax_breakdowns` where `tax_type` is `food`.
    *   **County 2.00% Tax:** Sum of `amount` from `receipt_tax_breakdowns` where `tax_type` is `county` and the tax rate is 2.00%.
    *   **County 2.25% Tax:** Sum of `amount` from `receipt_tax_breakdowns` where `tax_type` is `county` and the tax rate is 2.25%.
    *   **Transit 0.50% Tax:** Sum of `amount` from `receipt_tax_breakdowns` where `tax_type` is `transit`.

## 4. Supplementary Form Generation: E-536R

If an organization has paid taxes in more than one county during the reporting period, the system must also generate Form E-536R.

### Triggering Condition:
*   The system will query all `approved` receipts for the reporting period and identify the number of distinct counties from the `receipts.county` field. If the count is greater than one, the E-536R generation process is triggered.

### Calculation Logic for E-536R Fields:
*   The form will be populated by grouping all `receipt_tax_breakdowns` by county.
*   For each county, the system will sum the `amount` for each `tax_type` (`county` and `transit`) and populate the corresponding fields on the E-536R form.

### PDF Generation Process:
*   The E-536R will be generated as a separate but linked PDF alongside the main E-585 form.
*   The treasurer will be prompted to download both documents, as they must be submitted together.

### Field-by-Field Calculation Logic:

1.  **Name of Taxing County:**
    *   **Rule:** If all taxes were paid in only one county, enter the name of that county. If you made purchases and paid county & transit tax in more than one county, do not list a county on Line 1 and attach Form E-536R.
    *   **Logic:** If `COUNT(DISTINCT receipts.county)` for the reporting period is 1, this field will be pre-filled with the county name. Otherwise, it will be left blank.

2.  **Total Qualifying Purchases:**
    *   **Rule:** Do not include tax paid, purchases for resale, or items described in the nonrefundable items box.
    *   **Logic (State Column):** `SUM(receipts.subtotal_amount)` for all approved receipts in the reporting period.
    *   **Logic (Food, County & Transit Column):** `SUM(receipts.subtotal_amount)` for all approved receipts that have a corresponding entry in `receipt_tax_breakdowns` with `tax_type` of `food`, `county`, or `transit`.

3.  **Amount of Sales and Use Tax Paid Directly to Retailers:**
    *   **Rule:** Do not include tax paid on nonrefundable purchases as described in the box on the front of the claim form.
    *   **Logic:** `SUM(receipt_tax_breakdowns.amount)` for all approved receipts.

4.  **Amount of Sales and Use Tax Paid Indirectly on Qualifying Purchases:**
    *   **Rule:** Enter the total amount of sales and use tax paid indirectly on qualifying purchases of building materials, supplies, fixtures, and equipment as shown on certified statements from real property contractors or other persons.
    *   **Logic:** **0.00** (not supported in the initial implementation).

5.  **Amount of Use Tax Paid Directly to the Department on Qualifying Purchases:**
    *   **Rule:** Do not include tax collected and remitted on sales made by the entity.
    *   **Logic:** **0.00** (not supported in the initial implementation).

6.  **Total Tax:**
    *   **Rule:** Add Lines 3, 4, and 5. Food, County & Transit tax must be identified by rate on Line 8. For nonprofit entity only; annual cap applies.
    *   **Logic:** The sum of the calculated values for Lines 3, 4, and 5.

7.  **Total Refund Requested:**
    *   **Rule:** Add State and Food, County & Transit tax on Line 6.
    *   **Logic:** The calculated value from Line 6.

8.  **Allocation of Food, County & Transit Tax:**
    *   **Rule:** Enter the Food, County & Transit tax paid at each applicable rate. If you paid more than one county's tax, see the instructions on page 2 and attach Form E-536R.
    *   **Logic (Food 2.00% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `food`.
    *   **Logic (County 2.00% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `county` and the associated county's tax rate is 2.00%.
    *   **Logic (County 2.25% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `county` and the associated county's tax rate is 2.25%.
    *   **Logic (Transit 0.50% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `transit`.

1.  **Initiation:** The treasurer selects a reporting period and clicks a "Generate E-585 Report" button in the web dashboard.
2.  **Data Aggregation:** The backend service fetches all `approved` receipts and their corresponding `receipt_tax_breakdowns` for the selected period.
3.  **Calculation:** The service executes the calculation logic defined in Section 2 to compute the value for each field.
4.  **PDF Population:** The service uses a PDF library (e.g., `pdf-lib` for Node.js or `PyPDF2` for Python) to programmatically fill in the fields of a template E-585 PDF form. The system will only pre-fill the following fields:
    *   Organization Name
    *   Organization Address
    *   Period Beginning and Period Ending dates
5.  **Download:** The generated, partially-completed PDF is then made available for the treasurer to download. The treasurer must then manually fill in the remaining sensitive information (Account ID, Federal Employer ID, contact details, etc.) before signing and mailing the form.
