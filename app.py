"""
Main Application Entry Point for SovereigntyAI.
Flask web server delivering the dashboard, assessment engine, policy explorer,
history logs, export capabilities, and REST APIs.
"""

import os
import json
from pathlib import Path
from flask import (
    Flask, render_template, request, jsonify, redirect,
    url_for, flash, Response
)

import config
import database
from policy_engine import PolicyEngine
from risk_assessment import RiskAssessmentEngine
import ai_services
import utils
from src.aws.aws_services import S3ReportStorage, SNSComplianceNotifier, CloudWatchMetricsLogger

# Instantiate Flask application
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Initialize components
engine = PolicyEngine()
s3_storage = S3ReportStorage()
sns_notifier = SNSComplianceNotifier()
cw_logger = CloudWatchMetricsLogger()

# Ensure database is initialized on launch
with app.app_context():
    database.init_db()

def _load_sample_scenarios():
    """Load sample scenarios from dataset/sample_scenarios.json."""
    if not config.SCENARIOS_PATH.exists():
        return []
    try:
        with open(config.SCENARIOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[App] Error loading sample scenarios: {e}")
        return []

# ==========================================
# Web UI Routes
# ==========================================

@app.route("/")
def dashboard():
    """Render dashboard with aggregate statistics and recent logs."""
    stats = database.get_dashboard_stats()
    return render_template("index.html", stats=stats)

@app.route("/assessment", methods=["GET", "POST"])
def new_assessment():
    """Render new assessment form (GET) or process compliance evaluation (POST)."""
    sample_scenarios = _load_sample_scenarios()
    
    if request.method == "POST":
        # Process submitted form data
        is_valid, error_msg, payload = utils.normalize_payload(request.form)
        if not is_valid:
            flash(error_msg, "danger")
            return render_template(
                "assessment.html",
                jurisdictions=config.JURISDICTIONS,
                aws_regions=config.AWS_REGIONS,
                data_categories=config.DATA_CATEGORIES,
                transfer_mechanisms=config.TRANSFER_MECHANISMS,
                sample_scenarios=sample_scenarios,
                form_data=request.form,
                result=None
            )

        # 1. Deterministic Policy Rule Evaluation
        policy_results = engine.evaluate(payload)

        # 2. Explainable Risk Score Calculation
        risk_result = RiskAssessmentEngine.calculate_risk(payload, policy_results)

        # 3. Advisory ML Inference (scikit-learn baseline)
        ml_prediction = ai_services.predict_compliance_ml(payload)

        # Combine results into complete assessment record
        assessment_record = {
            **payload,
            **risk_result,
            "policy_results": policy_results,
            "ml_prediction": ml_prediction
        }

        # 4. Persist to SQLite Database
        assessment_id = database.save_assessment(assessment_record)

        # 5. Archive Report & Emit Metrics via AWS Adapters
        s3_storage.archive_report(assessment_id, assessment_record)
        cw_logger.log_assessment_metric(
            assessment_record["compliance_status"],
            assessment_record["risk_score"],
            assessment_record["origin_jurisdiction"]
        )

        if assessment_record["compliance_status"] == config.STATUS_NON_COMPLIANT:
            sns_notifier.publish_alert(
                assessment_id,
                assessment_record["compliance_status"],
                assessment_record["risk_score"],
                "Critical compliance breach detected during assessment."
            )

        flash(f"Assessment {assessment_id} evaluated successfully.", "success")
        return render_template(
            "assessment.html",
            jurisdictions=config.JURISDICTIONS,
            aws_regions=config.AWS_REGIONS,
            data_categories=config.DATA_CATEGORIES,
            transfer_mechanisms=config.TRANSFER_MECHANISMS,
            sample_scenarios=sample_scenarios,
            form_data=payload,
            result=assessment_record
        )

    # GET request
    return render_template(
        "assessment.html",
        jurisdictions=config.JURISDICTIONS,
        aws_regions=config.AWS_REGIONS,
        data_categories=config.DATA_CATEGORIES,
        transfer_mechanisms=config.TRANSFER_MECHANISMS,
        sample_scenarios=sample_scenarios,
        form_data=None,
        result=None
    )

@app.route("/policies")
def policy_explorer():
    """Display all configured policy rules with filters and legal citations."""
    rules = engine.get_all_rules()
    return render_template("policies.html", rules=rules, metadata=engine.metadata)

@app.route("/history")
def assessment_history():
    """Display searchable, filterable history of past compliance evaluations."""
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    jurisdiction = request.args.get("jurisdiction", "").strip()

    assessments = database.get_assessments(
        limit=100,
        filter_status=status if status else None,
        filter_jurisdiction=jurisdiction if jurisdiction else None,
        search_term=search if search else None
    )

    return render_template(
        "history.html",
        assessments=assessments,
        jurisdictions=config.JURISDICTIONS,
        current_search=search,
        current_status=status,
        current_jurisdiction=jurisdiction
    )

@app.route("/history/<assessment_id>")
def assessment_detail(assessment_id):
    """Display full audit detail of a single assessment."""
    assessment = database.get_assessment(assessment_id)
    if not assessment:
        flash(f"Assessment {assessment_id} not found.", "warning")
        return redirect(url_for("assessment_history"))

    return render_template("detail.html", assessment=assessment)

@app.route("/scenarios")
def sample_scenarios_page():
    """Showcase pre-configured sample scenarios."""
    scenarios = _load_sample_scenarios()
    return render_template("scenarios.html", scenarios=scenarios)

@app.route("/about")
def about_page():
    """About page with viva voce prep notes, academic objectives, and legal disclaimers."""
    return render_template("about.html")

# ==========================================
# REST API & Export Endpoints
# ==========================================

@app.route("/api/assessments", methods=["POST"])
def api_create_assessment():
    """REST API to evaluate and record a compliance assessment programmatically."""
    raw_data = request.get_json(force=True, silent=True) or {}
    is_valid, error_msg, payload = utils.normalize_payload(raw_data)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    policy_results = engine.evaluate(payload)
    risk_result = RiskAssessmentEngine.calculate_risk(payload, policy_results)
    ml_prediction = ai_services.predict_compliance_ml(payload)

    assessment_record = {
        **payload,
        **risk_result,
        "policy_results": policy_results,
        "ml_prediction": ml_prediction
    }

    assessment_id = database.save_assessment(assessment_record)
    s3_storage.archive_report(assessment_id, assessment_record)

    return jsonify({"assessment_id": assessment_id, "data": assessment_record}), 201

@app.route("/api/assessments/<assessment_id>")
def api_get_assessment(assessment_id):
    """REST API to fetch single assessment record by ID."""
    assessment = database.get_assessment(assessment_id)
    if not assessment:
        return jsonify({"error": "Assessment not found"}), 404
    return jsonify(assessment)

@app.route("/api/policies")
def api_list_policies():
    """REST API to list all policy rules."""
    return jsonify({
        "metadata": engine.metadata,
        "rules": engine.get_all_rules()
    })

@app.route("/api/scenarios")
def api_list_scenarios():
    """REST API to list sample scenarios."""
    return jsonify(_load_sample_scenarios())

@app.route("/api/scenarios/<scenario_id>")
def api_get_scenario(scenario_id):
    """REST API to fetch a specific scenario by ID."""
    scenarios = _load_sample_scenarios()
    for sc in scenarios:
        if sc.get("scenario_id") == scenario_id:
            return jsonify(sc)
    return jsonify({"error": "Scenario not found"}), 404

@app.route("/export/csv")
def export_csv():
    """Download all assessment audit records as a CSV file."""
    csv_data = database.export_assessments_csv()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sovereignty_ai_audit_export.csv"}
    )

@app.route("/export/json")
def export_json():
    """Download or view all assessment audit records as JSON."""
    json_data = database.export_assessments_json()
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=sovereignty_ai_audit_export.json"}
    )

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html"), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"[*] Starting SovereigntyAI Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
