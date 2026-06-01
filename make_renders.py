#!/usr/bin/env python3
import math
import os
import re

BASE = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts"
MONO = "/Users/rapid-002/Famtech Agricore /Famtech Software/Software/hardware-concepts"

def hex_to_rgb(h): 
    return tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

M_HEX = {
  'ALU':    ['#cdd2da','#9aa0ae','#626876'],
  'STEEL':  ['#b0b6c2','#808694','#505660'],
  'CARBON': ['#363840','#22242a','#10121a'],
  'HDPE':   ['#f2eedf','#c4c0ae','#8c8a80'],
  'PC':     ['#c4e4f6','#88c0e2','#4882b8'],
  'SOLAR':  ['#1e3468','#101e40','#080e22'],
  'SOLAR2': ['#243e7c','#14244e','#0a1232'],
  'RUBBER': ['#2e2e2e','#1c1c1c','#0c0c0c'],
  'TPU':    ['#b07820','#806010','#503a08'],
  'ORANGE': ['#f09030','#c06018','#884010'],
  'GREEN':  ['#38cc7c','#18a050','#0a6830'],
  'DARK':   ['#2c303c','#1c2030','#0c1020'],
  'YELLOW': ['#ecd820','#b8b010','#7a7408'],
  'SCREEN': ['#2060b0','#103880','#081840'],
  'LED_G':  ['#50ff88','#20cc54','#0c7a30'],
  'LED_B':  ['#4080ff','#2050c0','#102070'],
  'WATER':  ['#60b4f0','#3080c0','#184880'],
  'CONC':   ['#8a8678','#6a6658','#4a4840'],
  'LEAD':   ['#5c6070','#3c4050','#1c2030'],
  'RED':    ['#e03030','#a01818','#680808'],
}
M = {k: hex_to_rgb(v[1]) for k, v in M_HEX.items()}

M_SPEC = {
  'ALU':    (0.8, 40),   # highly reflective, sharp highlight
  'STEEL':  (0.5, 20),   # semi-reflective, medium highlight
  'CARBON': (0.1, 5),    # matte
  'HDPE':   (0.2, 10),   # slightly shiny plastic
  'PC':     (0.9, 60),   # very shiny clear plastic
  'SOLAR':  (0.6, 30),   # shiny glass
  'SOLAR2': (0.6, 30),
  'RUBBER': (0.05, 5),   # very matte
  'TPU':    (0.1, 5),    
  'ORANGE': (0.3, 15),
  'GREEN':  (0.3, 15),
  'DARK':   (0.1, 5),    # mostly matte
  'YELLOW': (0.3, 15),
  'SCREEN': (0.8, 50),
  'LED_G':  (0.9, 40),
  'LED_B':  (0.9, 40),
  'WATER':  (0.8, 40),
  'CONC':   (0.0, 1),
  'LEAD':   (0.2, 10),
  'RED':    (0.3, 15),
}

