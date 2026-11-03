# Development Phases - OHMies

The development of OHMies is strictly sequential. You are not allowed to proceed to the next phase or go back once a phase is completed and approved.

## Phase 1: Setup & Tab-1 (General Layout)
*   **Tasks:**
    *   Initialize React frontend and FastAPI backend.
    *   Setup `.env` and `.gitignore` for `NAME: Jeevan` and `PASSWORD: JAI RNSIT`.
    *   Build Login Screen with dark red error handling.
    *   Create Top Header ("Welcome User" & "Goal").
    *   Integrate internet UI/UX imagery.
    *   Build Tab-1 metrics UI (Average Daily Draw, Peak Window Intensity, Grid Carbon Footprint, Tariff Bracket).
    *   Implement dynamic message summary.
*   **Gate:** Tab-1 must be fully functional and pixel-perfect before moving to Phase 2.

## Phase 2: Tab-2 (Statistical Values)
*   **Tasks:**
    *   Integrate charting libraries (e.g., Chart.js or Recharts).
    *   Build the Graphs, Pie-Charts, and weekly Bar Graphs.
    *   Implement the hardcoded Smart Tips specific to the chosen sector classification (Domestic vs. Commercial).
*   **Gate:** Ensure data visualizations accurately reflect the Supabase datasets.

## Phase 3: Tab-3 (Savings & Reference UI)
*   **Tasks:**
    *   Extract the structure and style from the provided "The Green Pass Road" demo HTML file.
    *   Recreate the layout in React/Tailwind.
    *   Display monetary savings data based on Tab-2's insights.
    *   Implement the backend log file creation and the recurring loop script.
*   **Gate:** Final UI polish and end-to-end testing.