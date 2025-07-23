# GoodStewards Admin Dashboard UX

## 1. Document Purpose

This document provides a comprehensive plan for the user experience (UX) and user flows for the Admin Dashboard. This dashboard is the global control panel for managing the entire GoodStewards platform, used by the GoodStewards support and operations team.

## 2. Target Persona

### The Platform Administrator

*   **Who they are:** A member of the GoodStewards internal team responsible for platform health, customer support, and business oversight.
*   **Core Motivation:** To ensure the platform is running smoothly, new organizations are onboarded correctly, and any user-facing issues are resolved quickly.
*   **Key Pain Points:**
    *   Difficulty getting a high-level overview of platform usage and health.
    *   Time-consuming to manage individual organization or user issues.
    *   Lack of a centralized place to view and manage user feedback.
*   **Primary Goals:**
    *   A single dashboard to monitor key business and performance metrics.
    *   The ability to quickly find and manage any organization or user on the platform.
    *   An efficient workflow for handling support tickets and feedback.

## 3. UI/UX Principles

*   **Data-Dense & Clear:** Present a large amount of information in a clear, digestible format using charts, graphs, and tables.
*   **Comprehensive & Centralized:** A single source of truth for all platform data and management tasks.
*   **Efficient & Powerful:** Provide robust search, filtering, and sorting capabilities to allow admins to find information quickly.
*   **Secure:** Access is strictly limited to authorized admin users with appropriate permissions.

## 4. Screen-by-Screen Breakdown & Mockups

### Screen A: The Main Dashboard (Global Overview)

*   **Purpose:** To provide a high-level, real-time "mission control" view of the entire platform's health and activity.
*   **Key Elements:** A series of data widgets showing key metrics, a list of recently joined organizations, and a live feed of user feedback.

```ascii
+------------------------------------------------------------------------------------------------+
| Admin Dashboard                                                                 [Admin Avatar] |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|  +------------------------+  +------------------------+  +-------------------------+           |
|  | Total Orgs             |  | Total Users            |  | System-Wide Refund Est. |           |
|  |          42            |  |          1,337         |  |       $1,234,567.89     |           |
|  +------------------------+  +------------------------+  +-------------------------+           |
|                                                                                                |
|  +--------------------------------------------------+  +-------------------------------------+ |
|  | Receipts Processed (Last 30 Days)                |  | Latest Feedback                     | |
|  |                                                  |  | ----------------------------------- | |
|  |  [ Chart showing daily receipt volume ]          |  | [Bug] "Can't upload receipt" - J.Doe| |
|  |                                                  |  | [Feature] "Quickbooks sync" - A.Smith | 
|  |                                                  |  | [Praise] "This app is great!" - B.Lee | 
|  +--------------------------------------------------+  +-------------------------------------+ |
|                                                                                                |
|  +------------------------------------------------------------------------------------------+  |
|  | Recently Joined Organizations                                                            |  |
|  | ---------------------------------------------------------------------------------------- |  |
|  | [Logo] Hope Foundation       members: 50    plan: Pro      joined: 2025-07-22            |  |
|  | [Logo] Animal Shelter        members: 25    plan: Basic    joined: 2025-07-21            |  |
|  +------------------------------------------------------------------------------------------+  |
+------------------------------------------------------------------------------------------------+
```

### Screen B: Organization Management

*   **Purpose:** To allow admins to view, search, and manage all non-profit organizations on the platform.
*   **Key Elements:** A powerful, searchable table of all organizations. Clicking an organization takes the admin to a detailed view.

```ascii
+-------------------------------------------------------------------------------------------------+
| < Back      Organizations                                                                       |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|  Search Orgs: [ Hope Foundation...          ]  [+ Add New Org]                                  |
|                                                                                                 |
|  |----------------|------------------|-------------|-----------------|-----------|------------| |
|  | ORG NAME       | PRIMARY CONTACT  | MEMBERS     | PLAN            | STATUS    | JOINED     | |
|  |----------------|------------------|-------------|-----------------|-----------|------------| |
|  | Hope Foundation| treasurer@hope.org | 50          | Pro             | Active    | 2025-07-22 |
|  | Animal Shelter | finance@pets.org | 25          | Basic           | Active    | 2025-07-21 | |
|  | City Library   | books@city.gov   | 120         | Pro             | Trialing  | 2025-07-20 | |
|  | ...            | ...              | ...         | ...             | ...       | ...        | |
|  |----------------|------------------|-------------|-----------------|-----------|------------| |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

### Screen C: User Management

*   **Purpose:** To allow admins to find any user across any organization, view their details, and manage their roles or status.
*   **Key Elements:** A searchable table of all users, with filters for role, organization, and status.

```ascii
+--------------------------------------------------------------------------------------------------+
| < Back      Users                                                                                |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|  Search Users: [ john.doe@example.com...   ]  Filter by Role: [All v]  Org: [All v]              |
|                                                                                                  |
|  |--------------------|----------------------|-----------------|----------|-------------------|  |
|  | USER               | ORGANIZATION         | ROLE            | STATUS   | LAST SEEN         |  |
|  |--------------------|----------------------|-----------------|----------|-------------------|  |
|  | john.doe@example.com| Hope Foundation      | Member          | Active   | 2025-07-23 10:05 AM | 
|  | treasurer@hope.org | Hope Foundation      | Treasurer       | Active   | 2025-07-23 09:15 AM| |
|  | finance@pets.org   | Animal Shelter       | Treasurer       | Active   | 2025-07-22 04:30 PM| |
|  | user@city.gov      | City Library         | Member          | Pending  | 2025-07-21 11:00 AM| |
|  | ...                | ...                  | ...             | ...      | ...                | |
|  |--------------------|----------------------|-----------------|----------|--------------------| |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

### Screen D: Feedback Management Inbox

*   **Purpose:** To provide a centralized place to review, categorize, assign, and respond to all user-submitted feedback.
*   **Key Elements:** An inbox-style layout with filters for feedback type (Bug, Feature, Praise) and status (New, In Progress, Resolved).

```ascii
+------------------------------------------------------------------------------------------------+
| < Back      Feedback Inbox                                                                     |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|  Filter by Type: [All v]   Status: [New v]   Search: [ quickbooks... ]                         |
|                                                                                                |
|  +------------------------------------------------------------------------------------------+  |
|  | [BUG] Can't upload receipt from Android                                                  |  |
|  | From: john.doe@example.com (Hope Foundation) | Status: New | Assigned: Unassigned        |  |
|  | > I'm trying to upload a PNG file from my gallery and the app just spins...              |  |
|  |------------------------------------------------------------------------------------------|  |
|  | [FEATURE] QuickBooks Integration                                                         |  |
|  | From: finance@pets.org (Animal Shelter) | Status: In Progress | Assigned: Dev Team       |  |
|  | > We would love to be able to sync our approved expenses directly to QuickBooks...       |  |
|  |------------------------------------------------------------------------------------------|  |
|  | [PRAISE] This app is great!                                                              |  |
|  | From: user@city.gov (City Library) | Status: Resolved | Assigned: N/A                    |  |
|  | > Just wanted to say thank you for building this, it saves me so much time!              |  |
|  +------------------------------------------------------------------------------------------+  |
+------------------------------------------------------------------------------------------------+
```