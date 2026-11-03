# OHMies — Development Phases and Execution Instructions

## 1. Development Philosophy

OHMies must be developed incrementally.

The project has three main development phases.

**STRICT DEVELOPMENT ORDER**

1. Tab 1 — Overview
2. Tab 2 — Analytics
3. Tab 3 — Savings / Green Pass Road

The coding agent must not skip phases or begin implementing the next tab before the current tab has been completed and approved.

The objective is to achieve quality through iterative implementation, testing, and refinement.

---

## 2. PHASE 0 — Initial Project Inspection

Before writing code:

1. Inspect the existing repository.
2. Understand the current folder structure.
3. Identify existing React and FastAPI files.
4. Inspect installed dependencies.
5. Locate the Supabase datasets.
6. Inspect the actual Supabase database schema where access is available.
7. Locate the existing sample dashboard HTML.
8. Inspect its design and functionality.
9. Identify reusable components.
10. Identify files that should not be modified.

Do not start rewriting existing files without understanding their purpose.

### Deliverable

Provide a short inspection report containing:

- Existing project structure.
- Existing technologies.
- Dataset information.
- Existing reusable components.
- Required changes.
- Missing dependencies or resources.

Proceed to Phase 1.

---

# PHASE 1 — TAB 1: OVERVIEW

<status>FIRST PRIORITY</status>

## Objective

Build a fully functional dashboard overview page.

### Step 1: Authentication

- Implement the login page.
- Connect authentication.
- Verify credentials.
- Protect frontend routes.
- Protect backend endpoints.
- Display the specified invalid login message in dark red.

### Step 2: Dashboard Layout

Implement:

**Header**
- Welcome User on the left.
- Goal on the extreme right.

**Four Metric Cards**
1. Average Daily Draw.
2. Peak Window Intensity.
3. Grid Carbon Footprint.
4. Tariff Bracket.

### Step 3: Usage Summary

Implement a meaningful statistical summary.

The summary must explain:

- Current electricity consumption.
- Daily average.
- Peak consumption period.
- Relevant comparisons.
- Recommended actions.

### Step 4: Supabase Integration

- Inspect actual tables.
- Connect backend to Supabase.
- Retrieve the required records.
- Process data.
- Calculate metrics.
- Display the results.

### Step 5: UI/UX

- Implement responsive styling.
- Improve typography.
- Design metric cards.
- Add suitable icons and visual elements.
- Maintain consistency across the dashboard.

### Step 6: Testing

Test:

- Login.
- Invalid credentials.
- Protected routes.
- API connectivity.
- Database connectivity.
- Statistical calculations.
- Empty datasets.
- Loading states.
- Error states.
- Responsive layouts.

### PHASE 1 COMPLETION CHECKLIST

- [ ] Login works.
- [ ] Invalid login is rejected.
- [ ] Dashboard is protected.
- [ ] Welcome User header works.
- [ ] Goal section works.
- [ ] Average Daily Draw works.
- [ ] Peak Window Intensity works.
- [ ] Grid Carbon Footprint works.
- [ ] Tariff Bracket works.
- [ ] Usage summary works.
- [ ] Supabase data is integrated.
- [ ] UI is responsive.
- [ ] Tests pass.

### STOP CONDITION

Once all requirements are satisfied:

1. Present the completed Tab 1.
2. Show screenshots or a working demonstration.
3. Explain the implemented features.
4. Present testing results.
5. List any known limitations.
6. Ask the user for approval.

**DO NOT START PHASE 2 WITHOUT EXPLICIT APPROVAL.**

---

# PHASE 2 — TAB 2: ANALYTICS

<status>SECOND PRIORITY</status>

Begin only after Phase 1 has been approved.

## Objective

Create a dedicated electricity analytics page.

### Step 1: Graphs

Implement historical electricity consumption graphs.

Display:
- Consumption trends.
- Daily usage.
- Historical patterns.

### Step 2: Pie Charts

Implement pie charts showing consumption distribution.

Only use valid categories supported by the dataset.

### Step 3: Weekly Bar Graph

Display electricity consumption per week.

Requirements:
- Clearly labelled weeks.
- Correct aggregation.
- Correct units.
- Consistent date boundaries.

### Step 4: Smart Tips

Implement the predefined Smart Tips catalogue.

Tips must be relevant to:
- Domestic users.
- MICRO businesses.
- SMALL businesses.
- MEDIUM businesses.

Use the user's subcategory to select appropriate tips.

Where possible, connect tips to observed consumption patterns.

### Step 5: UI/UX

- Clean analytics layout.
- Interactive charts.
- Appropriate spacing.
- Readable legends.
- Responsive design.

### PHASE 2 COMPLETION CHECKLIST

