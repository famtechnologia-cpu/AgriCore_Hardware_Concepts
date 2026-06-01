import os
import re

css_path = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts/styles.css"
css_path2 = "/Users/rapid-002/Famtech Agricore /Famtech Software/Software/hardware-concepts/styles.css"

new_css = """
/* ── ULTRA-PREMIUM INDUSTRIAL DESIGN UPGRADE ────────────────── */
/* Clean, minimal, airy, high-tech */

section:not(.views-section):not(.illus-section) {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
  transition: background 0.3s ease, border-color 0.3s ease;
}
section:not(.views-section):not(.illus-section):hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
}
section:not(.views-section):not(.illus-section)::before { display: none; }

/* Elegant Headers */
section:not(.views-section):not(.illus-section) h2 {
  font-family: var(--sans);
  font-size: 0.85rem;
  font-weight: 500;
  color: #fff;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin: -2rem -2rem 1.5rem -2rem;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: transparent;
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Minimal ring for section numbers */
section:not(.views-section):not(.illus-section) .section-num {
  background: transparent;
  color: var(--text-3);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  width: 26px;
  height: 26px;
  font-size: 0.65rem;
  font-family: var(--mono);
  font-weight: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}
section:not(.views-section):not(.illus-section):hover .section-num {
  color: #fff;
  border-color: rgba(255, 255, 255, 0.4);
}

/* Nullify .panel entirely */
section:not(.views-section):not(.illus-section) .panel {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  padding: 0 !important;
  border-radius: 0 !important;
}

/* Beautiful Typography for paragraphs */
section:not(.views-section):not(.illus-section) .panel p {
  color: var(--text-2);
  font-size: 0.95rem;
  line-height: 1.7;
  padding: 0;
  border: none;
  font-weight: 300;
}

/* Elegant Brief Grid (Industrial Spec Sheet) */
.brief-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  margin: 0;
}
.brief-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: baseline;
  padding: 0.85rem 0 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  border-left: none !important;
  background: transparent !important;
}
.brief-row:hover { background: transparent !important; }
.brief-row:last-child { border-bottom: none; }
.brief-row:nth-child(even) { border-left: none !important; padding-left: 0 !important; }
.brief-row:nth-child(odd) { padding-right: 0 !important; }
.brief-label {
  color: var(--text-3);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  font-weight: 400;
  text-transform: none;
}
.brief-value {
  color: #fff;
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 400;
}

/* Beautiful Spec Table */
.spec-table { margin: 0; width: 100%; }
.spec-table th {
  color: var(--text-3);
  font-weight: 400;
  font-size: 0.8rem;
  text-transform: none;
  letter-spacing: normal;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.spec-table td {
  color: #fff;
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 400;
  text-align: right;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.spec-table tr:hover th, .spec-table tr:hover td { background: transparent; }
.spec-table tr:last-child th, .spec-table tr:last-child td { border-bottom: none; }

/* Minimal Component Chips */
.comp-grid { gap: 0.6rem; }
.comp-chip {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 99px; /* Pill shape */
  color: var(--text-2);
  font-family: var(--mono);
  font-size: 0.75rem;
  padding: 0.45rem 0.9rem;
  transition: all 0.2s ease;
  letter-spacing: normal;
}
.comp-chip::before { display: none; }
.comp-chip:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

/* Sleek Fusion List */
.fusion-list li {
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0;
  padding: 0.85rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--text-2);
}
.fusion-list li:last-child { border-bottom: none; }
.fusion-list li::before {
  border: none;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-3);
  font-weight: 400;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 0.65rem;
}
.fusion-list li:hover {
  background: transparent;
  color: #fff;
  transform: translateX(4px);
}
.fusion-list li:hover::before { 
  color: #fff; 
  background: rgba(255, 255, 255, 0.15); 
  border-color: transparent; 
}

/* Risk Panel */
.risk-panel { border: none; background: transparent; padding: 0; }
.risk-panel h2 { background: transparent !important; border-bottom: 1px solid rgba(239, 68, 68, 0.2) !important; color: #f87171 !important; }
.risk-panel .section-num { border-color: rgba(239, 68, 68, 0.4) !important; color: #f87171 !important; }
.risk-list li { border-bottom-color: rgba(239, 68, 68, 0.15); }

/* Main Grid Spacing */
.grid { gap: 1.5rem; }
"""

for path in [css_path, css_path2]:
    if not os.path.exists(path):
        continue
    
    with open(path, "r") as f:
        content = f.read()
    
    if "/* ── PREMIUM BENTO BOX LAYOUT UPGRADE" in content:
        # Replace the old appended block
        content = re.sub(r'/\* ── PREMIUM BENTO BOX LAYOUT UPGRADE.*', new_css, content, flags=re.DOTALL)
    elif "/* ── ULTRA-PREMIUM INDUSTRIAL DESIGN UPGRADE" in content:
        content = re.sub(r'/\* ── ULTRA-PREMIUM INDUSTRIAL DESIGN UPGRADE.*', new_css, content, flags=re.DOTALL)
    else:
        content += "\n" + new_css
        
    with open(path, "w") as f:
        f.write(content)
    
    print(f"Updated {path}")
