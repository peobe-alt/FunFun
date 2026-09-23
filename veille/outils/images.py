#!/usr/bin/env python3
"""Outils d'images pour La FunVeille.

  python3 veille/outils/images.py candidats <url_de_la_page>
      Liste les images d'une page source : og:image, twitter:image, puis les
      <img> les plus grandes déclarées. À ouvrir ensuite pour choisir.

  python3 veille/outils/images.py telecharger <url_image> <destination.jpg> [largeur_max]
      Télécharge l'image, la convertit en JPEG léger (1600 px de large par
      défaut, qualité 82, sans métadonnées) et affiche son poids.

Dépendance : Pillow (pip install pillow).
"""
import html
import io
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def candidats(page):
    raw, _ = fetch(page)
    doc = raw.decode("utf-8", "replace")
    found = []

    def add(u, why):
        if not u:
            return
        u = urllib.parse.urljoin(page, html.unescape(u.strip()))
        if u.startswith("data:") or u in [f[0] for f in found]:
            return
        found.append((u, why))

    for prop in ("og:image", "og:image:url", "og:image:secure_url", "twitter:image", "twitter:image:src"):
        for m in re.finditer(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]*>' % re.escape(prop), doc, re.I):
            c = re.search(r'content=["\']([^"\']+)', m.group(0))
            if c:
                add(c.group(1), prop)
    imgs = []
    for m in re.finditer(r"<img[^>]+>", doc, re.I):
        tag = m.group(0)
        src = None
        srcset = re.search(r'(?:data-)?srcset=["\']([^"\']+)', tag)
        if srcset:
            parts = [p.strip().split(" ") for p in srcset.group(1).split(",") if p.strip()]
            best = max(parts, key=lambda p: int(re.sub(r"\D", "", p[1]) or 0) if len(p) > 1 else 0)
            src = best[0]
        if not src:
            s = re.search(r'(?:data-src|src)=["\']([^"\']+)', tag)
            src = s.group(1) if s else None
        w = re.search(r'width=["\']?(\d+)', tag)
        alt = re.search(r'alt=["\']([^"\']*)', tag)
        if src and not re.search(r"\.(svg|gif)(\?|$)|logo|icon|sprite|avatar", src, re.I):
            imgs.append((int(w.group(1)) if w else 0, src, alt.group(1) if alt else ""))
    for w, src, alt in sorted(imgs, key=lambda x: -x[0])[:15]:
        add(src, "img %spx %s" % (w or "?", alt[:60]))
    for u, why in found:
        print("%s\t%s" % (why, u))


def telecharger(url, dest, largeur=1600):
    from PIL import Image

    raw, ctype = fetch(url)
    im = Image.open(io.BytesIO(raw))
    im.load()
    if im.mode not in ("RGB", "L"):
        bg = Image.new("RGB", im.size, (246, 245, 237))
        rgba = im.convert("RGBA")
        bg.paste(rgba, mask=rgba.split()[-1])
        im = bg
    im = im.convert("RGB")
    if im.width > largeur:
        im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    import os
    if os.path.dirname(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    print("%s  %dx%d  %d ko" % (dest, im.width, im.height, os.path.getsize(dest) // 1024))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "candidats":
        candidats(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "telecharger":
        telecharger(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1600)
    else:
        print(__doc__)
        sys.exit(1)
