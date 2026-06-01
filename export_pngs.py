import sys
import os
import cairosvg

# Add AgriCore_Hardware_Concepts to path so we can import make_renders
sys.path.append('/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts')
import make_renders

# Create output dir
os.makedirs('ai_refs', exist_ok=True)

r = make_renders.RENDERER()
make_renders.make_spray_x(r)

iso_svg = r.render_view(rot_x=35.264, rot_y=45)
front_svg = r.render_view(rot_x=0, rot_y=0)
side_svg = r.render_view(rot_x=0, rot_y=90)
top_svg = r.render_view(rot_x=90, rot_y=0)

cairosvg.svg2png(bytestring=iso_svg.encode('utf-8'), write_to='ai_refs/spray_x_iso.png', output_width=800, output_height=800)
cairosvg.svg2png(bytestring=front_svg.encode('utf-8'), write_to='ai_refs/spray_x_front.png', output_width=800, output_height=800)
cairosvg.svg2png(bytestring=side_svg.encode('utf-8'), write_to='ai_refs/spray_x_side.png', output_width=800, output_height=800)
cairosvg.svg2png(bytestring=top_svg.encode('utf-8'), write_to='ai_refs/spray_x_top.png', output_width=800, output_height=800)

print("Exported 4 PNGs.")