class RENDERER:
    def __init__(self):
        self.faces = [] 
        
    def add_quad(self, p1, p2, p3, p4, mat):
        col = M.get(mat, M['STEEL'])
        self.faces.append((col, mat, [p1, p2, p3, p4]))
        
    def add_poly(self, pts, mat):
        col = M.get(mat, M['STEEL'])
        self.faces.append((col, mat, pts))

    def box(self, x, y, z, W, H, D, mat='STEEL'):
        # 8 vertices
        v0 = (x, y, z)
        v1 = (x+W, y, z)
        v2 = (x+W, y+H, z)
        v3 = (x, y+H, z)
        v4 = (x, y, z+D)
        v5 = (x+W, y, z+D)
        v6 = (x+W, y+H, z+D)
        v7 = (x, y+H, z+D)
        
        # 6 faces (counter-clockwise looking from outside)
        self.add_quad(v3, v2, v1, v0, mat) # Front (-Z)
        self.add_quad(v4, v5, v6, v7, mat) # Back (+Z)
        self.add_quad(v0, v1, v5, v4, mat) # Bottom (-Y)
        self.add_quad(v7, v6, v2, v3, mat) # Top (+Y)
        self.add_quad(v0, v4, v7, v3, mat) # Left (-X)
        self.add_quad(v1, v2, v6, v5, mat) # Right (+X)
        
    def cyl_v(self, cx, cy, cz, r, h, mat='STEEL', seg=36):
        pts_bottom = []
        pts_top = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            nx = cx + r * math.cos(a)
            nz = cz + r * math.sin(a)
            pts_bottom.append((nx, cy, nz))
            pts_top.append((nx, cy+h, nz))
            
        self.add_poly(pts_bottom, mat)
        self.add_poly(pts_top[::-1], mat)
        for i in range(seg):
            next_i = (i + 1) % seg
            self.add_quad(pts_top[i], pts_top[next_i], pts_bottom[next_i], pts_bottom[i], mat)
            
    def cyl_h(self, cx, cy, cz, r, h, axis='x', mat='STEEL', seg=36):
        pts_left = []
        pts_right = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            if axis == 'x':
                ny = cy + r * math.cos(a)
                nz = cz + r * math.sin(a)
                pts_left.append((cx, ny, nz))
                pts_right.append((cx+h, ny, nz))
            else: # z
                nx = cx + r * math.cos(a)
                ny = cy + r * math.sin(a)
                pts_left.append((nx, ny, cz))
                pts_right.append((nx, ny, cz+h))
                
        self.add_poly(pts_left[::-1], mat)
        self.add_poly(pts_right, mat)
        for i in range(seg):
            next_i = (i + 1) % seg
            self.add_quad(pts_left[i], pts_left[next_i], pts_right[next_i], pts_right[i], mat)

    def disc(self, cx, cy, cz, r, th, mat='STEEL'):
        self.cyl_v(cx, cy, cz, r, th, mat)

    def panel(self, x, y, z, W, D, mat='SOLAR'):
        self.box(x, y, z, W, 0.02, D, mat)

    def render_view(self, rot_x, rot_y, rot_z=0, scale=100, bg='#060c1b'):
        def rotate(vx, vy, vz, rx, ry, rz):
            # Y rotation FIRST (heading)
            cy, sy = math.cos(ry), math.sin(ry)
            x1 = vx * cy + vz * sy
            y1 = vy
            z1 = -vx * sy + vz * cy
            # X rotation SECOND (pitch)
            cx, sx = math.cos(rx), math.sin(rx)
            y2 = y1 * cx - z1 * sx
            z2 = y1 * sx + z1 * cx
            # Z rotation THIRD
            cz, sz = math.cos(rz), math.sin(rz)
            x3 = x1 * cz - y2 * sz
            y3 = x1 * sz + y2 * cz
            return x3, y3, z2

        # Light vector (Top-Left-Front relative to camera space)
        lx, ly, lz = -0.5, 0.7, 0.5
        ll = math.sqrt(lx*lx + ly*ly + lz*lz)
        lx, ly, lz = lx/ll, ly/ll, lz/ll

        projected_faces = []
        rx_rad = math.radians(rot_x)
        ry_rad = math.radians(rot_y)
        rz_rad = math.radians(rot_z)
        
        for color, mat, pts in self.faces:
            rot_pts = [rotate(x, y, z, rx_rad, ry_rad, rz_rad) for x, y, z in pts]
            
            if len(rot_pts) < 3: continue
            p0, p1, p2 = rot_pts[0], rot_pts[1], rot_pts[2]
            v1x, v1y, v1z = p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]
            v2x, v2y, v2z = p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2]
            nx = v1y*v2z - v1z*v2y
            ny = v1z*v2x - v1x*v2z
            nz = v1x*v2y - v1y*v2x
            nl = math.sqrt(nx*nx + ny*ny + nz*nz)
            if nl == 0: continue
            nx, ny, nz = nx/nl, ny/nl, nz/nl
            
            # Backface culling
            if nz <= 0: continue 

            # Ambient Occlusion (darken faces pointing downwards)
            ao = 1.0
            if ny < -0.3: ao = 0.7

            # Lambertian Lighting (Diffuse)
            dot_nl = nx*lx + ny*ly + nz*lz
            intensity = max(0, min(1, dot_nl))
            
            ambient = 0.35
            diffuse = 0.65
            factor = (ambient + diffuse * intensity) * ao
            
            # Specular Highlights (Phong)
            spec_intensity = 0
            if dot_nl > 0:
                spec_coeff, shininess = M_SPEC.get(mat, (0.1, 5))
                # R = 2*(N.L)*N - L
                rz = 2 * dot_nl * nz - lz
                spec_intensity = spec_coeff * (max(0, rz) ** shininess)
            
            r, g, b = color
            r = min(255, int(r * factor + 255 * spec_intensity))
            g = min(255, int(g * factor + 255 * spec_intensity))
            b = min(255, int(b * factor + 255 * spec_intensity))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            screen_pts = [(x * scale, -y * scale) for x, y, z in rot_pts]
            
            # Depth sorting using the furthest point of the polygon to prevent overlapping bugs
            min_z = min(p[2] for p in rot_pts)
            projected_faces.append((min_z, hex_color, screen_pts))
            
        # Painter's algorithm
        projected_faces.sort(key=lambda x: x[0])
        
        svg_parts = []
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')
        
        for _, hex_col, pts in projected_faces:
            pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            # Use same color for stroke to remove cartoon outline but prevent anti-aliasing gaps
            svg_parts.append(f'<polygon points="{pts_str}" fill="{hex_col}" stroke="{hex_col}" stroke-width="0.6" stroke-linejoin="round"/>')
            for x, y in pts:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
                
        w = max_x - min_x if max_x != float('-inf') else 100
        h = max_y - min_y if max_y != float('-inf') else 100
        if w == 0: w = 100
        if h == 0: h = 100
        
        cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2
        
        # Consistent square bounding box to prevent stretching
        vbox_s = max(w, h) * 1.5
        vbox_x = cx - vbox_s/2
        vbox_y = cy - vbox_s/2
        
        # Soft Drop Shadow Filter
        defs = '''<defs>
          <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="15" stdDeviation="15" flood-color="#000000" flood-opacity="0.6"/>
          </filter>
        </defs>'''
        
        shapes = "".join(svg_parts)
        return f'<svg viewBox="{vbox_x:.1f} {vbox_y:.1f} {vbox_s:.1f} {vbox_s:.1f}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%; display:block;">{defs}<g filter="url(#shadow)">{shapes}</g></svg>'


