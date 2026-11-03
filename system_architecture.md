# Architecture Document - OHMies

## 1. High-Level Architecture
OHMies follows a modern decoupled architecture utilizing a frontend Single Page Application (SPA), a Python-based RESTful API, and a managed PostgreSQL database.

## 2. Component Breakdown

### 2.1 Frontend (Client-Side)
*   **Framework:** React.js
*   **Styling:** Tailwind CSS & standard CSS modules.
*   **Structure:** Evaluates the provided HTML reference file to replicate the "Green Pass Road" UI components dynamically in React.

### 2.2 Backend (Server-Side)
*   **Framework:** FastAPI (Python)
*   **Responsibilities:** 
    *   Handle login verification.
    *   Serve aggregated statistical data to Tab-1 and Tab-2.
    *   Run ML models (scikit-learn) for insight generation if applicable.
    *   Manage file I/O for logging.

### 2.3 Data Layer
*   **Database:** Supabase (PostgreSQL).
*   **Existing Data:** Backend will connect to pre-populated Supabase tables containing historical consumption datasets.

### 2.4 Security & Configuration
*   **Credentials:** Saved in `.env` files (which are strictly added to `.gitignore` to prevent exposure in version control). The frontend will validate inputs against these variables or a backend auth route.

### 2.5 Logging System
*   **Log File Implementation:** The FastAPI backend will implement Python's `logging` module to write daily logs (`ohmies_access.log`) capturing login attempts, data fetch requests, and system errors.

### 2.6 Background Tasks (Loop File)
*   **Recurring Check:** A background Python script (the "loop file") utilizing a `while True` loop or asynchronous task scheduler (like Celery or APScheduler) to continuously process/match data streams until an optimal conservation match/insight is found for the user's profile.