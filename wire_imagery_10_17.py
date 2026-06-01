#!/usr/bin/env python3
"""Wire Product Imagery sections into products 10-17 using the
Antigravity-generated images and the captions defined in image_prompts.md."""

import os

BASE = '/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts'

# file -> [(img, caption), (img, caption)]
PHOTOS = {
    '10_hub.html': [
        ('hub_hero.png',  'Edge AI gateway — finned aluminium chassis, multi-radio antenna array &amp; industrial IO'),
        ('hub_ports.png', 'Detail view — gigabit ethernet, USB &amp; M12 power ports with status LEDs'),
    ],
    '11_crewlink.html': [
        ('crewlink_hero.png', 'Worker wearable — polycarbonate core, green TPU bumper, e-ink display &amp; SOS button'),
        ('crewlink_worn.png', 'In-use view — belt-clip mount showing heart-rate &amp; GPS-lock readout'),
    ],
    '12_agrimule.html': [
        ('agrimule_hero.png',   'Autonomous cargo UGV — rubber tracks, aluminium flatbed, LiDAR mast &amp; stereo cameras'),
        ('agrimule_loaded.png', 'Loaded configuration — secured payload, rear charge port &amp; tow hitch'),
    ],
    '13_rowplanter.html': [
        ('rowplanter_hero.png',    '12-row precision planter — toolbar, central seed hopper, row units &amp; 3-point hitch'),
        ('rowplanter_rowunit.png', 'Row-unit detail — double-disc opener, gauge &amp; closing wheels, pneumatic seed meter'),
    ],
    '14_terraplanter.html': [
        ('terraplanter_hero.png', 'Tracked sapling planter — hydraulic auger boom, 5-axis planting arm &amp; rotary magazine'),
        ('terraplanter_arm.png',  'Planting-arm detail — gripper placing a sapling above the augered hole'),
    ],
    '15_microweeder.html': [
        ('microweeder_hero.png',   'High-clearance weeding robot — portal frame, 4-wheel drive, stereo vision &amp; GPS dome'),
        ('microweeder_vision.png', 'Vision &amp; laser detail — stereo cameras targeting a weed between crop seedlings'),
    ],
    '16_brushcrusher.html': [
        ('brushcrusher_hero.png',  'Forestry mulcher — tracked chassis, protected cab, exhaust stack &amp; front flail drum'),
        ('brushcrusher_flail.png', 'Flail-head detail — carbide-toothed rotor drum with hazard striping'),
    ],
    '17_omniharvester.html': [
        ('omniharvester_hero.png',    'Autonomous harvester — wheeled base, 6-axis arm, soft gripper &amp; produce bin'),
        ('omniharvester_gripper.png', 'End-effector detail — soft gripper picking ripe produce with wrist camera'),
    ],
}

STYLE = """
  <style>
    .photos-section h2 { margin-bottom: 1rem; }
    .photos-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
    .photo-card {
      margin: 0; background: #060c1b;
      border: 1px solid rgba(30,48,96,0.8);
      border-radius: 16px; overflow: hidden;
      transition: border-color .22s ease, box-shadow .22s ease, transform .22s ease;
    }
    .photo-card:hover {
      border-color: rgba(16,185,129,0.35);
      box-shadow: 0 0 30px rgba(16,185,129,0.10);
      transform: translateY(-3px);
    }
    .photo-card img { display: block; width: 100%; height: auto; }
    .photo-card figcaption {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem; letter-spacing: 0.03em; color: #5a7aaa;
      padding: 12px 16px; border-top: 1px solid rgba(20,35,72,0.9);
      background: linear-gradient(180deg, #080e20 0%, #060c1a 100%);
    }
    @media (max-width: 768px) { .photos-grid { grid-template-columns: 1fr; } }
  </style>
"""

TARGET = '        <section class="views-section" style="margin: 40px 0;">'

ok = 0
for fname, shots in PHOTOS.items():
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'class="photos-section"' in html:
        print(f'  SKIP (already wired): {fname}')
        continue
    if TARGET not in html:
        print(f'  ERROR (no insertion target): {fname}')
        continue

    figs = ''
    for img, cap in shots:
        figs += (
            '      <figure class="photo-card">\n'
            f'        <img src="{img}" alt="Famtech product imagery" loading="lazy">\n'
            f'        <figcaption>{cap}</figcaption>\n'
            '      </figure>\n'
        )

    section = (
        '  <section class="photos-section" style="margin: 40px 0;">\n'
        '    <h2><span class="section-num">◷</span> Product Imagery</h2>\n'
        '    <div class="photos-grid">\n'
        f'{figs}'
        '    </div>\n'
        '  </section>\n'
        f'{STYLE}\n'
    )

    html = html.replace(TARGET, section + TARGET, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    ok += 1
    print(f'  ✅ wired: {fname}  ({len(shots)} images)')

print(f'\nDone — {ok}/8 pages wired.')
