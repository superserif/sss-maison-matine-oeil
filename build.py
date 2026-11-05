#!/usr/bin/env python3
"""Assemble index.html (fichier autonome) :
   src/page.html  + svg/illu-1.svg (frise du footer)
                  + œil construit depuis svg/illu-2.svg (pupille) et svg/illu-4.svg (amande + contour)
                  + vendor/lenis.min.js en ligne.
   Lancer : python3 build.py"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
q = lambda t: f'{{{NS}}}{t}'
SHAPES = {q('path'), q('polygon'), q('circle')}
ALMOND = ('M192.6,69.77s-24.42,26.81-54.54,26.81-54.54-26.81-54.54-26.81'
          'c0,0,24.42-26.81,54.54-26.81s54.54,22.69,54.54,26.81Z')

# --- frise : classes renommées (le <style> d'un SVG en ligne vaut pour toute la page)
illu = ET.parse(ROOT / 'svg/illu-1.svg').getroot()
for el in illu.iter():
    if el.tag == q('style'):
        el.text = el.text.replace('.cls-', '.mmi-')
    if el.get('class'):
        el.set('class', el.get('class').replace('cls-', 'mmi-'))
for k in ('id', 'data-name'):
    illu.attrib.pop(k, None)
illu.set('id', 'illu')
illu.set('role', 'group')
illu.set('aria-label', 'Maison Matine : une lampe-œil au milieu des nuages')
lamp = illu.find(q('g'))
beam, band, dome = list(lamp)
dome.set('id', 'dome')
# noms des éléments de la frise (recomposée en mobile par la page)
names = ['lamp', 'cloud-bl', 'cloud-tr', 'cloud-ml', 'cloud-br', 'cloud-tl', 'star-l', 'star-r', 'star-m', 'logo']
groups = [g for g in illu if g.tag == q('g')]
assert len(groups) == len(names), len(groups)
for g, name in zip(groups, names):
    g.set('id', name)

def shapes(name, keep=lambda el: True):
    root = ET.parse(ROOT / name).getroot()
    out = []
    for el in root.iter():
        if el.tag in SHAPES and keep(el):
            el.attrib.pop('class', None)
            out.append(el)
    return out

# --- l'œil (paupières en #000 comme le remplissage du dôme), dans le repère des fichiers 2 à 4 (placé sur le dôme par le script de la page)
# centre de la pupille relevé sur la capture du site : (965,5 ; 128,1) dans le repère de la frise
eye = ET.SubElement(illu, q('g'), {'id': 'eye', 'transform': 'translate(827.44 58.33)',
                                   'tabindex': '0', 'role': 'button',
                                   'aria-label': 'L’œil de la lampe : le toucher pour qu’il se ferme'})
defs = ET.SubElement(eye, q('defs'))
clip = ET.SubElement(defs, q('clipPath'), {'id': 'mm-almond'})
ET.SubElement(clip, q('path'), {'d': ALMOND})
ET.SubElement(eye, q('path'), {'d': ALMOND, 'fill': '#fff'})
inside = ET.SubElement(eye, q('g'), {'clip-path': 'url(#mm-almond)'})
pupil = ET.SubElement(inside, q('g'), {'id': 'pupil', 'fill': '#202020'})
pupil.extend(shapes('svg/illu-2.svg'))
pupil.find(q('circle')).set('fill', '#000')   # disque noir, bords irréguliers en #202020 comme le dessin
ET.SubElement(inside, q('path'), {'id': 'lid-top', 'fill': '#000', 'd': 'M60,20H216V69.77H60Z'})
ET.SubElement(inside, q('path'), {'id': 'lid-bot', 'fill': '#000', 'd': 'M60,120H216V120H60Z'})
outline = ET.SubElement(eye, q('g'), {'fill': '#202020'})
outline.extend(shapes('svg/illu-4.svg', keep=lambda el: el.get('class') != 'cls-1'))  # sans le blanc
ET.SubElement(eye, q('ellipse'), {'id': 'eye-ring', 'cx': '138.06', 'cy': '66', 'rx': '96', 'ry': '62',
                                  'fill': 'none', 'stroke': '#202020', 'stroke-width': '1.5',
                                  'stroke-dasharray': '4 5'})

svg = ET.tostring(illu, encoding='unicode')
page = (ROOT / 'src/page.html').read_text()
page = page.replace('<!--ILLU-->', svg).replace('<!--LENIS-->', (ROOT / 'vendor/lenis.min.js').read_text())
(ROOT / 'index.html').write_text(page)
print(f'index.html : {len(page) / 1024:.0f} Ko')