# ── Per-product illustration data ─────────────────────────────────────────────

def make_spray_x(iso):
    iso.box(-0.17,-0.01,-0.17, 0.34,0.18,0.34, 'CARBON')
    iso.box(-0.14, 0.17,-0.14, 0.28,0.04,0.28, 'ALU')
    for deg in [0,60,120,180,240,300]:
        a=math.radians(deg); L=0.74; r=0.028
        cx=math.cos(a)*L/2; cz=math.sin(a)*L/2
        iso.box(cx-L/2*math.cos(a),-0.01+0.06, cz-L/2*math.sin(a), L*abs(math.cos(a))+r, 0.06, L*abs(math.sin(a))+r, 'CARBON')
        mx=math.cos(a)*0.76; mz=math.sin(a)*0.76
        iso.cyl_v(mx, 0.06, mz, 0.042, 0.055, 'DARK')
        iso.disc(mx, 0.118, mz, 0.16, 0.006, 'CARBON')
    iso.cyl_v(-0.20,-0.32,-0.15, 0.20,0.22,'HDPE')
    iso.box(-0.82,-0.34,-0.008, 1.64,0.04,0.016, 'ALU')
    for nx in [-0.66,-0.44,-0.22,0,0.22,0.44,0.66]:
        iso.cyl_v(nx,-0.40,-0.008, 0.008,0.06,'HDPE')

def make_scout(iso):
    iso.box(-0.065,-0.028,-0.065, 0.130,0.060,0.130, 'DARK')
    iso.box(-0.055, 0.032,-0.055, 0.110,0.020,0.110, 'CARBON')
    for deg in [45,135,225,315]:
        a=math.radians(deg); L=0.110; r=0.012
        cx=math.cos(a)*L/2; cz=math.sin(a)*L/2
        iso.box(cx-0.05, 0, cz-0.05, 0.10,0.015,0.10, 'CARBON')
        mx=math.cos(a)*L; mz=math.sin(a)*L
        iso.cyl_v(mx,0.010,mz, 0.016,0.024,'DARK')
        iso.disc(mx,0.030,mz, 0.085,0.004,'CARBON')
    iso.box(-0.025,-0.040,-0.005, 0.050,0.032,0.040, 'DARK')
    iso.cyl_v(-0.002,-0.045,0.028, 0.010,0.020,'PC')

