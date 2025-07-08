# Project Roadmap: GoodStewards.app

This document outlines the strategic roadmap for the GoodStewards.app project, encompassing business, technical, and operational phases. It is structured to facilitate understanding and integration with project management tools.

## Project Vision & Goal

**Vision:** To empower non-profit organizations in North Carolina to maximize their financial resources by automating the complex and labor-intensive process of claiming sales and use tax refunds.

**Goal:** Develop and launch a unified web and mobile application that streamlines receipt submission, automates data extraction, facilitates electronic reimbursement workflows, and generates accurate, compliant tax refund forms (E-585 and E-536R).

## Key Principles

*   **Open Source First:** Prioritize well-supported open-source libraries and frameworks.
*   **Cost-Effective Scalability:** Choose hosting and service providers with generous free tiers and predictable scaling paths.
*   **Lean & Modern Stack:** Employ technologies that enable rapid development and high effectiveness.
*   **User-Centric Design:** Focus on intuitive and simple user experiences for both members and treasurers.
*   **Security & Compliance:** Implement robust data security measures and adhere strictly to tax regulations.
*   **Continuous Improvement:** Embrace iterative development and incorporate user feedback for ongoing enhancements.

## Defined Roles

*   **Product Owner (PO):** Defines vision, prioritizes features, manages roadmap.
*   **Technical Lead (TL):** Oversees technical architecture, ensures code quality, guides development.
*   **AI/ML Engineer (AI/ML):** Focuses on OCR, data extraction, and AI model training.
*   **Backend Developer (BE):** Implements API, database interactions, business logic.
*   **Frontend Developer (FE):** Develops user interfaces for web and mobile.
*   **QA Engineer (QA):** Designs and executes test plans, ensures quality and stability.
*   **DevOps Engineer (DO):** Manages infrastructure, CI/CD, deployment.
*   **Gemini-CLI Agent (AI-Agent):** Assists with code generation, documentation, and task automation.

## Project Phases & Sprints

### Phase 0: Feasibility & Validation (Pre-Product)

*   **Status:** Completed
*   **Goal:** Validate market need, refine business model, and establish initial customer relationships.

    *   **Sprint 0.1: Deep Customer Discovery**
        *   **Tasks:** Interview 20-30 non-profit treasurers to validate pain points and gather feedback.
        *   **Assigned Roles:** PO

    *   **Sprint 0.2: Concierge MVP & Business Model Refinement**
        *   **Tasks:** Manually process receipts and fill forms for early customers; refine pricing strategy and go-to-market plan based on feedback.
        *   **Assigned Roles:** PO, TL

### Phase 1: Product Development (MVP)

