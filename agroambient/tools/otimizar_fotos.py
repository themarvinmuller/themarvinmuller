#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera versões leves (WebP em 480, 800 e 1280 px) das fotos de static/fotos e o arquivo static/fotos/tamanhos.json.

Rode sempre que adicionar ou trocar uma foto:  python3 tools/otimizar_fotos.py
Precisa do Pillow (pip install pillow) só na sua máquina; o build da Vercel não usa este script.
"""
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FOTOS = ROOT / "static" / "fotos"
OUT = FOTOS / "w"
WIDTHS = (480, 800, 1280)


def main():
    OUT.mkdir(exist_ok=True)
    sizes = {}
    for f in sorted(FOTOS.glob("*.jpg")):
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        w, h = im.size
        variants = []
        for tw in WIDTHS:
            if tw > w and variants:
                break
            tw = min(tw, w)
            th = round(h * tw / w)
            dest = OUT / ("%s-%d.webp" % (f.stem, tw))
            im.resize((tw, th), Image.LANCZOS).save(dest, "WEBP", quality=72, method=6)
            variants.append(tw)
        sizes[f.name] = {"w": w, "h": h, "webp": variants}
    (FOTOS / "tamanhos.json").write_text(json.dumps(sizes, indent=1) + "\n", encoding="utf-8")

    # Logo em tamanho de exibição (44 px, 88 px para telas retina)
    logo = Image.open(ROOT / "static" / "logo-agroambient.png").convert("RGBA")
    logo.resize((88, 88), Image.LANCZOS).save(ROOT / "static" / "logo-88.png", optimize=True)
    logo.resize((88, 88), Image.LANCZOS).save(ROOT / "static" / "logo-88.webp", "WEBP", quality=85)
    print("%d fotos otimizadas em %s" % (len(sizes), OUT))


if __name__ == "__main__":
    main()
