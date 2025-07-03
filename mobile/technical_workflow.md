Technical Workflow: Receipt Submission
User Action: User taps the "Upload [N] Receipts" button.
Frontend: The mobile web app initiates parallel uploads for each selected image file to a secure backend API endpoint. The request includes the user's authentication token.
Backend - Initial Ingestion:
    The API server receives the image files.
    For each image, it immediately creates a new record in the receipts table in PostgreSQL with a status of processing, linking it to the authenticated user and their organization.
    It securely streams the image file to the designated bucket in Cloudflare R2 object storage. The storage path (e.g., org_id/user_id/receipt_uuid.jpg) is saved to the database record.
Backend - AI Processing (Asynchronous):
    The backend triggers an asynchronous job for each new receipt.
    This job calls the BAML runtime, passing it the image URL from Cloudflare R2.
    BAML executes a function call to Google's Gemini Pro API, sending the image for analysis.
Backend - Data Persistence:
    Gemini returns a structured JSON object containing the extracted vendor, date, total_amount, sales_tax, etc.
    The asynchronous job receives this JSON.
    It updates the corresponding record in the PostgreSQL receipts table with the extracted data and changes the status from processing to pending.
Frontend - UI Update: The member's dashboard periodically refreshes (or updates via a WebSocket connection) to show the new status and extracted data for the submitted receipts.