# Frontend Presentation Layer (`src/frontend`)

The frontend layer delivers a responsive, accessible user experience implemented in standard HTML5, CSS3, and vanilla JavaScript without external UI frameworks or third-party CDN dependencies.

## Structure
- **Templates (`templates/`):**
  - `base.html`: Common layout, brand navigation, and message flashes.
  - `index.html`: Executive dashboard with fleet metrics, risk distribution bar, and recent audit logs.
  - `assessment.html`: 12-parameter evaluation form, one-click scenario loaders, and full XAI results display.
  - `policies.html`: Interactive policy explorer with live text search and dropdown filters.
  - `history.html`: Searchable assessment history table with CSV/JSON export actions.
  - `detail.html`: Immutable audit record view for single assessments.
  - `scenarios.html`: Showcase of the six demonstration scenarios with one-click test buttons.
  - `about.html`: Academic context, viva voce cheat-sheet, and legal disclaimers.
- **Static Assets (`static/`):**
  - `css/style.css`: Modern responsive stylesheet with CSS custom properties, responsive cards, and dials.
  - `js/app.js`: Client-side scenario loading, live policy filtering, and validation.
