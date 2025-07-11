# GoodStewards Project Overview

This document provides a comprehensive overview of the GoodStewards project, encompassing its vision, goals, key principles, defined roles, epics, use cases, and strategic roadmap. It also includes detailed design considerations for core functionalities like E-585 report generation.

## 1. Project Vision & Goal

**Vision:** To empower non-profit organizations in North Carolina to maximize their financial resources by automating the complex and labor-intensive process of claiming sales and use tax refunds.

**Goal:** Develop and launch a unified web and mobile application that streamlines receipt submission, automates data extraction, facilitates electronic reimbursement workflows, and generates accurate, compliant tax refund forms (E-585 and E-536R).

## 2. Key Principles

*   **Open Source First:** Prioritize well-supported open-source libraries and frameworks to avoid vendor lock-in and manage costs.
*   **Cost-Effective Scalability:** Choose hosting and service providers with generous free tiers and predictable scaling paths.
*   **Lean & Modern Stack:** Employ technologies that enable rapid development and high effectiveness.
*   **User-Centric Design:** Focus on intuitive and simple user experiences for both members and treasurers.
*   **Security & Compliance:** Implement robust data security measures and adhere strictly to tax regulations.
*   **Continuous Improvement:** Embrace iterative development and incorporate user feedback for ongoing enhancements.

## 3. Defined Roles

*   **Product Owner (PO):** Defines vision, prioritizes features, manages roadmap.
*   **Technical Lead (TL):** Oversees technical architecture, ensures code quality, guides development.
*   **AI/ML Engineer (AI/ML):** Focuses on OCR, data extraction, and AI model training.
*   **Backend Developer (BE):** Implements API, database interactions, business logic.
*   **Frontend Developer (FE):** Develops user interfaces for web and mobile.
*   **QA Engineer (QA):** Designs and executes test plans, ensures quality and stability.
*   **DevOps Engineer (DO):** Manages infrastructure, CI/CD, deployment.
*   **Gemini-CLI Agent (AI-Agent):** Assists with code generation, documentation, and task automation.

## 4. Epics and Use Cases

### Epic 1: Automate Tax Refund Claims

**As the treasurer of a nonprofit organization, I need an effective and efficient mechanism to automate the process of capturing and claiming refunds on state, county, and transit sales and use taxes.**

*   **Use Case 1.1: AI-Powered Data Extraction**
    *   The system shall allow the treasurer to view all member-submitted receipts in a central dashboard.
    *   The system shall use an AI model to automatically extract key information from receipts: vendor name, date, subtotal, and distinct tax amounts (state, county, transit).
    *   The system shall provide a clean interface for the treasurer to quickly review and, if necessary, correct any extracted data.

*   **Use Case 1.2: Automated Form Generation**
    *   The system shall automatically aggregate financial data from all approved receipts for a given refund period.
    *   The system shall generate a completed, pixel-perfect PDF of Form E-585 (and any other required schedules like Form E-536R) with the aggregated data, ready for the treasurer to sign and submit.

*   **Use Case 1.3: Automated Reporting**
    *   The system shall provide automated end-of-year expense reports with expenses auto-categorized, simplifying budget review and financial reporting.

### Epic 2: Streamline Expense and Donation Submission

**As a nonprofit organization member, I need an efficient and effective mechanism to submit my expense and or donation receipts so that sales taxes are accurately captured.**

*   **Use Case 2.1: Mobile-First Receipt Submission**
    *   The member can use their smartphone to take a picture of a physical receipt and upload it in seconds.
    *   The member can upload a digital receipt (e.g., PDF, email screenshot).
    *   The member does not need to manually calculate the total amount of their receipts.

*   **Use Case 2.2: Voice-to-Text Summary (Future Feature)**
    *   The member can use their voice to provide a brief summary or description of the expenses being submitted, which the system transcribes and attaches as a note.

*   **Use Case 2.3: Automated Reimbursement Workflow**
    *   Once a member submits an expense, the treasurer receives a mobile notification to approve the submission.
    *   Upon approval, the treasurer can initiate payment via Zelle or issue a check in person.
    *   The treasurer can upload an online banking payments export (CSV) with dates and paid amounts.
    *   The system will attempt to automatically match submitted receipts with corresponding Zelle transaction IDs or check numbers from the CSV.
    *   For any receipts that cannot be automatically matched, the treasurer can manually link them.
    *   The system will store the payment confirmation alongside the receipt for audit purposes.
    *   The member receives status update notifications (e.g., "Submitted," "Approved," "Paid") at each stage of the process.

