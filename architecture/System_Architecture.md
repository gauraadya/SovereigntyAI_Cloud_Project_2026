# System Architecture & Component Design

## 1. Architectural Philosophy

SovereigntyAI is built on three core software engineering principles:
1. **Decoupled Modularity:** The policy evaluation engine, explainable risk scoring algorithm, database persistence, and user interfaces are isolated into separate modules with minimal inter-dependencies.
2. **Determinism over Stochasticity:** Compliance decisions are driven strictly by deterministic statutory condition trees rather than probabilistic generative AI, preventing hallucinations and ensuring legal repeatability.
3. **Defense-in-Depth Observability:** Every evaluation produces an itemized mathematical audit trail, an advisory ML comparison, and an immutable log entry.

---

## 2. Multi-Layer System Architecture Diagram

```mermaid
graph TD
    subgraph UI ["Layer 1: Presentation Layer"]
        DashboardView["Dashboard View (index.html)"]
        AssessmentForm["Assessment Form (assessment.html)"]
        PolicyExplorer["Policy Explorer (policies.html)"]
        AuditHistory["Audit History (history.html)"]
        DetailView["Detail View (detail.html)"]
        CSSJS["Vanilla JS Controller (app.js) & CSS (style.css)"]
    end

    subgraph API ["Layer 2: Application Controller (Flask WSGI)"]
        AppRoutes["app.py (Web & REST Endpoints)"]
        SecurityMW["Security Headers & Sanitization (utils.py)"]
    end

    subgraph CoreEngine ["Layer 3: Core Compliance Intelligence"]
        PolicyEngineModule["Policy Intelligence Engine (policy_engine.py)"]
        RiskEngineModule["Explainable Risk Assessment Engine (risk_assessment.py)"]
        RulesJSON[("Configurable Policy Rules (policy_rules.json)")]
    end

    subgraph MLEngine ["Layer 4: Advisory Machine Learning (scikit-learn)"]
        AIServices["AI Services Adapter (ai_services.py)"]
        JoblibModel["RandomForestClassifier Pipeline (sovereignty_risk_model.joblib)"]
    end

    subgraph Persistence ["Layer 5: Local & Cloud Persistence"]
        DBLayer["Database Manager (database.py)"]
        SQLiteDB[("SQLite Datastore (sovereignty_ai.db)")]
        AWSAdapters["AWS Cloud Adapters (src/aws/)"]
        S3Mock[("Mock S3 Report Storage (data/s3_mock/)")]
    end

    CSSJS --> AppRoutes
    AppRoutes --> SecurityMW
    SecurityMW --> PolicyEngineModule
    SecurityMW --> RiskEngineModule
    PolicyEngineModule --> RulesJSON
    PolicyEngineModule --> RiskEngineModule
    AppRoutes --> AIServices
    AIServices --> JoblibModel
    RiskEngineModule --> DBLayer
    AppRoutes --> DBLayer
    DBLayer --> SQLiteDB
    AppRoutes --> AWSAdapters
    AWSAdapters --> S3Mock
```

---

## 3. End-to-End Evaluation Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Cloud Engineer / Auditor
    participant Web as Web Browser / API Client
    participant App as Flask Controller (app.py)
    participant Util as Validator (utils.py)
    participant PE as Policy Engine (policy_engine.py)
    participant RE as Risk Engine (risk_assessment.py)
    participant ML as ML Service (ai_services.py)
    participant DB as SQLite Datastore (database.py)
    participant AWS as AWS Adapters (src/aws/)

    User->>Web: Fill Deployment Form or Select Sample Scenario
    Web->>App: POST /assessment (or POST /api/assessments)
    App->>Util: normalize_payload(form_data)
    Util-->>App: (is_valid: true, clean_payload)

    App->>PE: evaluate(clean_payload)
    Note over PE: Matches jurisdiction, data category,<br/>and AWS regions against JSON rules
    PE-->>App: policy_results (PASS, FAIL, REVIEW)

    App->>RE: calculate_risk(clean_payload, policy_results)
    Note over RE: Computes baseline sensitivity + penalties - mitigations.<br/>Generates XAI narrative & recommendations.
    RE-->>App: risk_result (Score 0-100, Status, Factors, Next Steps)

    App->>ML: predict_compliance_ml(clean_payload)
    ML-->>App: ml_prediction (Predicted Status, Confidence, Probabilities)

    App->>DB: save_assessment(assessment_record)
    DB-->>App: assessment_id (SOV-YYYYMMDD-XXXX)

    App->>AWS: archive_report(assessment_id, report)
    App->>AWS: log_assessment_metric(status, score)

    App-->>Web: Render Results View with Score Dial, Checks, & Factors
    Web-->>User: Display Compliance Status, Recommendations & Audit Report
```

---

## 4. Component Directory & File Responsibility Mapping

- `app.py`: Central routing, error handling, session management, and HTTP API delivery.
- `config.py`: Environment flags, AWS region definitions, jurisdiction dictionaries, sensitivity weights.
- `policy_engine.py`: Dynamic JSON rule parser and condition matcher evaluating statutory transfer requirements.
- `risk_assessment.py`: Deterministic score calculator (0-100), factor waterfall generator, recommendation builder.
- `ai_services.py`: Advisory inference wrapper loading the trained scikit-learn pipeline with fallback handling.
- `database.py`: SQLite connection pool, schema initialization, audit trail logger, CSV/JSON exporters.
- `utils.py`: Payload normalization, input sanitization, unique ID generation.
- `src/aws/`: Modular adapters for Amazon S3, SNS, and CloudWatch.
