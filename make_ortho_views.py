#!/usr/bin/env python3
import re, os, math

BASE = "/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts"

# Material palette
M = {
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

def _f(v): return f"{v:.1f}"

class ORTHO:
    def __init__(self, scale=100):
        self.s = scale
        # We will build front, top, side simultaneously
        self.front_parts = []
        self.top_parts = []
        self.side_parts = []

    def _rect(self, cx, cy, w, h, col, depth, parts):
        """Helper to draw a center-anchored rectangle"""
        rx = cx - w/2
        ry = cy - h/2
        sw = 0.5
        parts.append((depth, f'<rect x="{_f(rx)}" y="{_f(ry)}" width="{_f(w)}" height="{_f(h)}" fill="{col}" stroke="rgba(0,0,0,0.3)" stroke-width="{sw}"/>'))

    def _poly(self, pts, col, depth, parts):
        pstr = " ".join(f"{_f(x)},{_f(y)}" for x,y in pts)
        sw = 0.5
        parts.append((depth, f'<polygon points="{pstr}" fill="{col}" stroke="rgba(0,0,0,0.3)" stroke-width="{sw}"/>'))

    def _ellipse(self, cx, cy, rx, ry, col, depth, parts):
        sw = 0.5
        parts.append((depth, f'<ellipse cx="{_f(cx)}" cy="{_f(cy)}" rx="{_f(rx)}" ry="{_f(ry)}" fill="{col}" stroke="rgba(0,0,0,0.3)" stroke-width="{sw}"/>'))

    def box(self, x, y, z, W, H, D, mat='STEEL', opacity=1.0):
        cols = M.get(mat, M['STEEL'])
        # Center coordinates
        cx = x + W/2
        cy = y + H/2
        cz = z + D/2
        
        # Front: XY plane (looking down -Z)
        self._rect(cx * self.s, -cy * self.s, W * self.s, H * self.s, cols[1], z, self.front_parts)
        
        # Top: XZ plane (looking down -Y)
        self._rect(cx * self.s, cz * self.s, W * self.s, D * self.s, cols[0], y, self.top_parts)
        
        # Side (Right): ZY plane (looking down -X)
        self._rect(cz * self.s, -cy * self.s, D * self.s, H * self.s, cols[2], x, self.side_parts)

    def cyl_v(self, cx, cy, cz, r, h, mat='STEEL', seg=14):
        cols = M.get(mat, M['STEEL'])
        y_center = cy + h/2
        
        # Front: XY (looks like a rect)
        self._rect(cx * self.s, -y_center * self.s, r*2 * self.s, h * self.s, cols[1], cz, self.front_parts)
        
        # Top: XZ (looks like a circle)
        self._ellipse(cx * self.s, cz * self.s, r * self.s, r * self.s, cols[0], cy+h, self.top_parts)
        
        # Side: ZY (looks like a rect)
        self._rect(cz * self.s, -y_center * self.s, r*2 * self.s, h * self.s, cols[2], cx, self.side_parts)

    def cyl_h(self, cx, cy, cz, r, h, axis='x', mat='STEEL'):
        cols = M.get(mat, M['STEEL'])
        if axis == 'x':
            # Front: circle or rect? X axis means left-right. Front view sees a rect.
            self._rect(cx * self.s, -cy * self.s, h * self.s, r*2 * self.s, cols[1], cz, self.front_parts)
            # Top: XZ sees a rect
            self._rect(cx * self.s, cz * self.s, h * self.s, r*2 * self.s, cols[0], cy, self.top_parts)
            # Side: ZY sees a circle
            self._ellipse(cz * self.s, -cy * self.s, r * self.s, r * self.s, cols[2], cx+h/2, self.side_parts)
        else: # z axis
            # Front: XY sees a circle
            self._ellipse(cx * self.s, -cy * self.s, r * self.s, r * self.s, cols[1], cz+h/2, self.front_parts)
            # Top: XZ sees a rect
            self._rect(cx * self.s, cz * self.s, r*2 * self.s, h * self.s, cols[0], cy, self.top_parts)
            # Side: ZY sees a rect
            self._rect(cz * self.s, -cy * self.s, h * self.s, r*2 * self.s, cols[2], cx, self.side_parts)

    def disc(self, cx, cy, cz, r, th, mat='STEEL'):
        self.cyl_v(cx, cy, cz, r, th, mat)

    def panel(self, x, y, z, W, D, mat='SOLAR'):
        self.box(x, y, z, W, 0.02, D, mat)

    def render(self, vw=260, vh=192, bg='#060c1b'):
        """Return 3 SVG strings: front, side, top"""
        grid = ('<defs>'
                '<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">'
                '<path d="M20,0L0,0L0,20" fill="none" stroke="#0d1a38" stroke-width=".6"/>'
                '</pattern></defs>'
                f'<rect width="{vw}" height="{vh}" fill="{bg}"/>'
                f'<rect width="{vw}" height="{vh}" fill="url(#g)"/>')

        def build_svg(parts, invert_depth=False):
            # Sort back to front based on depth
            parts.sort(key=lambda p: p[0], reverse=invert_depth)
            
            # Find bounding box to center the model
            min_x, max_x = float('inf'), float('-inf')
            min_y, max_y = float('inf'), float('-inf')
            
            # Simple fast parse of cx/cy or x/y from SVG strings to find bounds
            for _, s in parts:
                for match in re.finditer(r'(?:cx|x)="([^"]+)" (?:cy|y)="([^"]+)"', s):
                    xx, yy = float(match.group(1)), float(match.group(2))
                    min_x = min(min_x, xx)
                    max_x = max(max_x, xx)
                    min_y = min(min_y, yy)
                    max_y = max(max_y, yy)
            
            w = max_x - min_x if max_x != float('-inf') else 100
            h = max_y - min_y if max_y != float('-inf') else 100
            if w == 0: w = 100
            if h == 0: h = 100
            
            # Add padding
            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2
            
            vbox_w = w * 1.5
            vbox_h = h * 1.5
            
            # Make sure it fits nicely
            vbox_x = cx - vbox_w/2
            vbox_y = cy - vbox_h/2
            
            shapes = ''.join(p[1] for p in parts)
            return f'<svg viewBox="{_f(vbox_x)} {_f(vbox_y)} {_f(vbox_w)} {_f(vbox_h)}" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%;">{grid}{shapes}</svg>'

        # For front view, smaller z is further away
        front_svg = build_svg(self.front_parts, invert_depth=False)
        # For top view, smaller y is further away
        top_svg = build_svg(self.top_parts, invert_depth=False)
        # For side view, smaller x is further away
        side_svg = build_svg(self.side_parts, invert_depth=False)
        
        return front_svg, side_svg, top_svg

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

def build_views_html(front, side, top):
    return (
        f'<section class="views-section">\n'
        f'  <h2>2D Technical Views</h2>\n'
        f'  <div class="views-grid">\n'
        f'    <div class="view-card"><div class="view-label-bar">Front View</div>{front}</div>\n'
        f'    <div class="view-card"><div class="view-label-bar">Side View</div>{side}</div>\n'
        f'    <div class="view-card"><div class="view-label-bar">Top View</div>{top}</div>\n'
        f'  </div>\n'
        f'</section>'
    )

for prod_id, filename, func in PRODUCT_FUNCS:
    path = os.path.join(BASE, filename)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    ortho = ORTHO(scale=100)
    func(ortho)
    front, side, top = ortho.render()
    
    views_html = build_views_html(front, side, top)

    # Replace the existing views-section
    if '<section class="views-section">' in html:
        html = re.sub(r'<section class="views-section">.*?</section>',
                      views_html, html, flags=re.DOTALL, count=1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✓  {filename}")
    else:
        print(f"  x  {filename} - no views-section found")

print(f"\nDone. {len(PRODUCT_FUNCS)} files updated with orthographic views.")
