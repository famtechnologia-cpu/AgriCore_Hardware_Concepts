#!/usr/bin/env python3
"""Add Open Graph + Twitter Card meta tags to all pages so shared links
render rich preview cards (image + title + description)."""

import os

BASE = '/Users/rapid-002/Famtech Agricore /AgriCore_Hardware_Concepts'
SITE = 'https://agricore-hardware-concepts.vercel.app'

VIEWPORT = '  <meta name="viewport" content="width=device-width, initial-scale=1.0">'

# file -> (page_path, title, description, hero_image)
PAGES = {
    'index.html': ('/index.html',
        'Famtech AgriCore — Hardware Catalog',
        '17 specialized hardware systems for precision agriculture, autonomous field operations, aquaculture & livestock management.',
        'spray_x_hero_1779399245364.png'),
    '01_spray_x.html': ('/01_spray_x.html',
        'Famtech Spray X — AgriCore Hardware',
        'Precision agricultural sprayer drone — 20 L tank, variable-rate nozzles & RTK positioning.',
        'spray_x_hero_1779399245364.png'),
    '02_scout.html': ('/02_scout.html',
        'Famtech Scout — AgriCore Hardware',
        'Multispectral crop scouting drone — 5-band sensor array, NDVI mapping & 45-min flight time.',
        'scout_hero_1779399880747.png'),
    '03_nest.html': ('/03_nest.html',
        'Famtech Nest — AgriCore Hardware',
        'Autonomous drone docking, recharging & weather-shelter station for unattended field ops.',
        'nest_hero_1779399909314.png'),
    '04_watchtower.html': ('/04_watchtower.html',
        'Famtech Watchtower — AgriCore Hardware',
        'Farm security & crop monitoring tower — PTZ camera, multispectral sensors & LoRa gateway.',
        'watchtower_hero_1779399938007.png'),
    '05_soilnode.html': ('/05_soilnode.html',
        'Famtech Soilnode — AgriCore Hardware',
        'In-field soil intelligence sensor — moisture, EC, pH, temperature & NPK at three depths.',
        'soilnode_hero_1779400004722.png'),
    '06_feedpro.html': ('/06_feedpro.html',
        'Famtech Feedpro — AgriCore Hardware',
        'Multi-species automated feeding station for poultry, livestock & aquaculture, solar-powered.',
        'feedpro_hero_1779400036426.png'),
    '07_herdtag.html': ('/07_herdtag.html',
        'Famtech Herdtag — AgriCore Hardware',
        'Livestock health & location tracker — biometric sensing, GPS & five-year battery life.',
        'herdtag_hero_1779400063942.png'),
    '08_aquasense.html': ('/08_aquasense.html',
        'Famtech Aquasense — AgriCore Hardware',
        'Aquaculture water-quality monitoring buoy — DO, pH, temperature, turbidity & algae sensors.',
        'aquasense_hero_1779400127520.png'),
    '09_fencegrid.html': ('/09_fencegrid.html',
        'Famtech Fencegrid — AgriCore Hardware',
        'Perimeter intrusion detection node — vibration, PIR & seismic sensing on existing fencelines.',
        'fencegrid_hero_1779400158295.png'),
    '10_hub.html': ('/10_hub.html',
        'Famtech Hub — AgriCore Hardware',
        'Farm edge AI gateway & compute node with multi-radio connectivity and local inference.',
        'hub_hero.png'),
    '11_crewlink.html': ('/11_crewlink.html',
        'Famtech CrewLink — AgriCore Hardware',
        'Farm worker safety & tracking wearable — biometrics, GPS, fall detection & emergency SOS.',
        'crewlink_hero.png'),
    '12_agrimule.html': ('/12_agrimule.html',
        'Famtech AgriMule — AgriCore Hardware',
        'Autonomous electric cargo UGV — 500 kg payload, terrain following & autonomous navigation.',
        'agrimule_hero.png'),
    '13_rowplanter.html': ('/13_rowplanter.html',
        'Famtech RowPlanter — AgriCore Hardware',
        '12-row pneumatic precision row-crop planter with variable-rate seeding & stand mapping.',
        'rowplanter_hero.png'),
    '14_terraplanter.html': ('/14_terraplanter.html',
        'Famtech TerraPlanter — AgriCore Hardware',
        'Autonomous tree & forestry sapling planter — terrain-adaptive arm, soil augering & GPS mapping.',
        'terraplanter_hero.png'),
    '15_microweeder.html': ('/15_microweeder.html',
        'Famtech MicroWeeder — AgriCore Hardware',
        'Precision computer-vision laser & blade weeder with per-plant weed ID between crop rows.',
        'microweeder_hero.png'),
    '16_brushcrusher.html': ('/16_brushcrusher.html',
        'Famtech BrushCrusher — AgriCore Hardware',
        'Heavy-duty diesel forestry mulcher & land-clearing system with high-inertia flail rotor.',
        'brushcrusher_hero.png'),
    '17_omniharvester.html': ('/17_omniharvester.html',
        'Famtech OmniHarvester — AgriCore Hardware',
        'Autonomous modular robotic harvester — 6-DOF arm, multi-crop vision AI & swappable end-effectors.',
        'omniharvester_hero.png'),
}

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')

ok = 0
for fname, (path, title, desc, img) in PAGES.items():
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'og:image' in html:
        print(f'  SKIP (already has OG): {fname}')
        continue
    if VIEWPORT not in html:
        print(f'  ERROR (no viewport line): {fname}')
        continue

    t, d = esc(title), esc(desc)
    url = SITE + path
    img_abs = SITE + '/' + img

    # Add a name=description meta only if the page lacks one
    desc_meta = ''
    if 'name="description"' not in html:
        desc_meta = f'  <meta name="description" content="{d}">\n'

    block = (
        VIEWPORT + '\n'
        + desc_meta +
        f'  <link rel="canonical" href="{url}">\n'
        '  <!-- Open Graph -->\n'
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="Famtech AgriCore">\n'
        f'  <meta property="og:title" content="{t}">\n'
        f'  <meta property="og:description" content="{d}">\n'
        f'  <meta property="og:url" content="{url}">\n'
        f'  <meta property="og:image" content="{img_abs}">\n'
        '  <meta property="og:image:width" content="1024">\n'
        '  <meta property="og:image:height" content="1024">\n'
        f'  <meta property="og:image:alt" content="{t}">\n'
        '  <!-- Twitter -->\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{t}">\n'
        f'  <meta name="twitter:description" content="{d}">\n'
        f'  <meta name="twitter:image" content="{img_abs}">'
    )

    html = html.replace(VIEWPORT, block, 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    ok += 1
    print(f'  ✅ {fname}  →  {img}')

print(f'\nDone — {ok}/{len(PAGES)} pages tagged.')