*   **Status:** In Progress
*   **Goal:** Develop and launch the core application with essential features for initial user adoption.

    *   **Sprint 1.1: Requirements Gathering & Analysis**
        *   **Status:** Completed
        *   **Tasks:** Define core functionalities, user stories, technical specifications, mobile UX, expense/donation workflow, non-refundable categories, initial technical architecture, E-585/E-536R form requirements.
        *   **Assigned Roles:** PO, TL, AI-Agent

    *   **Sprint 1.2: Design & Prototyping**
        *   **Tasks:** Finalize database schema, design core API endpoints, authentication/authorization flows (including OAuth2 for "Sign in with Apple/Google"), create high-fidelity UI/UX mockups for mobile and web dashboards, design PDF generation interface.
        *   **Assigned Roles:** TL, BE, FE, AI/ML, QA

    *   **Sprint 1.3: Core Backend & AI Integration**
        *   **Tasks:** Set up FastAPI/Fastify backend, implement user/organization management (including OAuth2 for "Sign in with Apple/Google"), integrate BAML for AI-powered receipt data extraction, implement Cloudflare R2/Backblaze B2 for image storage.
        *   **Assigned Roles:** BE, AI/ML, TL, AI-Agent (for code generation)

    *   **Sprint 1.4: Mobile App Development**
        *   **Tasks:** Develop Svelte/Capacitor mobile app for receipt submission. Implement camera/photo library integration and submission review/confirmation screens. Add functionality for treasurers to submit receipts on behalf of members, including a CSV member import and search-as-you-type selection.
        *   **Assigned Roles:** FE, BE, QA, AI-Agent (for UI components, data binding)

    *   **Sprint 1.5: Web Dashboard & Reimbursement Workflow**
        *   **Tasks:** Develop SvelteKit web dashboard for treasurers. Implement receipt approval/rejection and payment reconciliation (CSV upload, matching).
        *   **Assigned Roles:** FE, BE, QA, AI-Agent (for dashboard components, workflow logic)

    *   **Sprint 1.6: PDF Generation Implementation**
        *   **Tasks:** Implement E-585 PDF generation logic, implement E-536R PDF generation logic, integrate PDF generation library.
        *   **Assigned Roles:** BE, QA, AI-Agent (for form-filling logic, scripts)

    *   **Sprint 1.7: Testing & Quality Assurance (MVP)**
        *   **Tasks:** Write/execute unit/integration tests, conduct initial UAT with early adopters, perform basic security/performance testing.
        *   **Assigned Roles:** QA, BE, FE, TL

    *   **Sprint 1.8: Initial Deployment (MVP)**
        *   **Tasks:** Set up initial production hosting (Vercel/Netlify, Railway/Render), configure basic CI/CD pipelines, deploy web dashboard and backend services.
        *   **Assigned Roles:** DO, TL

    *   **Sprint 1.9: Website Development**
        *   **Tasks:** Purchase and register the goodstewards.app domain. Develop a public-facing website to attract and inform potential users, primarily non-profit treasurers. The site will feature short videos, infographics, and testimonials to illustrate ROI.
        *   **Assigned Roles:** FE, PO, TL

    *   **Sprint 1.10: App Store Deployment**
        *   **Tasks:** Register for Apple Developer and Google Play Developer accounts, configure app store listings, prepare marketing materials (screenshots, descriptions), submit the mobile app for review and approval.
        *   **Assigned Roles:** PO, TL, FE

### Phase 2: Growth & Expansion (Post-MVP)

*   **Status:** To Do
*   **Goal:** Scale customer acquisition, expand feature set, and explore new markets.

    *   **Sprint 2.1: Post-Launch Monitoring & Support**
        *   **Tasks:** Monitor application performance/error logs, provide user support, address immediate issues.
        *   **Assigned Roles:** DO, QA, PO

    *   **Sprint 2.2: Customer Acquisition & Adoption**
        *   **Tasks:** Ramp up marketing/sales efforts, implement freemium model (if applicable), develop customer success strategies.
        *   **Assigned Roles:** PO

    *   **Sprint 2.3: Feature Enhancements & Optimizations**
        *   **Tasks:** Implement voice-to-text summary, integrate with accounting software (QuickBooks, Xero), develop advanced reporting, optimize existing features.
        *   **Assigned Roles:** PO, TL, BE, FE, AI/ML, QA, AI-Agent

    *   **Sprint 2.4: Geographic Expansion**
        *   **Tasks:** Investigate sales tax refund programs in other states, adapt product for new regulatory environments.
        *   **Assigned Roles:** PO, TL

## Cross-Cutting Concerns

*   **Metrics Capture & Analysis:** Define key performance indicators (KPIs) for user engagement, refund amounts, processing efficiency, and financial performance. Implement analytics tools to track and report on these metrics continuously.
    *   **Assigned Roles:** PO, TL, BE
*   **Security & Compliance:** Ongoing review and implementation of security best practices (data encryption, access control) and adherence to evolving tax laws and data privacy regulations.
    *   **Assigned Roles:** TL, BE, QA
*   **Beta Testing Program:** Establish a formal beta testing program for new features and major releases to gather early feedback and ensure quality.
    *   **Assigned Roles:** PO, QA
