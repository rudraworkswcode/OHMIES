# OHMies — System Architecture

## 1. Architecture Overview

OHMies follows a layered web application architecture.

### Technology flow

Browser → React Frontend → FastAPI Backend → Supabase Database

```text
                USER
                  |
                  v
          REACT FRONTEND
          (Tailwind + CSS)
                  |
                  v
           FASTAPI BACKEND
                  |
          ------------------
          |        |       |
          v        v       v
       AUTH     ANALYSIS  APIs
          |        |       |
          ------------------
                  |
                  v
              SUPABASE
                  |
          -----------------
          |               |
          v               v
       DATABASE        DATASETS
```

The frontend handles presentation and user interaction.

The backend handles authentication verification, data processing, calculations and API communication.

Supabase stores the actual application and electricity consumption data.

---

## 2. Frontend Architecture

Technology:
- React
- Tailwind CSS
- Custom CSS
- HTML5
- Recharts or Chart.js

Suggested structure:

```text
frontend/
|
|-- src/
|   |
|   |-- app/
|   |   |-- App.jsx
|   |   |-- routes.jsx
|   |
|   |-- components/
|   |   |-- Header.jsx
|   |   |-- MetricCard.jsx
|   |   |-- Navigation.jsx
|   |   |-- LoadingState.jsx
|   |   |-- ErrorState.jsx
|   |   |
|   |   |-- charts/
|   |
|   |-- pages/
|   |   |-- LoginPage.jsx
|   |   |-- OverviewPage.jsx
|   |   |-- AnalyticsPage.jsx
|   |   |-- SavingsPage.jsx
|   |
|   |-- services/
|   |   |-- api.js
|   |
|   |-- styles/
|   |
|   |-- utils/
|
|-- package.json
```

### Frontend responsibilities

**LoginPage.jsx**
- Collect UID and password.
- Validate input.
- Communicate with authentication service.
- Display invalid credentials message.

**OverviewPage.jsx**
- Display Welcome User.
- Display Goal.
- Display four primary metrics.
- Display consumption summary.

**AnalyticsPage.jsx**
- Render graphs.
- Render pie charts.
- Render weekly bar charts.
- Display Smart Tips.

**SavingsPage.jsx**
- Display financial savings.
- Display electricity conservation opportunities.
- Adapt the Green Pass Road reference.

**api.js**
- Centralise API requests.
- Handle authentication headers.
- Handle API errors.

---

## 3. Backend Architecture

Technology:
- Python
- FastAPI
- Pandas
- NumPy
- Scikit-learn

Suggested structure:

```text
backend/
|
|-- app/
|   |
|   |-- main.py
|   |
|   |-- api/
|   |   |-- auth.py
|   |   |-- overview.py
|   |   |-- analytics.py
|   |   |-- savings.py
|   |
|   |-- core/
|   |   |-- config.py
|   |   |-- security.py
|   |   |-- logging_config.py
|   |
|   |-- db/
|   |   |-- supabase_client.py
|   |
|   |-- schemas/
|   |
|   |-- services/
|       |-- consumption.py
|       |-- tariffs.py
|       |-- emissions.py
|       |-- recommendations.py
|
|-- tests/
```

### Backend responsibilities

**main.py**
- Initialise FastAPI.
- Register API routers.
- Configure middleware.
- Configure CORS.

**auth.py**
- Authentication integration.
- Session verification.
- Protected endpoint access.

**overview.py**
- Fetch electricity consumption.
- Calculate dashboard metrics.
- Generate summary inputs.

**analytics.py**
- Process historical data.
- Calculate weekly consumption.
- Prepare chart-ready information.

**savings.py**
- Calculate estimated savings.
- Compare baseline and proposed consumption.
- Calculate potential financial benefits.

**consumption.py**
- Data cleaning.
- Aggregation.
- Statistical analysis.

**recommendations.py**
- Select relevant predefined Smart Tips.