def make_nest(iso):
    iso.box(-0.60,-0.70,-0.60, 1.20,0.10,1.20,'STEEL')
    for face,(px,pz,W,D) in enumerate([( 0.56,-0.60,0.04,1.20),(-0.60,-0.60,0.04,1.20),
                                        (-0.60, 0.56,1.20,0.04),(-0.60,-0.60,1.20,0.04)]):
        iso.box(px,-0.60,pz, W,1.30,D,'ALU')
    iso.box(-0.44,0.60,-0.57, 0.88,0.04,1.14,'ALU')
    iso.box( 0.00,0.60,-0.57, 0.88,0.04,1.14,'ALU')
    iso.box(-0.60,0.54,-0.58, 0.88,0.04,0.30,'DARK')
    iso.panel(-0.44,0.60,-0.44, 0.88,0.88,'DARK')
    iso.box(-0.58,-0.10,-0.55, 0.30,0.80,0.82,'DARK')

def make_watchtower(iso):
    iso.box(-0.25,-0.20,-0.25, 0.50,0.30,0.50,'CONC')
    iso.cyl_v(-0.02, 0.10,-0.02, 0.038,5.20,'STEEL')
    iso.box( 0.04,3.10, 0.00, 0.28,0.20,0.16,'DARK')
    iso.panel(-0.04,4.54, 0.26, 0.68,0.44,'SOLAR')
    iso.cyl_v(-0.02,5.24,-0.02, 0.095,0.13,'DARK')
    iso.disc(-0.02,5.38,-0.02, 0.130,0.06,'PC')
    iso.cyl_v( 0.04,5.50,-0.02, 0.007,0.36,'ALU')
    iso.cyl_v(-0.04,5.45,-0.02, 0.005,0.26,'ALU')

def make_soilnode(iso):
    iso.cyl_v(-0.002, 0,-0.002, 0.046,0.15,'HDPE')
    iso.disc(-0.002,0.152,-0.002, 0.046,0.010,'SOLAR')
    iso.cyl_v(-0.002,-0.005,-0.002, 0.046,0.018,'ALU')
    iso.cyl_v(-0.002,-0.110,-0.002, 0.022,0.200,'STEEL')
    for deg in [0,120,240]:
        a=math.radians(deg)
        iso.cyl_v(math.cos(a)*0.016-0.002,-0.200,math.sin(a)*0.016-0.002, 0.003,0.065,'GREEN')

def make_feedpro(iso):
    iso.box(-0.46,-0.06,-0.34, 0.92,0.30,0.68,'DARK')
    for px,pz in [(-0.44,-0.32),(-0.44,0.30),(0.44,-0.32),(0.44,0.30)]:
        iso.cyl_v(px,-0.06,pz, 0.018,1.90,'STEEL')
    iso.box(-0.44, 0.78,-0.28, 0.46,0.60,0.54,'HDPE')
    iso.box(-0.44, 0.50,-0.24, 0.38,0.18,0.44,'HDPE')
    iso.box(-0.44, 1.38,-0.28, 0.48,0.04,0.56,'ALU')
    iso.box(-0.78, 0.30,-0.28, 0.22,0.10,0.56,'ALU')
    iso.cyl_v(0.24, 0.60,-0.002, 0.175,0.76,'HDPE')
    iso.disc(0.24, 1.36,-0.002, 0.185,0.04,'ALU')
    iso.cyl_v(0.24, 1.50,-0.002, 0.016,0.28,'STEEL')
    iso.disc(0.24, 1.686,-0.002, 0.19,0.018,'STEEL')
    iso.cyl_v(0.44, 0.24,-0.002, 0.014,0.88,'STEEL')
    iso.cyl_h(0.44, 1.05, 0.16, 0.012,0.36,'z','STEEL')
    iso.cyl_v(0.44,1.04, 0.40, 0.020,0.06,'ALU')
    iso.panel(-0.46, 1.76,-0.30, 0.90,0.60,'SOLAR')
    iso.box( 0.28, 0.70, 0.21, 0.18,0.22,0.06,'DARK')
    iso.box( 0.28, 0.72, 0.268, 0.11,0.12,0.005,'SCREEN')

