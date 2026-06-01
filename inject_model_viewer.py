import os
import re
import base64

BASE = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts"
MONO = "/Users/rapid-002/Famtech Agricore /Famtech Software/Software/hardware-concepts"

MODELS = [
    ('01','01_spray_x.html', 'spray_x.glb'),
    ('02','02_scout.html', 'scout.glb'),
    ('03','03_nest.html', 'nest.glb'),
    ('04','04_watchtower.html', 'watchtower.glb'),
    ('05','05_soilnode.html', 'soilnode.glb'),
    ('06','06_feedpro.html', 'feedpro.glb'),
    ('07','07_herdtag.html', 'herdtag.glb'),
    ('08','08_aquasense.html', 'aquasense.glb'),
    ('09','09_fencegrid.html', 'fencegrid.glb'),
    ('10','10_hub.html', 'hub.glb'),
    ('11','11_crewlink.html', 'crewlink.glb'),
    ('12','12_agrimule.html', 'agrimule.glb'),
    ('13','13_rowplanter.html', 'rowplanter.glb'),
    ('14','14_terraplanter.html', 'terraplanter.glb'),
    ('15','15_microweeder.html', 'microweeder.glb'),
    ('16','16_brushcrusher.html', 'brushcrusher.glb'),
    ('17','17_omniharvester.html', 'omniharvester.glb')
]

def build_3d_views(glb_filename):
    glb_path = os.path.join(BASE, "models", glb_filename)
    if not os.path.exists(glb_path):
        return ""
    
    with open(glb_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode('utf-8')
    
    data_uri = f"data:model/gltf-binary;base64,{b64_data}"
    
    return f'''  <section class="views-section" style="margin: 40px 0;">
    <h2 style="text-align:center; margin-bottom:10px;">High-Fidelity 3D Photorealistic Renders</h2>
    <p style="color: var(--text-muted); text-align:center; margin-bottom: 30px;">True Physically-Based Rendering (PBR) exactly matching the 360 viewer</p>
    
    <!-- Model Viewer Script -->
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Isometric View</div>
        <model-viewer src="{data_uri}" camera-orbit="-45deg 55deg 100%" auto-rotate interaction-prompt="none" style="width: 100%; aspect-ratio: 4/3; background-color: #060c1b;" exposure="1.2" shadow-intensity="1.5" shadow-softness="1"></model-viewer>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Front View</div>
        <model-viewer src="{data_uri}" camera-orbit="0deg 90deg 100%" interaction-prompt="none" style="width: 100%; aspect-ratio: 4/3; background-color: #060c1b;" exposure="1.2" shadow-intensity="1.5" shadow-softness="1"></model-viewer>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Side View</div>
        <model-viewer src="{data_uri}" camera-orbit="90deg 90deg 100%" interaction-prompt="none" style="width: 100%; aspect-ratio: 4/3; background-color: #060c1b;" exposure="1.2" shadow-intensity="1.5" shadow-softness="1"></model-viewer>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Top View</div>
        <model-viewer src="{data_uri}" camera-orbit="0deg 0deg 100%" interaction-prompt="none" style="width: 100%; aspect-ratio: 4/3; background-color: #060c1b;" exposure="1.2" shadow-intensity="1.5" shadow-softness="1"></model-viewer>
      </div>
    </div>
  </section>'''

for _, filename, glb in MODELS:
    path1 = os.path.join(BASE, filename)
    path2 = os.path.join(MONO, filename)
    
    if not os.path.exists(path1): continue
        
    with open(path1, encoding='utf-8') as f:
        html = f.read()
        
    new_section = build_3d_views(glb)
    if not new_section: continue
    
    # Replace the existing views-section
    html = re.sub(r'<section class="views-section".*?</section>', new_section, html, flags=re.DOTALL)
    
    for p in [path1, path2]:
        if os.path.exists(p):
            with open(p, 'w', encoding='utf-8') as f:
                f.write(html)
                
    print(f"Updated {filename} with base64 embedded WebGL viewers!")
