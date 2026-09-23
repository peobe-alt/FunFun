#!/usr/bin/env python3
"""Vérifie un numéro de La FunVeille avant publication.

  python3 veille/outils/verifier.py <numero>

Contrôle : structure du fichier du numéro, présence et poids des images,
entrée dans numeros/index.json, entrées du registre, doublons avec les
numéros précédents, et absence des tirets longs interdits.
Code de sortie 0 si tout est bon, 1 sinon.
"""
import json
import os
import re
import sys
import unicodedata

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = os.path.join(RACINE, "site")
POIDS_MAX = 450 * 1024

erreurs = []


def err(msg):
    erreurs.append(msg)


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def exige(obj, chemin, cles):
    for c in cles:
        if c not in obj or obj[c] in (None, "", []):
            err("Champ manquant : %s.%s" % (chemin, c))


def origine(obj, chemin):
    """Pays de l'information : liste de codes ISO à deux lettres (FR, DE, CH...), EU ou INT."""
    o = obj.get("origine") if isinstance(obj, dict) else None
    if not isinstance(o, list) or not o or not all(isinstance(c, str) and (re.fullmatch(r"[A-Z]{2}", c) or c == "INT") for c in o):
        err("%s.origine manquant ou invalide : liste de codes pays en majuscules, par exemple [\"FR\"] ou [\"DE\", \"CH\"]" % chemin)