def make_herdtag(iso):
    iso.box(-0.024,-0.0075,-0.018, 0.048,0.015,0.036,'TPU')
    iso.box(-0.018,-0.0040,-0.012, 0.036,0.008,0.026,'DARK')
    iso.box(-0.016,-0.0020,-0.010, 0.032,0.003,0.022,'GREEN')
    iso.cyl_v(-0.002, 0.010,-0.002, 0.0030,0.018,'STEEL')
    iso.cyl_v(-0.002,-0.014,-0.002, 0.0025,0.016,'STEEL')

def make_aquasense(iso):
    for deg in range(0,360,18):
        a=math.radians(deg); R=0.20; r=0.09
        cx2=math.cos(a)*R; cz2=math.sin(a)*R
        iso.box(cx2-r*0.6,-0.09,cz2-r*0.6, r*1.2,0.18,r*1.2,'HDPE')
    iso.panel(-0.19, 0.10,-0.19, 0.38,0.38,'SOLAR')
    iso.box(-0.046, 0.06,-0.046, 0.092,0.050,0.092,'DARK')
    iso.cyl_v(-0.002,-0.06,-0.002, 0.055,0.26,'ALU')
    iso.cyl_h(-0.044,-0.17,-0.002, 0.008,0.10,'x','STEEL')
    iso.cyl_h(-0.002,-0.17,-0.044, 0.008,0.10,'x','STEEL')
    iso.cyl_h( 0.040,-0.17,-0.002, 0.008,0.10,'x','STEEL')
    iso.cyl_v(-0.002,-0.38,-0.002, 0.075,0.055,'LEAD')

def make_fencegrid(iso):
    iso.box(-0.090,-0.029,-0.055, 0.180,0.058,0.110,'PC')
    for x in [-0.030,0.030]:
        iso.box(x,-0.027,-0.053, 0.004,0.054,0.106,'DARK')
    iso.disc(-0.002, 0.030,-0.002, 0.024,0.008,'PC')
    iso.box(-0.070, 0.022, 0.052, 0.140,0.010,0.004,'SOLAR')
    iso.box(-0.090,-0.042,-0.006, 0.100,0.012,0.080,'STEEL')

def make_hub(iso):
    iso.box(-0.210,-0.080,-0.160, 0.420,0.160,0.320,'DARK')
    iso.box(-0.180,-0.080,-0.128, 0.360,0.010,0.256,'ALU')
    for x in range(-6,7,2):
        iso.cyl_v(x*0.028,-0.064,-0.160, 0.006,0.060,'ALU')
    for y in range(3):
        iso.box(-0.216,-0.040+y*0.028,-0.150, 0.008,0.016,0.012,'DARK')
    iso.box(-0.106,-0.080,-0.170, 0.212,0.160,0.012,'DARK')

def make_crewlink(iso):
    iso.box(-0.0325,-0.009,-0.022, 0.065,0.018,0.045,'TPU')
    iso.box(-0.026,-0.005,-0.018, 0.052,0.008,0.036,'DARK')
    iso.box(-0.020,-0.003,-0.014, 0.040,0.010,0.028,'SCREEN')
    iso.cyl_v( 0.022,0.004,-0.010, 0.005,0.006,'ORANGE')
    iso.cyl_v(-0.002, 0.010,-0.010, 0.004,0.010,'ALU')

def make_agrimule(iso):
    iso.box(-1.20,-0.24,-0.78, 2.40,0.28,0.20,'RUBBER')
    iso.box(-1.20,-0.24, 0.58, 2.40,0.28,0.20,'RUBBER')
    iso.box(-0.76, 0.04,-0.64, 1.52,0.88,1.28,'ALU')
    iso.box(-0.56, 0.14,-0.44, 1.12,0.52,0.88,'DARK')
    iso.cyl_v(-0.002, 0.54,-0.002, 0.070,0.060,'DARK')
    iso.disc(-0.002, 0.60,-0.002, 0.075,0.016,'DARK')
    iso.panel(-0.54, 0.96,-0.44, 1.08,0.88,'SOLAR')
    iso.box(-1.25,-0.04,-0.08, 0.10,0.14,0.16,'STEEL')