---

## 4. Supabase Integration

Supabase will act as the primary data storage system.

Before implementing database queries, inspect the existing Supabase schema.

Potential logical entities:

| Entity | Purpose |
|---|---|
| Profiles | User information and sector classification |
| Consumption Records | Electricity consumption data |
| Tariff Configs | Electricity tariff information |
| Emission Factors | Grid carbon emission factors |
| Goals | User conservation targets |
| Smart Tips | Predefined recommendations |

These are conceptual entities. Reuse existing tables wherever possible.

### Data flow

1. User logs in.
2. Authentication is verified.
3. User profile is retrieved.
4. Sector and subcategory are identified.
5. Relevant electricity records are fetched.
6. Backend processes the records.
7. Statistical values are calculated.
8. API sends the results to React.
9. React renders the dashboard.

Never trust a user ID supplied by the browser as proof of identity.

Use the authenticated session to determine which records the user can access.

---

## 5. Suggested API Endpoints

| Method | Endpoint | Function |
|---|---|---|
| POST | /api/auth/login | Authenticate user |
| POST | /api/auth/logout | Logout |
| GET | /api/auth/me | Fetch user profile |
| GET | /api/overview | Dashboard metrics |
| GET | /api/analytics/consumption | Consumption analytics |
| GET | /api/analytics/tips | Smart Tips |
| GET | /api/savings/estimate | Savings calculation |

These are proposed endpoint names. Adapt them if the existing project already has equivalent routes.

### Example overview response

```json
{
  "average_daily_draw": {
    "value": 12.4,
    "unit": "kWh/day"
  },
  "peak_window_intensity": {
    "value": 2.1,
    "unit": "kWh",
    "window": "18:00-21:00"
  },
  "grid_carbon_footprint": {
    "value": 84.2,
    "unit": "kg CO2e"
  },
  "tariff_bracket": {
    "label": "Configured tariff",
    "rate": null
  }
}
```

**Note:** This is an illustrative API response only. Its numerical values must never be presented as actual user consumption.

---

## 6. Calculation Architecture

All important calculations should be handled in reusable backend services.

### Average Daily Draw

Total energy consumed divided by the number of covered days.

### Peak Window Intensity

Identify the highest-use time window.

Clearly distinguish:
- Energy: kWh
- Power/demand: kW

### Grid Carbon Footprint

Energy consumption × applicable emissions factor.

### Tariff

Use the actual applicable tariff structure.

Account for slabs, fixed charges and other relevant components where available.

### Savings

Compare the baseline electricity cost against the estimated cost after a proposed reduction.

All calculations must be testable and reproducible.

---

## 7. Security Architecture

- Use Supabase Auth for production authentication.
- Enable Supabase Row Level Security.
- Keep service-role keys exclusively on the backend.
- Store secrets in environment variables.
- Never commit real credentials.
- Use HTTPS in deployment.
- Validate incoming requests.
- Apply login rate limiting.
- Do not log passwords or tokens.

The frontend must not be the only layer protecting dashboard access.

---

## 8. Logging Architecture

Create structured application logs.

Record:
- Timestamp.
- Log severity.
- Request ID.
- API endpoint.
- Response status.
- Request duration.
- Safe user identifier where appropriate.

Do not record:
- Passwords.
- Access tokens.
- Refresh tokens.
- Session cookies.
- Private API keys.

Keep development logs in ignored local files and configure retention for production.

---

## 9. Testing Architecture

Use:
- Pytest for backend tests.
- Frontend testing tools appropriate to the existing React setup.
- API integration tests.
- Authentication tests.
- Calculation validation tests.

Test:
- Invalid login.
- Valid login.
- Unauthenticated API requests.
- Cross-user data access.
- Missing datasets.
- Duplicate records.
- Incorrect units.
- Missing timestamps.
- Empty charts.
- Incorrect aggregation.

Never report a feature as complete without testing it.