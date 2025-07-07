# GoodStewards Mobile App UX and Workflow Plan

## 1. Document Purpose

This document provides a comprehensive plan for the user experience (UX), user flows, and core technical workflow for the member-facing mobile web application. Its purpose is to guide design and development, ensuring a consistent and intuitive experience for the end-user.

## 2. Target Persona: The Non-Profit Member

*   **Who they are:** A member of a non-profit organization who occasionally incurs expenses or makes small donations on its behalf.
*   **Core Motivation:** To contribute to their organization's mission with minimal personal friction.
*   **Key Pain Points:**
    *   Saving physical receipts is inconvenient.
    *   The process of getting reimbursed is slow and requires manual effort (e.g., in-person meetings).
    *   They often don't bother submitting small receipts, which results in lost data and unclaimed tax refunds for their organization.
*   **Primary Goals:**
    *   A fast, simple "fire-and-forget" way to submit a receipt the moment they get it.
    *   To be reimbursed quickly and electronically.

## 3. End-to-End User Journey

The user journey is split into two distinct phases: a one-time onboarding process and the recurring core usage loop.

### Phase 1: Onboarding & Registration (First-Time Use)

This phase allows a prospective member to join an organization. The primary, recommended method is via a secure, single-tap social sign-on (OAuth2), with a traditional email/password option available as a secondary choice.

1.  **Scan QR Code:** The user scans a unique QR code provided by the organization.
2.  **App Store Download:** The QR code directs the user to the appropriate app store to download the GoodStewards mobile app.
3.  **Install & Open App:** The user installs and opens the app, which is pre-configured with the organization's name from the QR code.
4.  **Choose Authentication Method:** The user is presented with a clear choice:
    *   **Primary (Recommended):** "Continue with Google" or "Continue with Apple."
    *   **Secondary:** A smaller option to sign up using their email and a password.
5.  **Create Account:**
    *   **OAuth Flow:** The user authenticates with their chosen provider (Google/Apple). The app receives their name and email, creating the account automatically.
    *   **Password Flow:** The user manually enters their full name, email, and creates a password.
6.  **First Login & Approval:** Upon successful registration, the user is logged in. Their membership status may be `pending` until approved by an organization administrator. They land on the main Dashboard.

### Phase 2: Core Usage Loop (Submitting Receipts)

This is the primary workflow for an authenticated, registered user. The design philosophy is **"Capture and Go."**

1.  **Open App:** The user opens the mobile web app. If their session is active, they land on the Dashboard. If not, they are presented with the Login screen.
2.  **Initiate Submission:** From the Dashboard, the user taps the primary "Add Receipts" button.
3.  **Capture or Select:** The user is given two clear choices: take new photos with their device camera or select one or more existing receipt images from their photo library.
4.  **Review Selections:** The user is shown thumbnails of all selected receipts, with details like total and sales tax for each. This allows them to spot and remove any accidental selections.
5.  **Choose Submission Type:** Before submitting, the user will be presented with a clear choice: "Reimburse" or "Donate".
6.  **Confirm Submission:** After selecting the submission type, the user reviews a summary of the total expenses and sales tax for all receipts to be redeemed. They then tap a single "Submit" button to confirm. The app immediately begins submitting the images in the background.
7.  **Receive Feedback:** The app provides immediate visual feedback that the submissions are processing. The user can safely navigate away or close the app; the process will continue.
8.  **View Submission:** The new submissions appear at the top of their Dashboard list with a "Pending" status, confirming the action was successful and closing the loop.

## 4. Screen-by-Screen Breakdown & Mockups

### Screen A: Login / Registration Screen
*   **Purpose:** To provide a single, clear entry point for both new and returning users, prioritizing modern, secure authentication.
*   **Key Elements:** Prominent "Continue with Google" and "Continue with Apple" buttons. A secondary, less emphasized option allows users to sign in or create an account with an email and password.
*   **Dynamic Behavior:** If the user chooses the email/password route, the screen could dynamically show a password field for existing users or name/password fields for new users after they type their email.

```ascii
+--------------------------------------+
|      Join [Organization Name]        |
|         or sign in                   |
+--------------------------------------+
|                                      |
|  [    G  Continue with Google      ] |
|                                      |
|  [      Continue with Apple      ] |
|                                      |
|  ---------------- or ---------------  |
|                                      |
|  Email Address                       |
|  [                             ]     |
|                                      |
|  [           Continue            ]   |
|                                      |
|  ----------------------------------  |
|  New user? Scan your organization's  |
|  QR code to get started.             |
+--------------------------------------+
```

### Screen C: The Dashboard (Home Screen)
*   **Purpose:** To provide the user with a clear history of their submissions and an obvious entry point for adding new receipts.
*   **Key Elements:** A vertically scrolling list of recent submissions with their status (Pending, Approved, Paid, Rejected), total, and sales tax, and a Floating Action Button (FAB) to add new ones.

