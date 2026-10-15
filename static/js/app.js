/**
 * SovereigntyAI Frontend Controller
 * Handles dynamic scenario loading, policy filtering, and interactive assessment workflows.
 */

document.addEventListener("DOMContentLoaded", () => {
  initScenarioLoader();
  initPolicyFilter();
  initAssessmentForm();
});

/**
 * Handles one-click loading of sample scenarios into the assessment form.
 */
function initScenarioLoader() {
  const pills = document.querySelectorAll(".scenario-pill");
  if (!pills.length) return;

  pills.forEach(pill => {
    pill.addEventListener("click", async () => {
      const scenarioId = pill.getAttribute("data-scenario-id");
      try {
        const response = await fetch(`/api/scenarios/${scenarioId}`);
        if (!response.ok) throw new Error("Failed to load scenario data");
        const data = await response.json();
        populateAssessmentForm(data);
      } catch (err) {
        console.error("Error loading scenario:", err);
      }
    });
  });

  // Check URL search params for ?scenario=SCENARIO-XX
  const urlParams = new URLSearchParams(window.location.search);
  const requestedScenario = urlParams.get("scenario");
  if (requestedScenario) {
    const targetPill = document.querySelector(`[data-scenario-id="${requestedScenario}"]`);
    if (targetPill) targetPill.click();
  }
}

/**
 * Populate form inputs with scenario parameters.
 */
function populateAssessmentForm(sc) {
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val !== undefined ? val : "";
  };

  const setCheck = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.checked = Boolean(val);
  };

  setVal("origin_jurisdiction", sc.origin_jurisdiction);
  setVal("source_org", sc.source_org);
  setVal("data_category", sc.data_category);
  setVal("storage_region", sc.storage_region);
  setVal("backup_region", sc.backup_region || "");
  setVal("cross_border", sc.cross_border ? "true" : "false");
  setVal("transfer_mechanism", sc.transfer_mechanism || "none_unverified");
  setVal("framework", sc.framework || "GDPR");
  setVal("notes", sc.notes || sc.description || "");

  setCheck("encryption_at_rest", sc.encryption_at_rest);
  setCheck("access_control", sc.access_control);
  setCheck("audit_logging", sc.audit_logging);

  // Notification badge
  const alertBox = document.getElementById("scenario-loaded-alert");
  if (alertBox) {
    alertBox.style.display = "block";
    alertBox.innerHTML = `<strong>Loaded Scenario:</strong> ${sc.title} &mdash; <em>${sc.expected_status || "Ready to evaluate"}</em>`;
  }

  // Scroll to form
  const formEl = document.getElementById("assessment-form");
  if (formEl) formEl.scrollIntoView({ behavior: "smooth" });
}

/**
 * Dynamic live search and filtering for Policy Explorer.
 */
function initPolicyFilter() {
  const searchInput = document.getElementById("policy-search");
  const jurisFilter = document.getElementById("filter-jurisdiction");
  const severityFilter = document.getElementById("filter-severity");
  const table = document.getElementById("policies-table");

  if (!table) return;

  const filterRows = () => {
    const query = (searchInput ? searchInput.value : "").toLowerCase();
    const juris = jurisFilter ? jurisFilter.value : "";
    const severity = severityFilter ? severityFilter.value : "";
    const rows = table.querySelectorAll("tbody tr");

    let visibleCount = 0;
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const rowJuris = row.getAttribute("data-jurisdiction") || "";
      const rowSev = row.getAttribute("data-severity") || "";

      const matchText = !query || text.includes(query);
      const matchJuris = !juris || rowJuris === juris;
      const matchSev = !severity || rowSev === severity;

      if (matchText && matchJuris && matchSev) {
        row.style.display = "";
        visibleCount++;
      } else {
        row.style.display = "none";
      }
    });

    const countEl = document.getElementById("filtered-count");
    if (countEl) countEl.textContent = `${visibleCount} rules visible`;
  };

  if (searchInput) searchInput.addEventListener("input", filterRows);
  if (jurisFilter) jurisFilter.addEventListener("change", filterRows);
  if (severityFilter) severityFilter.addEventListener("change", filterRows);
}

/**
 * Handle form submission validation and UI states.
 */
function initAssessmentForm() {
  const form = document.getElementById("assessment-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const origin = document.getElementById("origin_jurisdiction").value;
    const region = document.getElementById("storage_region").value;
    const category = document.getElementById("data_category").value;

    if (!origin || !region || !category) {
      e.preventDefault();
      alert("Please fill in the required origin jurisdiction, data category, and AWS storage region.");
      return;
    }

    const submitBtn = document.getElementById("submit-assessment-btn");
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Evaluating Policies...";
    }
  });
}