def image(img, chemin):
    if not isinstance(img, dict):
        err("Image manquante : %s" % chemin)
        return
    exige(img, chemin, ["src", "alt", "credit"])
    src = img.get("src", "")
    f = os.path.join(SITE, src)
    if not os.path.isfile(f):
        err("Fichier image absent : %s (%s)" % (src, chemin))
    elif os.path.getsize(f) > POIDS_MAX:
        err("Image trop lourde (%d ko) : %s" % (os.path.getsize(f) // 1024, src))
    if "maquette" in img.get("credit", "").lower():
        err("Crédit de maquette restant : %s" % chemin)


def main(num):
    fichier = os.path.join(SITE, "numeros", "n%02d.json" % num)
    if not os.path.isfile(fichier):
        print("Introuvable : %s" % fichier)
        return 1
    brut = open(fichier, encoding="utf-8").read()
    if "\u2014" in brut or "\u2013" in brut:
        err("Tiret long ou demi-long présent dans le numéro : remplacer par une virgule, deux-points ou parenthèses")
    n = json.loads(brut)

    exige(n, "numero", ["numero", "annee", "semaine", "date", "date_label", "couverture", "chiffres", "fil_rouge", "inspiration", "marche", "legal", "note_spirituelle", "mot_de_la_fin", "registre"])
    exige(n.get("fil_rouge", {}), "fil_rouge", ["titre", "tension", "texte", "sources"])
    exige(n.get("note_spirituelle", {}), "note_spirituelle", ["citation", "auteur", "contexte", "reflexion", "source"])
    if n.get("numero") != num:
        err("Le champ numero (%s) ne correspond pas au fichier (%s)" % (n.get("numero"), num))
    c = n.get("couverture", {})
    exige(c, "couverture", ["image", "alt", "credit", "titre", "ancre"])
    image({"src": c.get("image"), "alt": c.get("alt"), "credit": c.get("credit")}, "couverture")
    if len(n.get("chiffres", [])) != 4:
        err("Il faut exactement 4 chiffres clés")
    for i, k in enumerate(n.get("chiffres", [])):
        exige(k, "chiffres[%d]" % i, ["rubrique", "valeur", "texte", "source", "source_url"])
        origine(k, "chiffres[%d]" % i)
    if brut.count("**") % 2:
        err("Un passage en gras (**...**) n'est pas refermé")

    ins = n.get("inspiration", {})
    exige(ins, "inspiration", ["tendance", "signaux"])
    t = ins.get("tendance", {})
    exige(t, "tendance", ["nom", "accroche", "tension", "insight", "lecture", "couleur", "matiere", "forme", "citation", "mots_cles"])
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", str(t.get("couleur", {}).get("hex", ""))):
        err("tendance.couleur.hex doit être un code HEX à 6 caractères")
    exige(t.get("citation", {}), "tendance.citation", ["texte", "auteur"])
    for k in ("couleur", "matiere", "forme", "citation"):
        image(t.get(k, {}).get("image"), "tendance.%s.image" % k)
    signaux = ins.get("signaux", [])
    if not 3 <= len(signaux) <= 5:
        err("Il faut 3 à 5 signaux d'inspiration (4 conseillés)")
    types = " ".join(s.get("type", "").lower() for s in signaux)
    if "produit" not in types or "service" not in types:
        err("Les signaux doivent couvrir au moins un produit et au moins un service")
    ids = [s.get("id") for s in signaux]
    if c.get("ancre") not in ids:
        err("couverture.ancre doit reprendre l'id d'un signal")
    for i, s in enumerate(signaux):
        exige(s, "signaux[%d]" % i, ["id", "nom", "url", "lieu", "type", "maturite", "rubrique", "titre", "texte", "pour_funfun", "sources", "image"])
        if s.get("maturite") not in (1, 2, 3):
            err("signaux[%d].maturite doit valoir 1, 2 ou 3" % i)
        image(s.get("image"), "signaux[%d].image" % i)
        origine(s, "signaux[%d]" % i)

    exige(ins.get("signal_faible", {}), "signal_faible", ["lien", "titre", "lieu", "texte", "pourquoi", "pour_funfun", "sources"])
    origine(ins.get("signal_faible", {}), "signal_faible")
    nb = len(ins.get("signal_faible", {}).get("texte", "").replace("**", "").split())
    if nb > 70:
        err("Le signal faible est une note : 40 à 60 mots (actuellement %d)" % nb)

    m = n.get("marche", {})
    exige(m, "marche", ["titre", "accroche", "chapo", "figure", "constats", "implications", "lecture", "sources"])
    f = m.get("figure", {})
    if not any(k in f for k in ("chaine", "empile", "barres")):
        err("marche.figure doit contenir chaine, empile ou barres")
    origine(m, "marche")
    if len(m.get("constats", [])) != 3:
        err("Il faut 3 constats de marché")

    l = n.get("legal", {})
    exige(l, "legal", ["pays", "titre", "articles", "impact", "sources"])
    origine(l, "legal")

    # Tout ce qui est cité a sa source, avec un lien externe
    def liens(lst, chemin):
        if not isinstance(lst, list) or not lst:
            err("Sources manquantes ou sans lien : %s (liste de {titre, url} attendue)" % chemin)
            return
        for j, x in enumerate(lst):
            if not isinstance(x, dict) or not str(x.get("url", "")).startswith("http") or not x.get("titre"):
                err("Source sans lien externe : %s[%d]" % (chemin, j))
    liens(n.get("fil_rouge", {}).get("sources"), "fil_rouge.sources")
    liens(t.get("sources"), "tendance.sources")
    for k in ("couleur", "matiere", "forme", "citation"):
        liens([t.get(k, {}).get("source")] if t.get(k, {}).get("source") else None, "tendance.%s.source" % k)
    for i, s in enumerate(signaux):
        liens(s.get("sources"), "signaux[%d].sources" % i)
    liens(ins.get("signal_faible", {}).get("sources"), "signal_faible.sources")
    liens(m.get("sources"), "marche.sources")
    liens(l.get("sources"), "legal.sources")
    for i, a in enumerate(l.get("articles", [])):
        if not str(a.get("url", "")).startswith("http"):
            err("Article de loi sans lien (Légifrance, EUR-Lex...) : legal.articles[%d]" % i)
    sp = n.get("note_spirituelle", {}).get("source", {})
    if not str(sp.get("url", "")).startswith("http"):
        err("La note spirituelle doit avoir un lien vers sa source")
    for u in re.findall(r'"(?:url|source_url)": "([^"]*)"', brut):
        if not u.startswith("http"):
            err("Lien invalide : %s" % u)

    idx = json.load(open(os.path.join(SITE, "numeros", "index.json"), encoding="utf-8"))
    if not any(e.get("numero") == num and e.get("fichier") == "numeros/n%02d.json" % num for e in idx.get("numeros", [])):
        err("Numéro absent de numeros/index.json")

    reg = json.load(open(os.path.join(RACINE, "registre.json"), encoding="utf-8"))
    anciens = {}
    for e in reg.get("entrees", []):
        if e.get("numero", 0) < num:
            anciens.setdefault(norm(e.get("sujet", "")), e.get("numero"))
    nouveaux = [e for e in reg.get("entrees", []) if e.get("numero") == num]
    if not nouveaux:
        err("Aucune entrée du registre pour ce numéro")
    for e in nouveaux:
        k = norm(e.get("sujet", ""))
        if k in anciens and not e.get("mise_a_jour"):
            err("Doublon avec le numéro %s : « %s » (ajouter \"mise_a_jour\": true seulement s'il y a un fait nouveau)" % (anciens[k], e.get("sujet")))

    if erreurs:
        print("À corriger (%d) :" % len(erreurs))
        for e in erreurs:
            print(" - " + e)
        return 1
    print("Numéro %d : tout est bon." % num)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print(__doc__)
        sys.exit(1)
    sys.exit(main(int(sys.argv[1])))