def make_rowplanter(iso):
    iso.box(-3.0, 0.60,-0.16, 6.0,0.14,0.32,'STEEL')
    for i in range(8):
        x = -3.0 + 0.75 + i*0.86
        iso.box(x-0.08,-0.40,-0.18, 0.16,1.00,0.36,'DARK')
        iso.box(x-0.10, 0.54,-0.20, 0.20,0.12,0.40,'GREEN')
        iso.disc(x,-0.42,-0.002, 0.12,0.04,'STEEL')
    iso.box(-2.90, 0.70,-0.02, 5.80,0.04,0.04,'DARK')

def make_terraplanter(iso):
    for px,pz in [(-1.0,0.0),( 1.0,0.0),(-1.0,-0.80),( 1.0,-0.80)]:
        iso.disc(px,-0.38,pz, 0.24,0.14,'RUBBER')
    iso.box(-0.88, 0.00,-0.70, 1.76,0.88,0.70,'ALU')
    iso.box(-0.64, 0.10,-0.50, 1.28,0.60,0.50,'DARK')
    iso.cyl_v(0.80, 0.88,-0.34, 0.040,0.90,'STEEL')
    iso.box( 0.56, 1.76,-0.20, 0.50,0.12,0.40,'STEEL')
    iso.box( 0.80, 1.84,-0.24, 0.14,0.22,0.22,'DARK')
    iso.disc(-0.002, 1.00,-0.34, 0.20,0.04,'ORANGE')

def make_microweeder(iso):
    iso.box(-0.80, 0.10,-0.60, 0.06,0.80,0.06,'STEEL')
    iso.box( 0.74, 0.10,-0.60, 0.06,0.80,0.06,'STEEL')
    iso.box(-0.80, 0.10, 0.54, 0.06,0.80,0.06,'STEEL')
    iso.box( 0.74, 0.10, 0.54, 0.06,0.80,0.06,'STEEL')
    iso.box(-0.78, 0.90,-0.58, 1.56,0.06,0.06,'STEEL')
    iso.box(-0.78, 0.90, 0.50, 1.56,0.06,0.06,'STEEL')
    for ax,az in [(-0.46,-0.002),(0.44,-0.002)]:
        iso.cyl_v(ax, 0.52,-0.002, 0.020,0.32,'ALU')
    iso.cyl_v(-0.002, 0.52,-0.002, 0.020,0.32,'ALU')
    iso.box(-0.16, 0.06,-0.12, 0.32,0.20,0.24,'DARK')
    iso.disc(-0.002, 0.04,-0.002, 0.06,0.04,'RED')
    iso.box(-0.10, 0.52,-0.02, 0.20,0.10,0.14,'DARK')

def make_brushcrusher(iso):
    iso.box(-1.90, 0.02,-1.04, 3.80,0.80,2.08,'STEEL')
    for i in range(12):
        iso.box(-1.72+i*0.30,-0.04,-1.00, 0.18,0.28,2.00,'DARK')
    iso.cyl_h(-1.86, 0.12,-0.002, 0.28,3.72,'x','DARK')
    for xi in range(14):
        for zi in range(3):
            iso.box(-1.86+xi*0.27, 0.34,-0.90+zi*0.58, 0.10,0.14,0.10,'YELLOW')
    iso.disc(1.72, 0.12,-0.002, 0.18,0.10,'DARK')
    iso.box(-1.90, 0.82,-1.04, 3.80,0.08,2.08,'STEEL')
    iso.box(1.92,-0.06,-0.40, 0.12,0.70,0.80,'STEEL')

def make_omniharvester(iso):
    for px,pz in [(-1.20,0.08),(1.20,0.08),(-1.20,-1.18),(1.20,-1.18)]:
        iso.disc(px,-0.38,pz, 0.24,0.32,'RUBBER')
    iso.box(-1.14, 0.02,-1.06, 2.28,3.00,1.06,'ALU')
    iso.box(-0.88, 0.12,-0.84, 1.76,2.60,0.84,'DARK')
    iso.box(-1.08, 0.00,-0.52, 2.16,0.08,0.96,'RUBBER')
    for k in range(3):
        iso.box( 1.12, 0.30+k*0.72,-0.44, 0.22,0.16,0.88,'GREEN')
        iso.box(-1.34, 0.30+k*0.72,-0.44, 0.22,0.16,0.88,'GREEN')
        iso.disc(1.32, 0.38+k*0.72,-0.002, 0.12,0.04,'ALU')
        iso.disc(-1.36,0.38+k*0.72,-0.002, 0.12,0.04,'ALU')
    for xi in range(3):
        iso.box(-0.66+xi*0.62, 2.42,-0.53, 0.14,0.09,0.09,'DARK')

