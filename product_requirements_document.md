# Product Requirements Document (PRD) - OHMies

## 1. Project Overview
**OHMies** is a smart web platform designed to help users track, store, and analyze their electricity consumption data. The platform provides actionable insights and hardcoded smart tips to promote electricity conservation and optimize usage.

## 2. Target Audience & Sector Classification
The platform caters to two primary electricity sectors:

### 2.1 Domestic Household (Apartments and Villas)
*   High-Rise Apartments
*   Independent Bungalows
*   Compact Studio or Shared

### 2.2 Commercial or Industries (MSME)
*   **Micro:** Flour Mill, Garment and Tailor, Salon and Wellness
*   **Small:** Auto Garage, Photo Studio, Commercial Bakery
*   **Medium:** IT/CO Workspace, Retail Showroom, 24/7 Cold Pharmacy

## 3. Core Features & Requirements

### 3.1 Authentication
*   **Login Page:** Simple UI to capture UID (Name) and Password.
*   **Validation:** Hardcoded validation against predefined credentials (stored securely, ignored via `.gitignore` using environment variables).
*   **Error Handling:** If credentials do not match, strictly deny access and display: `<span style="color: darkred;">Invalid UID and Password, pls try again later</span>`.

### 3.2 Main Dashboard UI/UX
*   **Top Header:** 
    *   Left side: "Welcome User" (Slightly larger font).
    *   Extreme Right side: "Goal".
*   **Aesthetics:** Incorporate internet-sourced imagery to enhance UI/UX and make the application visually attractive.

### 3.3 Application Structure (Tabs)
The application is divided into three strictly sequential tabs.

#### Tab-1: Homepage / General Layout
*   **Core Metrics:**
    *   Average Daily Draw
    *   Peak Window Intensity
    *   Grid Carbon Footprint
    *   Tariff Bracket
*   **Message Summary:** A dynamic text block summarizing the user's current statistical usage and providing immediate recommendations on what to do next.

#### Tab-2: Statistical Values
*   **Visualizations:** 
    *   General Graphs
    *   Pie-Charts
    *   Bar Graph (Per Week consumption)
*   **Smart Tips:** Hardcoded, predefined tips for energy conservation based on sector.

#### Tab-3: Savings & Impact
*   **Financial Savings:** Displays how much money can be saved.
*   **Design Reference:** Must strictly follow the structure and style of "The Green Pass Road" section from the provided reference HTML file.

## 4. Data & Logging Requirements
*   Integrate with existing Supabase datasets.
*   Extract structures from the provided sample demo HTML file (without rebuilding the exact file, just taking UI/structure inputs).
*   Implement a server-side log file to store transactional and user data.