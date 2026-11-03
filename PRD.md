# OHMies — Product Requirements Document

## 1. Product Overview

**Product Name:** OHMies  
**Category:** Smart Electricity Monitoring and Conservation Platform

OHMies is a smart web application designed to help domestic households and commercial establishments monitor electricity consumption, store historical data, identify consumption patterns, and discover opportunities to conserve electricity.

The platform should transform raw electricity data into meaningful insights and actionable recommendations.

### Core Objectives

1. Track and monitor electricity consumption.
2. Store and retrieve historical consumption data.
3. Analyse electricity usage patterns.
4. Identify peak consumption periods.
5. Calculate electricity costs and potential savings.
6. Estimate grid-related carbon emissions.
7. Provide smart electricity conservation tips.
8. Help users make informed decisions using statistical insights.

---

## 2. User Classification

OHMies supports two major electricity sectors.

### A. Domestic Household

Applicable to apartments, villas and residential properties.

Subcategories:

- High-Rise Apartments
- Independent Bungalows
- Compact Studio or Shared Accommodation

### B. Commercial / Industrial

Classified into three business-size groups.

**MICRO**
- Flour Mill
- Garment and Tailor
- Salon and Wellness

**SMALL**
- Auto Garage
- Photo Studio
- Commercial Bakery

**MEDIUM**
- IT / Co-working Space
- Retail Showroom
- 24/7 Cold Pharmacy

The application must store the sector and corresponding subcategory for each user.

---

## 3. Authentication System

Create a login page that prevents unauthenticated users from accessing the application.

### Login requirements

- User ID / Name field.
- Password field.
- Login button.
- Validation for both fields.
- Protected dashboard routes.
- Backend authentication and authorization.

### Invalid credentials

Display the following exact message:

**Invalid UID and Password, pls try again later**

Styling:
- Dark red text.
- Clearly visible below the login form.
- Do not reveal whether the UID or password was incorrect.

### Security requirements

- Do not hardcode credentials in React.
- Use Supabase Auth for production authentication.
- For local development credentials, use an ignored `.env` file.
- Never store plaintext passwords in Git.
- Use secure password hashing if implementing local authentication.
- Protect backend APIs, not just frontend routes.
- Use Supabase Row Level Security.

Example development identity:
- UID: Jeevan
- Password: Configure locally; do not commit the plaintext password.

---

## 4. Application Structure

The application contains three major tabs.

### TAB 1 — OVERVIEW

This is the first development priority.

#### Header

Left side:
- Display `Welcome User`.
- Slightly larger font.
- Replace User with the authenticated user's display name.

Extreme right:
- Display `Goal`.
- Show the user's electricity conservation target if configured.

#### Main dashboard metrics

Four primary metric cards:

**1. Average Daily Draw**
- Average electricity consumption per day.
- Display in kWh/day.
- Show reporting period.

**2. Peak Window Intensity**
- Identify the highest electricity consumption window.
- Show the relevant time period.
- Distinguish energy (kWh) from demand/power (kW).

**3. Grid Carbon Footprint**
- Estimate carbon emissions associated with electricity consumption.
- Display in kg CO2e.
- Use a documented emissions factor.

**4. Tariff Bracket**
- Show the applicable electricity tariff category or rate.
- Use available tariff information.
- Do not assume a flat tariff if the tariff structure contains slabs or other charges.

#### Consumption Summary

Below the metric cards, display an intelligent summary explaining:

- How much electricity the user is consuming.
- Whether consumption is increasing or decreasing.
- Which time periods have higher consumption.
- What the user should do to conserve electricity.
- Relevant statistical values supporting the explanation.

All insights must be derived from actual dataset values.

If data is unavailable, display an appropriate message rather than inventing statistics.

### TAB 1 COMPLETION REQUIREMENTS

- Fully working login.
- Functional overview page.
- Four metric cards.
- Usage summary.
- Supabase integration.
- Responsive UI.
- Proper loading and error states.
- Verified statistical calculations.

Do not proceed to Tab 2 until Tab 1 is approved.

---

### TAB 2 — ANALYTICS

This is the second development priority.

The page must contain:

#### Graphs
- Electricity consumption over time.
- Consumption trends.
- Historical usage comparisons.

#### Pie Charts
- Consumption breakdown by available categories.
- Use only when the dataset supports a meaningful breakdown.

#### Weekly Bar Graph
- Electricity consumption per week.
- Clearly labelled weekly values.
- Correct aggregation and units.

#### Smart Tips

Create a predefined, hardcoded Smart Tips catalogue.

Tips should be selected based on:
- User sector.
- User subcategory.
- Observed electricity consumption patterns.

Examples:
- Switch off unused appliances.
- Reduce unnecessary lighting.
- Improve AC usage practices.
- Avoid unnecessary equipment idle time.
- Maintain refrigeration equipment.

Do not claim guaranteed savings without supporting calculations.

### TAB 2 COMPLETION REQUIREMENTS

- All charts work correctly.
- Correct data aggregation.
- Weekly consumption visualisation.
- Smart Tips are displayed.
- Date filtering where supported.
- Responsive design.

Do not proceed to Tab 3 until Tab 2 is approved.

---

### TAB 3 — SAVINGS / GREEN PASS ROAD

This is the third development priority.

The user will provide an existing HTML reference containing the Green Pass Road concept.

**IMPORTANT:** Inspect the entire Green Pass Road section before implementation.

Requirements:

- Understand the existing structure.
- Study the design and visual hierarchy.
- Extract relevant calculations and functionality.
- Adapt the structure into the existing React application.
- Do not recreate the original HTML as a separate duplicate website.

The page should communicate:

- How much money the user could save.
- Potential electricity consumption reduction.
- Financial benefits of conservation.
- Environmental benefits.
- Practical actions that can produce savings.

Every calculation must be transparent.

Show:
- Baseline consumption.
- Applicable tariff.
- Assumed reduction.
- Estimated savings.
- Calculation period.

Clearly distinguish projected savings from actual savings.

### TAB 3 COMPLETION REQUIREMENTS

- Green Pass Road reference inspected.
- Relevant design adapted.
- Savings calculations implemented.
- Financial assumptions displayed.
- Environmental calculations supported by documented factors.
- Responsive UI.

---

## 5. Data Management

Supabase is the primary database.

The project will use existing datasets stored in Supabase.

Before implementing queries:
1. Inspect existing tables.
2. Understand the columns.
3. Identify data types.
4. Identify relationships.
5. Understand timestamps and units.
6. Verify existing RLS policies.

Do not create unnecessary duplicate datasets.

---

## 6. UI/UX Requirements

Create a modern, attractive electricity analytics dashboard.

Design direction:
- Clean and professional.
- Modern dashboard layout.
- Green and teal accent colours.
- Clear typography.
- Beautiful metric cards.
- Smooth navigation.
- Responsive design.

Use internet-sourced images only where they improve the visual experience.

Prioritise data readability over decorative elements.

---

## 7. Logging

Create a logging mechanism that records:

- Application events.
- Login success/failure events.
- API errors.
- Dataset loading errors.
- Important application operations.

Never log passwords, authentication tokens or secrets.

Keep local logs out of Git.

---

## 8. Definition of Done

A feature is complete only when:

- Implemented.
- Connected to the correct data source.
- Tested.
- Responsive.
- Functionally verified.
- Documented.

User approval is mandatory before moving to the next development phase.