*   **Use Case 2.4: Receipt as Donation**
    *   The member can submit a receipt as a donation, not for reimbursement.
    *   Sales tax is still captured for the organization's tax refund claim.
    *   When the submission is approved, no payment is initiated to the member.

*   **Use Case 2.5: Flexible User and Donation Handling**
    *   Each organization shall have a default "Anonymous Donor" user for donations where the donor wishes to remain anonymous.
    *   Each organization shall have a default "Unknown User" to allow treasurers to submit old receipts where the original member is not known.
    *   The treasurer shall be able to create a new, simple user profile for a non-member donor by simply entering their name, allowing for proper record-keeping of one-time donations.

*   **Use Case 2.6: Treasurer Submits on Behalf of Member**
    *   The treasurer can submit receipts for an existing member of the organization.
    *   The system shall allow the treasurer to search for and select an existing member during the receipt submission process.
    *   The submitted receipt will be associated with the selected member's account for tracking and reimbursement purposes.

### Epic 3: Enhance User Engagement & Support

**As a user (member or treasurer), I need a simple way to provide feedback, report issues, or request new features so that my input can contribute to the improvement of the GoodStewards application.**

*   **Use Case 3.1: In-App Feedback Submission**
    *   The system shall provide a clear and accessible mechanism within both the mobile app and the web dashboard for users to submit feedback.
    *   Users shall be able to categorize their feedback (e.g., Testimony, Bug Report, Feature Request).
    *   Users shall be able to provide a free-text description of their feedback.
    *   The system shall automatically capture relevant user and device information (e.g., user ID, app version, OS) with bug reports.
    *   All feedback shall be persisted in a dedicated database table.
    *   An email notification shall be sent to a designated support inbox upon new feedback submission.

## 5. Project Phases & Roadmap

### Phase 0: Feasibility & Validation (Pre-Product)

*   **Status:** Completed
*   **Goal:** Validate market need, refine business model, and establish initial customer relationships.

    *   **Sprint 0.1: Deep Customer Discovery**
        *   **Task 0.1.1:** Interview 20-30 non-profit treasurers to validate pain points and gather feedback.
        *   **Assigned Roles:** PO

    *   **Sprint 0.2: Concierge MVP & Business Model Refinement**
        *   **Task 0.2.1:** Manually process receipts and fill forms for early customers.
        *   **Task 0.2.2:** Refine pricing strategy and go-to-market plan based on feedback.
        *   **Assigned Roles:** PO, TL

### Phase 1: Product Development (MVP)

