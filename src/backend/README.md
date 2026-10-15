# Backend Architecture & Service Modules (`src/backend`)

The backend layer implements the business logic, policy evaluation, risk scoring, data normalization, and persistence mechanisms of SovereigntyAI.

## Core Modules
- **`app.py`:** Flask web application entry point hosting HTML template routes and REST APIs.
- **`config.py`:** Centralized settings, AWS region metadata, ISO jurisdiction mappings, and risk scoring parameters.
- **`policy_engine.py`:** Evaluates cloud storage configurations against structured condition trees in `policies/policy_rules.json`.
- **`risk_assessment.py`:** Computes deterministic 0–100 risk scores, provides itemized factor waterfalls, and generates recommendations.
- **`database.py`:** SQLite relational storage for assessments and audit trails, with CSV/JSON export utilities.
- **`utils.py`:** Input sanitization, boolean parsing, and ID generation.
- **`ai_services.py`:** Advisory machine learning prediction wrapper with graceful fallback.

For full architectural details, consult `architecture/System_Architecture.md`.