```ascii
+-------------------------------------------------+
| Your Submissions                       [Avatar] |
+-------------------------------------------------+
|                                                 |
|  [Img]  Staples                       [Pending] |
|         Total: $45.21  Tax: $3.21               |
|  ---------------------------------------------  |
|  [Img]  Home Depot                     [Paid]   |
|         Total: $112.89 Tax: $8.89               |
|  ---------------------------------------------  |
|  [Img]  Processing...                 [Pending] |
|         Total: $---.-- Tax: $--.--              |
|                                                 |
|                                           [ + ] |
+-------------------------------------------------+
```

### Screen D: Review & Submit Screen
*   **Purpose:** To act as a final confirmation step, allowing the user to review their selected images, the extracted totals, and mark the submission as a donation before committing.
*   **Key Elements:** A grid of image thumbnails with totals, a summary of the combined total and sales tax, a checkbox to mark as a donation, a remove icon (X) on each, an "Add More" button, and a primary "Submit" button that dynamically counts the selections.

```ascii
+-------------------------------------------------+
| < Back      Review and Submit                   |
+-------------------------------------------------+
|                                                 |
|  +-----------+ X   +-----------+ X              |
|  | Receipt 1 |      | Receipt 2 |               |
|  | Total: $25 |     | Total: $50 |              |
|  | Tax: $2    |     | Tax: $4    |              |
|  +-----------+     +-----------+                |
|                                                 |
|  +-----------+ X                                |
|  | Receipt 3 |                                  |
|  | Total: $10 |                                 |
|  | Tax: $1    |                                 |
|  +-----------+                                  |
|                                                 |
|  ---------------------------------------------  |
|  Total: $85.00                                  |
|  Sales Tax: $7.00                               |
|                                                 |
|  [ ] Mark as donation (no reimbursement)        |
|  ---------------------------------------------  |
+-------------------------------------------------+
|  [      + Add More       ]                      |
|  [    Submit 3 Receipts    ]                    |
+-------------------------------------------------+
```

### Screen E: Submitting State Screen
*   **Purpose:** To provide clear, immediate feedback that the system has received the user's action and is processing it. This builds user trust.
*   **Key Elements:** The same layout as the Review screen, but with progress indicators (e.g., spinners) on each thumbnail and disabled action buttons to prevent duplicate submissions. A helper text reassures the user they can navigate away.

```ascii
+-------------------------------------------------+
|             Submitting...                       |
+-------------------------------------------------+
|                                                 |
|  +-----------+     +-----------+                |
|  | [Spinner] |     |     ✓     | (once done)    |
|  +-----------+     +-----------+                |
|                                                 |
|  Feel free to close this screen. We'll notify   |
|  you when your receipts are processed.          |
+-------------------------------------------------+
|  [      + Add More       ] (disabled)           |
|  [    Submitting...       ] (disabled)          |
+-------------------------------------------------+
```

## 5. Core Technical Workflow: Receipt Submission

This describes the step-by-step process that occurs when a user hits the "Submit" button.

1.  **User Action:** User taps the "Submit [N] Receipts" button.
2.  **Frontend:** The mobile web app initiates parallel HTTPS POST requests for each selected image file to a secure backend API endpoint (e.g., `/api/receipts`). The request header includes the user's JWT authentication token.
3.  **Backend - Initial Ingestion & Validation:**
    *   The API server receives the image files.
    *   It validates the authentication token to identify the user and their associated organization.
    *   For each image, it immediately creates a new record in the receipts table in PostgreSQL with a status of `processing`, linking it to `user_id` and `organization_id`.
    *   It securely streams the image file to the designated bucket in Cloudflare R2 object storage. The unique storage path (e.g., `org_id/user_id/receipt_uuid.jpg`) is saved to the new database record.
4.  **Backend - Asynchronous AI Processing:**
    *   The backend adds a job to a background queue (e.g., Celery, RQ) for each new receipt ID. This ensures the API can respond quickly to the user without waiting for AI processing.
    *   A worker process picks up the job, retrieves the image URL from the database record.
    *   The worker calls the BAML runtime, which executes a pre-defined function to call Google's Gemini Pro API, sending the image for analysis.
5.  **Backend - Data Persistence:**
    *   The Gemini API returns a structured JSON object containing the extracted vendor, date, total_amount, sales_tax, etc.
    *   The worker process receives this JSON.
    *   It updates the corresponding record in the PostgreSQL receipts table with the extracted data and changes the status from `processing` to `pending` (awaiting treasurer approval).
6.  **Frontend - UI Update:** The member's dashboard, upon being loaded or refreshed, will fetch the latest status for their submissions. For a more advanced experience, a WebSocket connection could push the status update (`processing` → `pending`) to the client in real-time.