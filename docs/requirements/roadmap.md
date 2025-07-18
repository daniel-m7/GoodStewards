# Project Phases & Roadmap

## Phase 1: Feasibility & Validation (Pre-Product)

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
        *   **Task 1.3.1: Project Scaffolding**
            *   Define the monorepo structure (`backend`, `frontend`, `docs`).
        *   **Task 1.3.2: Local Development Environment**
            *   Set up Docker and `docker-compose.yml` for local development.
            *   Add a PostgreSQL service to Docker Compose.
            *   Add a Dockerfile for the backend service.
        *   **Task 1.3.3: Database and Data Layer**
            *   Define and implement the initial database schema in PostgreSQL.
            *   Set up the data access layer using `psycopg3`.
            *   Implement data models for users, organizations, receipts, etc.
        *   **Task 1.3.4: Core Backend Services**
            *   Set up the FastAPI backend application.
            *   Implement user/organization management with OAuth2 support.
            *   Integrate BAML for AI-powered receipt data extraction.
            *   Implement Cloudflare R2 for image storage.
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
