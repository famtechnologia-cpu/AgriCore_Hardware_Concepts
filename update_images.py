import os
import glob
import shutil
import re

BRAIN_DIR = "/Users/rapid-002/.gemini/antigravity/brain/b0ef9b02-6a05-4d11-af5c-1fdc700dff4b"
CONCEPTS_DIR = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts"
MONO_DIR = "/Users/rapid-002/Famtech Agricore /Famtech Software/Software/hardware-concepts"

# Mapping from html file prefix to image name
IMAGE_MAP = {
    "01_spray_x": "spray_x_2d",
    "02_scout": "scout_drone_2d", # the name was scout_drone_2d
    "03_nest": "nest_2d",
    "04_watchtower": "watchtower_2d",
    "05_soilnode": "soilnode_2d",
    "06_feedpro": "feedpro_2d",
    "07_herdtag": "herdtag_2d",
    "08_aquasense": "aquasense_2d",
    "09_fencegrid": "fencegrid_2d",
    "10_hub": "hub_2d",
    "11_crewlink": "crewlink_2d",
    "12_agrimule": "agrimule_2d",
    "13_rowplanter": "rowplanter_2d",
    "14_terraplanter": "terraplanter_2d",
    "15_microweeder": "microweeder_2d",
    "16_brushcrusher": "brushcrusher_2d",
    "17_omniharvester": "omniharvester_2d"
}

def setup_dirs(base_dir):
    img_dir = os.path.join(base_dir, "assets", "images")
    os.makedirs(img_dir, exist_ok=True)
    return img_dir

concepts_img_dir = setup_dirs(CONCEPTS_DIR)
mono_img_dir = setup_dirs(MONO_DIR)

# Find all PNGs
png_files = glob.glob(os.path.join(BRAIN_DIR, "*_2d_*.png"))

for key, img_prefix in IMAGE_MAP.items():
    # Find the specific png
    matched_png = None
    for png in png_files:
        if os.path.basename(png).startswith(img_prefix + "_"):
            matched_png = png
            break
            
    if not matched_png:
        print(f"Warning: No PNG found for {img_prefix}")
        continue
        
    new_filename = f"{img_prefix}.png"
    
    # Copy to both directories
    shutil.copy(matched_png, os.path.join(concepts_img_dir, new_filename))
    shutil.copy(matched_png, os.path.join(mono_img_dir, new_filename))
    
    # Update HTML files
    for base_d in [CONCEPTS_DIR, MONO_DIR]:
        html_path = os.path.join(base_d, f"{key}.html")
        if not os.path.exists(html_path):
            continue
            
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the entire <section class="views-section">...</section>
        replacement = f'''<section class="views-section" style="text-align: center; margin: 40px 0;">
      <h2>High-Fidelity 2D Digital Render</h2>
      <p style="color: var(--text-muted); margin-bottom: 20px;">Premium isometric illustration of the physical hardware.</p>
      <img src="assets/images/{new_filename}" alt="{key} 2D Render" style="width:100%; max-width:800px; display:block; margin: 0 auto; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);">
    </section>'''
        
        # Regex to match the section and its content
        pattern = r'<section class="views-section">.*?</section>'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
print("Done updating HTML files with premium 2D illustrations!")