*   **Status:** In Progress
*   **Goal:** Develop and launch the core application with essential features for initial user adoption.

    *   **Sprint 1.1: Requirements Gathering & Analysis**
        *   **Status:** Completed
        *   **Task 1.1.1:** Define core functionalities.
        *   **Task 1.1.2:** Define user stories.
        *   **Task 1.1.3:** Define technical specifications.
        *   **Task 1.1.4:** Define mobile UX.
        *   **Task 1.1.5:** Define expense/donation workflow.
        *   **Task 1.1.6:** Define non-refundable categories.
        *   **Task 1.1.7:** Define initial technical architecture.
        *   **Task 1.1.8:** Define E-585/E-536R form requirements.
        *   **Assigned Roles:** PO, TL, AI-Agent

    *   **Sprint 1.2: Design & Prototyping**
        *   **Task 1.2.1:** Finalize database schema.
        *   **Task 1.2.2:** Design core API endpoints.
        *   **Task 1.2.3:** Design authentication/authorization flows (including OAuth2 for "Sign in with Apple/Google").
        *   **Task 1.2.4:** Create high-fidelity UI/UX mockups for mobile and web dashboards.
        *   **Task 1.2.5:** Design PDF generation interface.
        *   **Assigned Roles:** TL, BE, FE, AI/ML, QA

    *   **Sprint 1.3: Core Backend, Data Layer & AI Integration**
        *   **Task 1.3.1:** Define and implement database schema (PostgreSQL).
        *   **Task 1.3.2:** Set up ORM (e.g., SQLAlchemy with Alembic for migrations).
        *   **Task 1.3.3:** Implement data models for users, organizations, receipts, and extracted data.
        *   **Task 1.3.4:** Set up FastAPI backend.
        *   **Task 1.3.5:** Implement user/organization management (including OAuth2 for "Sign in with Apple/Google").
        *   **Task 1.3.6:** Integrate BAML for AI-powered receipt data extraction.
        *   **Task 1.3.7:** Implement Cloudflare R2 for image storage.
        *   **Assigned Roles:** BE, AI/ML, TL, AI-Agent (for code generation)

    *   **Sprint 1.4: Mobile App Development**
        *   **Task 1.4.1:** Develop Svelte/Capacitor mobile app for receipt submission.
        *   **Task 1.4.2:** Implement camera/photo library integration and submission review/confirmation screens.
        *   **Task 1.4.3:** Add functionality for treasurers to submit receipts on behalf of members, including a CSV member import and search-as-you-type selection.
        *   **Assigned Roles:** FE, BE, QA, AI-Agent (for UI components, data binding)

    *   **Sprint 1.5: Web Dashboard & Reimbursement Workflow**
        *   **Task 1.5.1:** Develop SvelteKit web dashboard for treasurers.
        *   **Task 1.5.2:** Implement receipt approval/rejection.
        *   **Task 1.5.3:** Implement payment reconciliation (CSV upload, matching).
        *   **Assigned Roles:** FE, BE, QA, AI-Agent (for dashboard components, workflow logic)

    *   **Sprint 1.6: PDF Generation Implementation**
        *   **Task 1.6.1:** Implement E-585 PDF generation logic.
        *   **Task 1.6.2:** Implement E-536R PDF generation logic.
        *   **Task 1.6.3:** Integrate PDF generation library.
        *   **Assigned Roles:** BE, QA, AI-Agent (for form-filling logic, scripts)

    *   **Sprint 1.7: Testing & Quality Assurance (MVP)**
        *   **Task 1.7.1:** Write/execute unit/integration tests.
        *   **Task 1.7.2:** Conduct initial UAT with early adopters.
        *   **Task 1.7.3:** Perform basic security/performance testing.
        *   **Assigned Roles:** QA, BE, FE, TL

    *   **Sprint 1.8: Initial Deployment (MVP)**
        *   **Task 1.8.1:** Set up initial production hosting (Vercel, Render).
        *   **Task 1.8.2:** Configure basic CI/CD pipelines.
        *   **Task 1.8.3:** Deploy web dashboard and backend services.
        *   **Assigned Roles:** DO, TL

    *   **Sprint 1.9: Website Development**
        *   **Task 1.9.1:** Purchase and register the goodstewards.app domain.
        *   **Task 1.9.2:** Develop a public-facing website to attract and inform potential users, primarily non-profit treasurers.
        *   **Task 1.9.3:** Feature short videos, infographics, and testimonials to illustrate ROI.
        *   **Assigned Roles:** FE, PO, TL

    *   **Sprint 1.10: App Store Deployment**
        *   **Task 1.10.1:** Register for Apple Developer and Google Play Developer accounts.
        *   **Task 1.10.2:** Configure app store listings.
        *   **Task 1.10.3:** Prepare marketing materials (screenshots, descriptions).
        *   **Task 1.10.4:** Submit the mobile app for review and approval.
        *   **Assigned Roles:** PO, TL, FE

### Phase 2: Growth & Expansion (Post-MVP)

*   **Status:** To Do
*   **Goal:** Scale customer acquisition, expand feature set, and explore new markets.

    *   **Sprint 2.1: Post-Launch Monitoring & Support**
        *   **Task 2.1.1:** Monitor application performance/error logs.
        *   **Task 2.1.2:** Provide user support.
        *   **Task 2.1.3:** Address immediate issues.
        *   **Assigned Roles:** DO, QA, PO

    *   **Sprint 2.2: Customer Acquisition & Adoption**
        *   **Task 2.2.1:** Ramp up marketing/sales efforts.
        *   **Task 2.2.2:** Implement freemium model (if applicable).
        *   **Task 2.2.3:** Develop customer success strategies.
        *   **Assigned Roles:** PO

    *   **Sprint 2.3: Feature Enhancements & Optimizations**
        *   **Task 2.3.1:** Implement voice-to-text summary.
        *   **Task 2.3.2:** Integrate with accounting software (QuickBooks, Xero).
        *   **Task 2.3.3:** Develop advanced reporting.
        *   **Task 2.3.4:** Optimize existing features.
        *   **Assigned Roles:** PO, TL, BE, FE, AI/ML, QA, AI-Agent

    *   **Sprint 2.4: Geographic Expansion**
        *   **Task 2.4.1:** Investigate sales tax refund programs in other states.
        *   **Task 2.4.2:** Adapt product for new regulatory environments.
        *   **Assigned Roles:** PO, TL

## 6. E-585 Report Generation Design

