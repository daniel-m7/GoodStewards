# Mobile App Development Plan: [Your App Name] - Member App

## 1. Project Summary

This document outlines the development plan for the member-facing mobile web application. The primary goal of this app is to provide a frictionless, "capture and go" experience for non-profit organization members to submit expense and donation receipts. By simplifying this process, we enable the parent organization to accurately collect the necessary data to claim semi-annual sales tax refunds, recovering funds that are often lost due to administrative complexity.

## 2. Target Persona: The Non-Profit Member

*   **Who they are:** A member of a non-profit who occasionally incurs expenses or makes small donations on behalf of the organization.
*   **Pain Points:**
    *   Saving and remembering to hand in physical receipts is a hassle.
    *   The reimbursement process is slow and requires meeting the treasurer in person.
    *   They often don't bother submitting small receipts, leading to lost data for the organization.
*   **Goals:**
    *   A fast, simple way to submit a receipt the moment they get it.
    *   To be reimbursed quickly and electronically.
    *   To help their organization without adding to their own administrative burden.

## 3. End-to-End User Journey

The user journey is split into two distinct phases: a one-time onboarding process and the recurring core usage loop.

### Phase 1: Onboarding & Registration (First-Time Use)

This phase begins outside the app, with an email invitation. The user cannot self-register; they must be invited by their organization's treasurer.

1.  **Receive Invitation:** The user receives a clear, trustworthy email from `[Your App Name]` on behalf of their organization's administrator.
2.  **Accept Invitation:** The user clicks a unique "Accept Invitation" link in the email.
3.  **Open Mobile App:** The link opens the mobile web app to a dedicated, pre-filled registration screen.
4.  **Create Account:** The user sets their full name and a password to create their account. Their email address is locked and tied to the invitation.
5.  **First Login:** Upon successful registration, the user is automatically logged in and lands on the main Dashboard screen.

### Phase 2: Core Usage (Submitting Receipts)

This is the primary workflow for an authenticated, registered user.

1.  **Open App:** The user opens the mobile web app and logs in if their session has expired.
2.  **Initiate Upload:** From the Dashboard, the user taps the primary "Add Receipts" button.
3.  **Capture/Select:** The user chooses to either take new photos with their camera or select one or more existing receipt images from their photo library.
4.  **Review Selections:** The user is shown thumbnails of all selected receipts, with the ability to remove any accidental selections.
5.  **Confirm Upload:** The user taps a single "Upload" button. The app begins uploading the images in the background.
6.  **Receive Feedback:** The app provides immediate visual feedback that the uploads are processing. The user can safely navigate away or close the app.
7.  **View Submission:** The new submissions appear at the top of their Dashboard list with a "Pending" status, confirming the action was successful.

## 4. Screen-by-Screen Breakdown & Mockups

### Screen A: Login Screen
*   **Purpose:** To authenticate an existing user. This is the fallback screen if a user opens the app without a valid session.
*   **Key Elements:** Email input, Password input, Login button.
*   **Helper Text:** "You must be invited by your organization to create an account."

```ascii
+--------------------------------------+
|                                      |
|            Welcome Back              |
|                                      |
|  Email Address                       |
|  [                             ]     |
|                                      |
|  Password                            |
|  [ •••••••••••                   ]     |
|                                      |
|  [              Login              ] |
|                                      |
|  ----------------------------------  |
|  You must be invited by your         |
|  organization to create an account.  |
+--------------------------------------+