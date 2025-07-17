# GEMINI Code Generation - Consolidated Project Standards

This document consolidates all standards and best practices. It should be considered the single source of truth for generating code for this project.

## 1. Project Foundation & Structure

This section defines the overall structure and foundational principles for the entire project.

### 1.1. Monorepo Project Folder Structure

The project is organized as a monorepo. All generated code must adhere to this structure.
```
/
├── .github/workflows/ # CI/CD pipelines (e.g., ci.yml)
│
├── backend/ # Python FastAPI Application
│ ├── app/
│ │ ├── api/ # API routers (e.g., api/v1/receipts.py)
│ │ ├── core/ # App configuration, security
│ │ ├── models/ # SQLModel table models (e.g., user_model.py)
│ │ ├── schemas/ # Pydantic schemas for API I/O (e.g., receipt_schema.py)
│ │ ├── services/ # Business logic (e.g., receipt_service.py)
│ │ └── init.py
│ ├── alembic/ # Database migrations
│ ├── tests/ # Pytest tests
│ ├── .env # Local environment variables (in .gitignore)
│ ├── pyproject.toml # Project metadata and dependencies (Poetry)
│ └── README.md # Backend-specific instructions
│
├── frontend/ # SvelteKit Application
│ ├── src/
│ │ ├── lib/
│ │ │ ├── client/ # Client-side only code
│ │ │ ├── server/ # Server-side only code (DB clients, etc.)
│ │ │ └── components/ # Reusable Svelte components
│ │ ├── routes/ # SvelteKit file-based routing
│ │ └── app.html
│ ├── static/ # Static assets (favicon, images)
│ ├── tests/ # Vitest tests
│ ├── .env # Local environment variables
│ └── package.json
│
├── website/ # Static marketing website
│ ├── css/
│ ├── js/
│ ├── assets/
│ └── index.html
│
└── .env.example # Template for environment variables
```

### 1.2. Environment & Configuration
*   **NEVER** hardcode secrets (API Keys, DB URLs, JWT secrets).
*   All configuration must be loaded from environment variables using `pydantic-settings` for the backend.
*   A `.env.example` file must always be maintained at the root.

### 1.3. Dependency Management
*   **Backend:** Use **Poetry** (`pyproject.toml`).
*   **Frontend:** Use **pnpm** (`package.json`, `pnpm-lock.yaml`).

### 1.4. Testing Strategy
*   Code without tests is incomplete. All features must include corresponding tests.
*   **Backend:** Use **Pytest**. Write unit tests for services and integration tests for API endpoints.
*   **Frontend:** Use **Vitest** with **@testing-library/svelte**. Write unit tests for components and stores.

### 1.5. CI/CD Pipeline
*   Generate **GitHub Actions** workflows.
*   The CI pipeline must run linters (`black`, `ruff`, `eslint`) and the full test suite for both backend and frontend on every pull request to `main`.

---

## 2. Core Code Generation Directives

*   **Error Handling is Mandatory:** Use `try...catch` (JS/Svelte) or `try...except` (Python) for any operation that can fail (API calls, DB ops, I/O).
*   **Logging Over Printing:** Use Python's `logging` module for structured backend logging. Never use `print()`.
*   **Readability:** Write code that is easy to read and understand. Use clear, descriptive names. Add comments only to explain the "why" of complex logic.
*   **Completeness:** Generated code must be complete, runnable, and include all necessary imports.

---

## 3. Backend: Python / FastAPI / SQLModel

*   **Structure:** Adhere to the monorepo structure. Use `APIRouter` to modularize endpoints.
*   **Error Handling:** Catch specific exceptions (e.g., `sqlalchemy.exc.IntegrityError`) and re-raise as `HTTPException` with correct status codes (`400`, `409`). A global handler should catch unhandled errors and return a generic `500`.
*   **Database (SQLModel & PostgreSQL):**
    *   Use **asynchronous** database sessions (`AsyncSession`).
    *   Manage sessions using FastAPI's dependency injection (`Depends`).
    *   Define table models by inheriting from `SQLModel, table=True`.
    *   Use **Alembic** for all schema migrations.
*   **Security (OAuth2 & RBAC):**
    *   Use `passlib` for password hashing.
    *   Implement **OAuth2** with a reusable dependency (`get_current_active_user`) to validate JWT tokens and protect endpoints.
    *   Implement **Role-Based Access Control (RBAC)** within the security dependency.
*   **Code Style:** Strictly adhere to **PEP 8**, use **type hints** everywhere, and use f-strings.

---

## 4. Frontend: SvelteKit / Capacitor

*   **Structure & Data Loading:**
    *   Adhere to the monorepo structure. Use `$lib` aliases.
    *   Fetch data in `+page.server.ts` or `+layout.server.ts` `load` functions.
*   **Error Handling:**
    *   In `load` functions, use SvelteKit's `@sveltejs/kit/error` helper.
    *   For client-side API calls, use `try...catch` and update the UI with a user-friendly error state.
*   **State Management & Forms:** Use Svelte Stores for shared state. Use SvelteKit's `enhance` action and consider `superforms` for complex forms.
*   **Styling:** Use **TailwindCSS** for utility-first CSS. Scope component-specific overrides in the `<style>` block.
*   **Accessibility (a11y):** All code must be accessible. Use semantic HTML, ensure keyboard navigability, and provide `alt` text and `aria-label`s.

---

## 5. Website: HTML5 / CSS / Vanilla JS

*   **HTML:** Use semantic HTML5. The document must be well-formed with `lang`, `charset`, `viewport`, and a descriptive `<title>`.
*   **CSS:** Implement a **mobile-first** design. Use **CSS Custom Properties** for theming.
*   **JavaScript:** Use modern **ES6+** syntax. Wrap code in a `DOMContentLoaded` event listener. Do not pollute the global scope.

---

## 6. User-Specific Preferences

### 6.1. Git Branching Strategy

- **Main Development Branch:** `develop`
- **Feature Branches:** `feature/<feature-name>` (from `develop`)
- **Release Branches:** `release/<version>` (from `develop`)
- **Hotfix Branches:** `hotfix/<description>` (from `main`)

### 6.2. Styling Preferences

- **Preferred Style:** fill: `#e1f5fe`, color: `#000000`
- **Alternative Style (B):** fill: `#fff3e0`, color: `#000000`
