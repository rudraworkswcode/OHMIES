# OHMies — Technology Stack

## 1. Technology Overview

OHMies will use the following technology stack.

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React | User interface |
| Styling | Tailwind CSS | Responsive styling |
| Custom Styling | CSS | Additional UI customisation |
| Backend | FastAPI | API development |
| Programming Language | Python | Backend and data processing |
| Database | Supabase | Data storage |
| Authentication | Supabase Auth | Secure login |
| Data Processing | Pandas | Dataset processing |
| Numerical Analysis | NumPy | Statistical calculations |
| Machine Learning | Scikit-learn | Optional predictive analysis |
| Charts | Recharts / Chart.js | Data visualisation |
| Markup | HTML5 | Semantic structure |
| Testing | Pytest | Backend testing |
| Version Control | Git | Source control |

---

## 2. Frontend Technologies

### React

React will be used to build the website.

Responsibilities:
- Component-based development.
- Dashboard rendering.
- Navigation between tabs.
- API communication.
- Authentication state management.
- Dynamic data rendering.

### Tailwind CSS

Used for:
- Responsive layouts.
- Metric cards.
- Navigation.
- Typography.
- Buttons.
- Spacing.
- UI consistency.

### Custom CSS

Use CSS for:
- Animations.
- Special dashboard effects.
- Custom backgrounds.
- Unique visual components.

### Recharts / Chart.js

Use one charting library consistently.

Recommended default: Recharts.

Used for:
- Line graphs.
- Pie charts.
- Weekly bar graphs.
- Consumption trends.

All charts must use actual dataset values.

---

## 3. Backend Technologies

### Python

Primary backend programming language.

### FastAPI

Used for:
- Authentication integration.
- API development.
- Database communication.
- Data processing.
- Statistical calculations.
- Savings calculations.

### Pandas

Used for:
- Dataset loading.
- Data cleaning.
- Grouping.
- Filtering.
- Weekly aggregation.
- Historical consumption analysis.

### NumPy

Used for:
- Numerical calculations.
- Statistical operations.
- Data transformations.

---

## 4. Database — Supabase

Supabase is the primary database.

Responsibilities:
- Store user information.
- Store electricity consumption records.
- Store relevant configuration data.
- Retrieve historical datasets.
- Support authenticated access.

Important:
- Inspect existing Supabase tables before implementation.
- Reuse existing datasets.
- Enable Row Level Security.
- Never expose the service-role key to React.

---

## 5. Machine Learning — Scikit-learn

Scikit-learn is included for future intelligent analysis.

Possible applications:

1. Electricity consumption anomaly detection.
2. Consumption trend forecasting.
3. Baseline usage estimation.
4. Identification of unusual consumption patterns.

However, machine learning is not mandatory for the first dashboard implementation.

First establish:
- Reliable data.
- Correct calculations.
- Descriptive statistics.
- Transparent recommendations.

Only introduce ML when there is enough clean historical data and a measurable benefit.

Never present predictions as guaranteed outcomes.

---

## 6. Environment Variables

Create a local `.env` file for sensitive configuration.

Example `.env.example`:

```env
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=server_only_secret
FRONTEND_ORIGIN=http://localhost:5173
ENVIRONMENT=development
```

Do not place actual credentials in `.env.example`.

The actual `.env` must be excluded from Git.

Suggested `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example

__pycache__/
*.pyc

node_modules/
dist/

logs/
*.log

.venv/
venv/

.DS_Store
```

Do not expose server secrets in frontend environment variables.

---

## 7. Suggested Project Structure

```text
OHMies/
|
|-- frontend/
|
|-- backend/
|
|-- data/
|   |-- README.md
|
|-- references/
|   |-- README.md
|
|-- docs/
|   |-- PRD.md
|   |-- Architecture.md
|   |-- Tech-stack.md
|   |-- sample-data.md
|   |-- phases.md
|
|-- .env.example
|-- .gitignore
|-- README.md
```

Adapt this structure to the existing repository.

Do not force a complete rewrite if a working project structure already exists.

---

## 8. Development Environment

Frontend:
- Node.js.
- React.
- Tailwind CSS.
- Vite, if appropriate for the existing project.

Backend:
- Python.
- FastAPI.
- Uvicorn.
- Required Python dependencies.

Database:
- Existing Supabase project.

Use the versions and package manager compatible with the existing repository.

---

## 9. Deployment

Deployment should include:

- Secure frontend hosting.
- FastAPI backend hosting.
- Supabase database.
- Environment-based secret management.
- HTTPS.
- Restricted CORS.
- Verified authentication.
- Verified RLS policies.
- Application logging and error monitoring.

---

## 10. Technology Selection Philosophy

Do not introduce additional frameworks or unnecessary dependencies without a reason.

Prioritise:
1. Reliability.
2. Security.
3. Maintainability.
4. Performance.
5. Simplicity.

The objective is to build a working electricity analytics platform, not simply a website containing many technologies.