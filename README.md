<h1 align="center">GoodStewards<br>
<span style="font-size: 0.75em; font-style: italic;">a Non-Profit Sales Tax Refund Automation</span></h1>

## Summary

This project is the foundation for a mobile and web platform that automates the process for non-profit organizations in North Carolina to claim refunds on state, county, and transit sales and use taxes. By simplifying receipt submission and automating the generation of official tax forms, we empower non-profits to reclaim significant funds that are often left unclaimed due to tedious manual processes.

## Problems and Challenges

*   **Complex and Labor-Intensive Process:** The process of collecting receipts, meticulously extracting data, and accurately filling out Form E-585 (and the supplementary Form E-536R if expenses span multiple counties) is complex and time-consuming.
*   **Volunteer Burden:** This burden often falls on volunteer treasurers who are short on time, leading to a significant loss of funds for the organization.
*   **Inefficient Reimbursement:** The associated manual expense reimbursement workflow is inefficient, often requiring in-person meetings and manual check-writing.
*   **Missing County Information:** Most receipts do not explicitly list the county as part of the vendor's address, yet the county is essential for accurately calculating the sales tax breakdown for the refund claim.
*   **Manual Calculation for Members:** Members often have to manually sum up totals for multiple receipts, which is an error-prone and tedious task.
*   **Fading Physical Receipts:** Physical receipts fade over time, becoming illegible and making it impossible to claim refunds for older expenses.

## Proposed Solution

We are building a unified web and mobile application designed to streamline the entire workflow from receipt submission to refund claim.

*   **For Members:** A simple, intuitive mobile application allows members to instantly submit expenses by photographing receipts. The platform handles all data entry and calculations automatically.
*   **For Treasurers:** A secure web dashboard provides a central hub for managing finances. It uses AI to extract data from receipts, categorizes expenses, facilitates a seamless electronic reimbursement workflow, and generates a print-ready Form E-585 with one click.

This solution saves valuable time, eliminates administrative friction, and ensures non-profits maximize their financial resources.

## Build and Run

To get the project up and running, follow these steps:

1.  **Ensure Docker is installed:** Make sure you have Docker Desktop or Docker Engine installed and running on your system.
2.  **Navigate to the project root:** Open your terminal or command prompt and change your current directory to the root of this project (where `docker-compose.yml` is located).
3.  **Build and run the services:** Execute the following command:

    ```bash
    docker compose up --build
    ```

    This command will:
    *   Build the `backend` service using the `Dockerfile` in the `backend/` directory.
    *   Start the PostgreSQL database service.
    *   Start the backend API service.

4.  **Access the application:**
    *   The backend API will be accessible at `http://localhost:8000`.

---

### Further Documentation

For more detailed information, please see the documents in the `docs/` folder:

*   **Technical Documentation**
    *   [**Technical Design Specification**](./docs/technical/tech_design_spec.md)
    *   [**Database Schema**](./backend/DATABASE_SCHEMA.md)
    *   [**Development Specification**](./docs/technical/dev_spec.md)
    *   [**Architecture Specification**](./docs/technical/architecture_spec.md)
*   **Business Documentation**
    *   [**Epics, Use Cases & Roadmap**](./docs/business/epics_usecases_roadmap.md)
    *   [**Project Feasibility Assessment**](./docs/business/project_feasibility_assesment.md)
    *   [**ROI Success Metrics**](./docs/business/roi_success_metrics.md)
    *   [**Target Audience**](./docs/business/target_audience.md)
*   **User Experience Documentation**
    *   [**Dashboard UX**](./docs/user_experience/dashboard_ux.md)
    *   [**Mobile UX**](./docs/user_experience/mobile_ux.md)
    *   [**Website UX**](./docs/user_experience/website_ux.md)
*   [**Forms**](./docs/forms)
    *   [**E-536R_5-20-24_webfill_v1_Final.pdf**](./forms/E-536R_5-20-24_webfill_v1_Final.pdf)
    *   [**e585_example_6-11-24_v.03.pdf**](./forms/e585_example_6-11-24_v.03.pdf)
    *   [**e585-Webfill-Final-01052021.pdf**](./forms/e585-Webfill-Final-01052021.pdf)