PRODUCT_FUNCS = [
    ('01','01_spray_x.html',    make_spray_x),
    ('02','02_scout.html',      make_scout),
    ('03','03_nest.html',       make_nest),
    ('04','04_watchtower.html', make_watchtower),
    ('05','05_soilnode.html',   make_soilnode),
    ('06','06_feedpro.html',    make_feedpro),
    ('07','07_herdtag.html',    make_herdtag),
    ('08','08_aquasense.html',  make_aquasense),
    ('09','09_fencegrid.html',  make_fencegrid),
    ('10','10_hub.html',        make_hub),
    ('11','11_crewlink.html',   make_crewlink),
    ('12','12_agrimule.html',   make_agrimule),
    ('13','13_rowplanter.html', make_rowplanter),
    ('14','14_terraplanter.html',make_terraplanter),
    ('15','15_microweeder.html',make_microweeder),
    ('16','16_brushcrusher.html',make_brushcrusher),
    ('17','17_omniharvester.html',make_omniharvester),
]

def build_4_views_html(iso_svg, front_svg, side_svg, top_svg):
    return f'''
  <section class="views-section" style="margin: 40px 0;">
    <h2 style="text-align:center; margin-bottom:10px;">High-Fidelity 2D Digital Renders</h2>
    <p style="color: var(--text-muted); text-align:center; margin-bottom: 30px;">Professional 4-View 3D-to-2D Projection (Isometric, Front, Side, Top)</p>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Isometric View</div>
        <div style="aspect-ratio: 4/3; padding: 20px;">{iso_svg}</div>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Front View</div>
        <div style="aspect-ratio: 4/3; padding: 20px;">{front_svg}</div>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Side View</div>
        <div style="aspect-ratio: 4/3; padding: 20px;">{side_svg}</div>
      </div>
      <div class="view-card" style="background:var(--panel-bg); border-radius:12px; border:1px solid var(--border-color); overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <div style="background:#14171f; padding:8px 15px; font-weight:600; font-size:0.9rem; border-bottom:1px solid var(--border-color); color:var(--text-color);">Top View</div>
        <div style="aspect-ratio: 4/3; padding: 20px;">{top_svg}</div>
      </div>
    </div>
  </section>
'''

for prod_id, filename, func in PRODUCT_FUNCS:
    # 1. Update in AgriCore_Hardware_Concepts
    path1 = os.path.join(BASE, filename)
    # 2. Update in monorepo
    path2 = os.path.join(MONO, filename)
    
    if not os.path.exists(path1): continue
        
    with open(path1, encoding='utf-8') as f:
        html = f.read()

    r = RENDERER()
    func(r)
    
    iso_svg = r.render_view(rot_x=35.264, rot_y=45)
    front_svg = r.render_view(rot_x=0, rot_y=0)
    side_svg = r.render_view(rot_x=0, rot_y=90)
    top_svg = r.render_view(rot_x=90, rot_y=0)
    
    views_html = build_4_views_html(iso_svg, front_svg, side_svg, top_svg)

    # Remove the old illus-section if it exists
    html = re.sub(r'<section class="illus-section">.*?</section>', '', html, flags=re.DOTALL)
    
    # Replace the views-section with the new unified 4-view section
    if '<section class="views-section"' in html:
        html = re.sub(r'<section class="views-section".*?</section>',
                      views_html, html, flags=re.DOTALL, count=1)
    elif '<section class="views-section">' in html:
        html = re.sub(r'<section class="views-section">.*?</section>',
                      views_html, html, flags=re.DOTALL, count=1)
    else:
        # If no views-section, insert before features
        html = re.sub(r'<section class="features-section">', views_html + '\n<section class="features-section">', html)

    for p in [path1, path2]:
        if os.path.exists(p):
            with open(p, 'w', encoding='utf-8') as f:
                f.write(html)
                
    print(f"  ✓  {filename}")

print(f"\nDone. {len(PRODUCT_FUNCS)} files updated with high-fidelity lit 4-view renders.")
