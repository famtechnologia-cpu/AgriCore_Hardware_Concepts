import sys
import os
import subprocess

sys.path.append('/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts')
import make_renders

os.makedirs('ai_refs', exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def svg_to_png(svg_html, out_path):
    # Write SVG to a clean HTML file
    html = f'''<!DOCTYPE html>
<html><body style="margin:0; background:#000;">
<div style="width:800px; height:800px; display:flex; justify-content:center; align-items:center;">
{svg_html}
</div>
</body></html>'''
    tmp_path = os.path.abspath('tmp_render.html')
    with open(tmp_path, 'w') as f:
        f.write(html)
    
    # Run Chrome headless to screenshot
    subprocess.run([
        CHROME,
        "--headless",
        "--disable-gpu",
        "--window-size=800,800",
        f"--screenshot={os.path.abspath(out_path)}",
        f"file://{tmp_path}"
    ], capture_output=True)
    os.remove(tmp_path)

r = make_renders.RENDERER()
make_renders.make_spray_x(r)

print("Rendering views...")
iso = r.render_view(rot_x=35.264, rot_y=45)
front = r.render_view(rot_x=0, rot_y=0)
side = r.render_view(rot_x=0, rot_y=90)
top = r.render_view(rot_x=90, rot_y=0)

print("Taking screenshots with Chrome...")
svg_to_png(iso, 'ai_refs/spray_x_iso.png')
svg_to_png(front, 'ai_refs/spray_x_front.png')
svg_to_png(side, 'ai_refs/spray_x_side.png')
svg_to_png(top, 'ai_refs/spray_x_top.png')

print("Done generating 4 structural blueprints for 01_spray_x!")
