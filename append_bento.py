import os

css_path = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts/styles.css"
css_path2 = "/Users/rapid-002/Famtech Agricore /Famtech Software/Software/hardware-concepts/styles.css"

bento_css = """
/* ── PREMIUM BENTO BOX LAYOUT UPGRADE ───────────────────────── */
/* Transform disjointed sections into cohesive structural cards */

section:not(.views-section):not(.illus-section) {
  background: linear-gradient(180deg, var(--surface-2) 0%, var(--surface) 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  display: flex;
  flex-direction: column;
  transition: border-color var(--t), transform var(--t), box-shadow var(--t);
  position: relative;
  overflow: hidden;
  margin-bottom: 0;
}

section:not(.views-section):not(.illus-section):hover {
  border-color: rgba(59,130,246,0.3);
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(59,130,246,0.1);
}

section:not(.views-section):not(.illus-section)::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(59,130,246,0.5), transparent);
  opacity: 0;
  transition: opacity var(--t);
}

section:not(.views-section):not(.illus-section):hover::before {
  opacity: 1;
}

/* Convert floating h2 into integrated, sleek headers */
section:not(.views-section):not(.illus-section) h2 {
  font-family: var(--display);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  padding: 1.1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* The .section-num pill inside the integrated header */
section:not(.views-section):not(.illus-section) .section-num {
  background: transparent;
  color: var(--text-3);
  border-color: var(--text-4);
}
section:not(.views-section):not(.illus-section):hover .section-num {
  color: var(--blue);
  border-color: var(--blue);
}

/* Nullify the old .panel background since the section is now the card */
section:not(.views-section):not(.illus-section) .panel {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  padding: 0 !important;
  border-radius: 0 !important;
}
section:not(.views-section):not(.illus-section) .panel::before {
  display: none;
}

/* Refine typography inside the panels */
section:not(.views-section):not(.illus-section) .panel p {
  color: var(--text-2);
  font-size: 0.95rem;
  line-height: 1.8;
  padding-left: 1rem;
  border-left: 2px solid var(--border);
}

/* Upgrade Spec Table */
.spec-table {
  margin: -0.5rem 0;
}
.spec-table th {
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.72rem;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.spec-table td {
  color: var(--text);
  font-size: 0.88rem;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
}
.spec-table tr:hover th, .spec-table tr:hover td {
  background: rgba(255,255,255,0.01);
}

/* Upgrade Brief Grid (The 2x2 or 3x2 info boxes) */
.brief-grid {
  background: rgba(0,0,0,0.25);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.05);
  overflow: hidden;
  margin: -0.5rem 0;
}
.brief-row {
  padding: 1rem 1.25rem !important;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  border-left: none !important;
  transition: background var(--t);
}
.brief-row:hover { background: rgba(255,255,255,0.02); }
.brief-row:nth-child(even) { border-left: 1px solid rgba(255,255,255,0.05) !important; }
.brief-label {
  color: var(--text-3);
  font-size: 0.68rem;
  margin-bottom: 0.25rem;
}
.brief-value {
  font-size: 0.95rem;
  color: var(--text);
}

/* Upgrade Component Chips */
.comp-grid {
  gap: 0.75rem;
}
.comp-chip {
  background: rgba(0,0,0,0.4);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 6px;
  color: var(--text-2);
  font-size: 0.82rem;
  padding: 0.5rem 0.85rem;
  letter-spacing: 0.02em;
}
.comp-chip::before { background: var(--blue); }
.comp-chip:hover {
  background: rgba(59,130,246,0.1);
  border-color: rgba(59,130,246,0.3);
  color: var(--blue);
}

/* Upgrade Fusion List */
.fusion-list li {
  background: rgba(0,0,0,0.2);
  border: 1px solid transparent;
  border-left: 2px solid rgba(255,255,255,0.08);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 0.75rem 1rem;
}
.fusion-list li::before {
  background: transparent;
  color: var(--text-3);
  border: 1px solid var(--text-4);
}
.fusion-list li:hover {
  border-left-color: var(--blue);
  background: rgba(59,130,246,0.04);
}
.fusion-list li:hover::before {
  color: var(--blue);
  border-color: var(--blue);
}

/* Risk Panel specific overrides */
.risk-panel {
  border: none;
  background: transparent;
  padding: 0;
}
.risk-panel h2 {
  background: rgba(239,68,68,0.1) !important;
  color: #fca5a5 !important;
  border-bottom: 1px solid rgba(239,68,68,0.2) !important;
}
.risk-panel .section-num {
  border-color: rgba(239,68,68,0.4) !important;
}

/* Adjust the main grid spacing to match the new Bento cards */
.grid { gap: 1.5rem; }
"""

for path in [css_path, css_path2]:
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        if "PREMIUM BENTO BOX LAYOUT UPGRADE" not in content:
            with open(path, "a") as f:
                f.write("\n" + bento_css)
            print(f"Appended Bento CSS to {path}")
        else:
            print(f"Bento CSS already in {path}")
