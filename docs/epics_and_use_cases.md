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

### Epic 3: Enhance User Engagement & Support

**As a user (member or treasurer), I need a simple way to provide feedback, report issues, or request new features so that my input can contribute to the improvement of the GoodStewards application.**

*   **Use Case 3.1: In-App Feedback Submission**
    *   The system shall provide a clear and accessible mechanism within both the mobile app and the web dashboard for users to submit feedback.
    *   Users shall be able to categorize their feedback (e.g., Testimony, Bug Report, Feature Request).
    *   Users shall be able to provide a free-text description of their feedback.
    *   The system shall automatically capture relevant user and device information (e.g., user ID, app version, OS) with bug reports.
    *   All feedback shall be persisted in a dedicated database table.
    *   An email notification shall be sent to a designated support inbox upon new feedback submission.