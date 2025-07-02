# Target Audience

Our solution is designed for two primary user personas within small to medium-sized non-profit organizations in North Carolina (typically with 50-500 members).

### Primary Target Audience: The Volunteer/Part-Time Treasurer

*   **Role:** Responsible for the organization's finances, including bookkeeping, budgeting, and reimbursements.
*   **Pain Points:**
    *   Overwhelmed by the manual, paper-based process of collecting and tracking receipts.
    *   Finds the process of filling out Form E-585 and associated schedules complex and time-consuming.
    *   Lacks a centralized system for a clear audit trail of expenses and reimbursements.
    *   Spends personal time on administrative tasks like writing and delivering physical checks.
*   **Goals:**
    *   To efficiently and accurately manage the organization's finances.
    *   To maximize the funds available to the non-profit's mission.
    *   To reduce the time spent on administrative tasks and focus on more strategic financial oversight.
    *   To have a clear, reportable view of the organization's spending.

### Secondary Target Audience: The Organization Member

*   **Role:** A member who incurs expenses or makes donations on behalf of the organization.
*   **Pain Points:**
    *   The hassle of saving and physically handing in receipts to the treasurer.
    *   Forgetting or choosing not to submit receipts for small donations, resulting in lost tax data for the organization.
    *   The reimbursement process is slow and requires meeting the treasurer in person.
*   **Goals:**
    *   To have a quick and easy way to submit expenses from their phone.
    *   To be reimbursed promptly and electronically without manual follow-up.
    *   To contribute to the organization's financial health with minimal personal effort.
```</details>

---

### **3. `docs/epics_and_use_cases.md`**

**Click to view/copy content:**

<details>
<summary><code>docs/epics_and_use_cases.md</code></summary>

```markdown
# Epics and Use Cases

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
    *   Once a member submits an expense, the treasurer is notified for approval via the web dashboard.
    *   Upon approval, the payment is processed electronically to the member's pre-configured bank account.
    *   The member receives status update notifications (e.g., "Submitted," "Approved," "Paid") at each stage of the process.