# Technical Architecture

This document outlines the proposed technical architecture, emphasizing open-source technologies, cost-effective hosting, and a maintainable, scalable structure.

### Guiding Principles
*   **Open Source First:** Prioritize well-supported open-source libraries and frameworks to avoid vendor lock-in and manage costs.
*   **Cost-Effective Scalability:** Choose hosting and service providers that offer generous free tiers and predictable, affordable scaling paths.
*   **Lean & Modern Stack:** Employ technologies that enable rapid development and a small team to be highly effective.

---

### Frontend Recommendation

Between the two proposed stacks, we recommend the **Svelte-based stack** for its simplicity, performance, and excellent developer experience, which is ideal for a startup.

*   **Recommendation: Svelte (SvelteKit + Capacitor)**
    *   **Web Dashboard:** **SvelteKit** provides a powerful, file-based routing and server-side rendering framework that is incredibly fast and intuitive.
    *   **Mobile App:** **Capacitor** allows us to wrap the Svelte web app into a native mobile shell for iOS and Android, providing access to native device features like the camera with minimal overhead. This "write once, adapt everywhere" approach is highly efficient.
*   **Why Svelte?**
    *   **Performance:** Svelte is a compiler that turns components into highly optimized, vanilla JavaScript at build time, resulting in smaller bundles and a faster app.
    *   **Simplicity:** The learning curve is gentle, and the code is often more concise and readable than other frameworks.
    *   **Unified Tooling:** The synergy between SvelteKit and Capacitor creates a seamless development workflow for both web and mobile.

---

### Core Architecture Components

*   **Frontend (Web & Mobile):** SvelteKit for the Treasurer Web Dashboard, packaged with Capacitor for the Member Mobile App.
*   **Backend API:** **FastAPI (Python)** or **Fastify (Node.js)**. Both are high-performance, modern frameworks perfect for building a robust API. FastAPI is an excellent choice if the team has Python experience, especially for future data science tasks.
*   **AI Layer (Receipt Processing):**
    *   **BAML (Boundary-spanning Action and Meaning Language):** We will use BAML to define our AI functions for interacting with Google's Gemini 1.5 Pro.
    *   **How it works:** BAML allows us to define the `ExtractReceiptData` function declaratively, specifying its inputs (image) and outputs (structured JSON with vendor, date, taxes, etc.). This separates the prompt engineering and LLM logic from the application code, making it highly maintainable and testable. The backend service will call the BAML-defined function, which then handles the API call to Gemini via a secure API key.
*   **Authentication & Authorization:**
    *   **Protocol:** **OAuth 2.0** will be the core protocol for secure authentication.
    *   **Implementation:** **Auth.js** (formerly NextAuth.js, now framework-agnostic) is a highly recommended open-source library that simplifies implementing OAuth with various providers (Google, etc.) and managing sessions.
    *   **Authorization:** A **Role-Based Access Control (RBAC)** system will be implemented in the backend. An authenticated user's token will contain their role (`treasurer` or `member`), which the API will use to protect endpoints and resources.
*   **Database:** **PostgreSQL**. It is a powerful, open-source, and reliable relational database that is well-supported by all major cloud and hosting providers.
*   **File Storage:** **Cloudflare R2** or **Backblaze B2**. These services offer S3-compatible APIs for storing receipt images but with significantly lower (or zero) egress fees, making them highly cost-effective compared to AWS S3.
*   **PDF Generation:** A server-side library like `PyPDF2` (Python) or `pdf-lib` (Node.js) to programmatically fill the Form E-585 PDF template.

---

### Hosting Strategy

*   **Frontend:** **Vercel** or **Netlify**. Both offer excellent free tiers for hosting modern frontend applications, with global CDNs, CI/CD, and seamless integration with GitHub.
*   **Backend & Database:** **Railway** or **Render**. These platforms simplify deploying backend services and databases. They provide managed infrastructure with auto-scaling, predictable pricing, and generous free tiers to start.

### High-Level Architectural Flow

```mermaid
graph TD
    A[Member's Mobile App<br/>Svelte/Capacitor] -->|Login via OAuth 2.0| B[Auth.js]
    A -->|Uploads Receipt Image| C[API Server<br/>FastAPI/Fastify]
    
    H[Treasurer's Web App<br/>SvelteKit] -->|Fetches data, manages approvals| C
    
    C -->|Stores Image| D[Cloudflare R2<br/>File Storage]
    C -->|Calls BAML Function| E[BAML Runtime]
    C -->|Stores Data| G[PostgreSQL DB]
    
    E -->|Invokes Gemini 1.5 Pro| F[Google AI Platform]
    F -->|Returns Structured JSON| E
    E -->|Returns JSON to API| C
    
    style A fill:#e1f5fe,color:#000000
    style H fill:#e1f5fe,color:#000000
    style C fill:#f3e5f5,color:#000000
    style B fill:#fff3e0,color:#000000
    style D fill:#e8f5e8,color:#000000
    style E fill:#fff8e1,color:#000000
    style F fill:#fce4ec,color:#000000
    style G fill:#e0f2f1,color:#000000
```