This section outlines the plan and prerequisite steps for calculating the required fields and generating a completed Form E-585 PDF.

### 6.1. Data Prerequisites

To accurately generate the E-585 form, the following data must be available in the system for a given reporting period (e.g., the last six months).

*   **From the `organizations` table:**
    *   `name`: The legal name of the non-profit organization.
    *   `fein`: The Federal Employer ID Number.
    *   `address`, `city`, `state`, `zip_code`: The organization's mailing address.
    *   `ntee_code`: The National Taxonomy of Exempt Entities (NTEE) code.

*   **From the `users` table (for the treasurer):**
    *   `full_name`: The name of the treasurer or designated contact person.
    *   `contact_telephone`: The contact telephone number for the treasurer.

*   **From the `receipts` and `receipt_tax_breakdowns` tables:**
    *   A collection of all `approved` receipts within the reporting period.
    *   For each receipt, a clear breakdown of the tax amounts into `state`, `county`, `transit`, and `food` categories, stored in the `receipt_tax_breakdowns` table.

### 6.2. Calculation Logic for Form E-585 Fields

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

### 6.3. Supplementary Form Generation: E-536R

If an organization has paid taxes in more than one county during the reporting period, the system must also generate Form E-536R.

### 6.3.1. Triggering Condition:
*   The system will query all `approved` receipts for the reporting period and identify the number of distinct counties from the `receipts.county` field. If the count is greater than one, the E-536R generation process is triggered.

### 6.3.2. Calculation Logic for E-536R Fields:
*   The form will be populated by grouping all `receipt_tax_breakdowns` by county.
*   For each county, the system will sum the `amount` for each `tax_type` (`county` and `transit`) and populate the corresponding fields on the E-536R form.

### 6.3.3. PDF Generation Process:
*   The E-536R will be generated as a separate but linked PDF alongside the main E-585 form.
*   The treasurer will be prompted to download both documents, as they must be submitted together.

### 6.4. Field-by-Field Calculation Logic (E-585 Details):

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
    *   **Logic (County 2.00% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `county` and the tax rate is 2.00%.
    *   **Logic (County 2.25% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `county` and the tax rate is 2.25%.
    *   **Logic (Transit 0.50% Tax):** `SUM(receipt_tax_breakdowns.amount)` where `tax_type` = `transit`.

### 6.5. PDF Generation Process (High-Level):

1.  **Initiation:** The treasurer selects a reporting period and clicks a "Generate E-585 Report" button in the web dashboard.
2.  **Data Aggregation:** The backend service fetches all `approved` receipts and their corresponding `receipt_tax_breakdowns` for the selected period.
3.  **Calculation:** The service executes the calculation logic defined in Section 6.2 to compute the value for each field.
4.  **PDF Population:** The service uses a PDF library (e.g., `pdf-lib` for Node.js or `PyPDF2` for Python) to programmatically fill in the fields of a template E-585 PDF form. The system will only pre-fill the following fields:
    *   Organization Name
    *   Organization Address
    *   Period Beginning and Period Ending dates
5.  **Download:** The generated, partially-completed PDF is then made available for the treasurer to download. The treasurer must then manually fill in the remaining sensitive information (Account ID, Federal Employer ID, contact details, etc.) before signing and mailing the form.

## 7. Cross-Cutting Concerns

*   **Metrics Capture & Analysis:**
    *   **Task C.1.1:** Define key performance indicators (KPIs) for user engagement, refund amounts, processing efficiency, and financial performance.
    *   **Task C.1.2:** Implement analytics tools to track and report on these metrics continuously.
    *   **Assigned Roles:** PO, TL, BE
*   **Security & Compliance:**
    *   **Task C.2.1:** Ongoing review and implementation of security best practices (data encryption, access control).
    *   **Task C.2.2:** Adherence to evolving tax laws and data privacy regulations.
    *   **Assigned Roles:** TL, BE, QA
*   **Beta Testing Program:**
    *   **Task C.3.1:** Establish a formal beta testing program for new features and major releases to gather early feedback and ensure quality.
    *   **Assigned Roles:** PO, QA

## 8. Tax Law Principles

General tax law principles and NCDOR practices suggest that refund claims may be subject to a statute of limitations, typically three years from the date the tax was paid or the due date of the return, whichever is later, as outlined in N.C. Gen. Stat. § 105-241.6. This could imply that nonprofits might be able to file refund claims for up to three years prior, covering six semiannual periods, provided the claims are within the statutory period and accompanied by proper documentation. 