- [ ] Historical graphs work.
- [ ] Pie charts work where supported.
- [ ] Weekly bar graph works.
- [ ] Data aggregation is correct.
- [ ] Smart Tips are displayed.
- [ ] Tips match the user's sector.
- [ ] Date filtering works where supported.
- [ ] Responsive layout works.
- [ ] Tests pass.

### STOP CONDITION

Present the completed analytics page and testing results.

Ask the user for explicit approval.

**DO NOT START PHASE 3 WITHOUT APPROVAL.**

---

# PHASE 3 — TAB 3: SAVINGS / GREEN PASS ROAD

<status>THIRD PRIORITY</status>

Begin only after Phase 2 has been approved.

## Objective

Develop the electricity savings page using the existing Green Pass Road HTML as a reference.

### Step 1: Reference Inspection

Inspect the entire Green Pass Road section.

Understand:
- Existing layout.
- Design structure.
- Calculation logic.
- User interactions.
- Visual hierarchy.
- Relevant components.

Do not recreate the same HTML file.

Extract and adapt the relevant structure into the existing React application.

If the reference file has not been provided, stop and request it.

### Step 2: Savings Calculations

Implement calculations showing:

- Current electricity consumption.
- Current estimated electricity cost.
- Potential consumption reduction.
- Estimated money saved.
- Environmental benefits where supported.

### Step 3: Financial Insights

Explain how the user can save money through electricity conservation.

Display the assumptions behind each calculation.

Clearly distinguish:
- Actual savings.
- Projected savings.
- Estimated savings.

### Step 4: UI/UX

Adapt the Green Pass Road visual language into the OHMies design system.

Ensure:
- Consistent styling.
- Smooth interactions.
- Clear financial information.
- Responsive layout.

### PHASE 3 COMPLETION CHECKLIST

- [ ] Green Pass Road reference inspected.
- [ ] Relevant structure adapted.
- [ ] Savings calculations implemented.
- [ ] Financial assumptions displayed.
- [ ] Environmental calculations supported.
- [ ] Responsive UI.
- [ ] Tests pass.

### STOP CONDITION

Present the completed page, calculations, reference adaptation and test results.

Ask for final approval.

---

# 3. ITERATIVE DEVELOPMENT LOOP

The development process must follow an iterative improvement cycle.

```text
          INSPECT
             |
             v
       UNDERSTAND TASK
             |
             v
       IMPLEMENT CODE
             |
             v
        RUN TESTS
             |
             v
      EVALUATE OUTPUT
             |
       +-----+-----+
       |           |
       v           v
     PASS         FAIL
       |           |
       v           v
     REVIEW     FIND ROOT CAUSE
       |           |
       |           v
       |        FIX CODE
       |           |
       |           v
       |        RETEST
       |           |
       +-----------+
             |
             v
      ACCEPTANCE REVIEW
             |
             v
       PHASE COMPLETION
```

## Loop Instructions

Repeat the implementation and testing cycle until the active phase satisfies its acceptance criteria.

During each iteration:

1. Identify what is incomplete.
2. Identify the actual problem.
3. Implement a targeted improvement.
4. Run relevant tests.
5. Compare the result against requirements.
6. Record the outcome.
7. Continue if a measurable issue remains.

Do not repeatedly rewrite working components.

Do not make random UI changes simply to find a better design.

Do not claim that the best implementation has been found without validating it against requirements.

If blocked by missing datasets, credentials, reference files, or unclear requirements, stop and ask the user.

---

# 4. GLOBAL DEVELOPMENT RULES

These instructions apply throughout the entire project.

### Rule 1 — Phase Restrictions

Never jump between phases.

Complete Tab 1 before Tab 2 and Tab 2 before Tab 3.

### Rule 2 — Existing HTML Reference

The existing HTML file is a reference.

Do not simply rebuild the same HTML file.

Extract useful design, logic and structure and integrate them into React.

### Rule 3 — Dataset Integrity

Use the actual Supabase datasets.

Never fabricate real-looking consumption statistics.

### Rule 4 — Authentication

Never expose protected pages or data to unauthenticated users.

### Rule 5 — Security

Never commit passwords, private keys, tokens or sensitive configuration.

### Rule 6 — Code Quality

Keep components reusable.

Avoid unnecessarily large files.

Separate frontend, backend, database and calculation logic.

### Rule 7 — Testing

Every major feature must be tested before it is declared complete.

### Rule 8 — User Approval

The user must approve each completed phase before the next phase begins.

---

# 5. FINAL INSTRUCTION TO ANTIGRAVITY

You are developing OHMies as a complete electricity analytics and conservation platform.

Do not attempt to build the entire application in one execution.

Start with repository inspection and then implement Tab 1 only.

Prioritise correctness, data integrity, security, UI/UX and maintainability.

Use the provided documentation as the project's development specification.

**CURRENT EXECUTION TARGET: PHASE 1 — TAB 1 OVERVIEW.**

Do not begin Tab 2 or Tab 3 until the user explicitly approves the preceding phase.