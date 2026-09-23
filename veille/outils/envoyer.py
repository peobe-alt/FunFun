#!/usr/bin/env python3
"""Envoie l'e-mail de La FunVeille : une annonce courte avec le lien vers la page.

  python3 veille/outils/envoyer.py <numero> --apercu <fichier.html>
      Écrit l'e-mail dans un fichier HTML, sans rien envoyer.

  python3 veille/outils/envoyer.py <numero> --test
      Envoie l'e-mail à l'expéditeur seulement, pour vérifier le rendu.

  python3 veille/outils/envoyer.py <numero>
      Envoie l'e-mail à tous les destinataires (en copie cachée) et note
      l'envoi dans veille/envois.json. Refuse de renvoyer un numéro déjà envoyé.

Variables d'environnement (réglages de l'environnement cloud) :
  BREVO_API_KEY            clé API Brevo (SMTP et API > Clés API)
  FUNVEILLE_EXPEDITEUR     adresse d'expédition, validée dans Brevo (Expéditeurs)
  FUNVEILLE_DESTINATAIRES  adresses des lecteurs, séparées par des virgules
"""
import datetime
import html
import json
import os
import sys
import urllib.error
import urllib.request

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = os.path.join(RACINE, "site")
PAGE = "https://veilleff.netlify.app/"
JOURNAL = os.path.join(RACINE, "envois.json")

BP, BX, CORAL, CANARD, AQUA, EAU, SNOW = "#361E1C", "#733635", "#FF6038", "#11363E", "#A0C9CB", "#EBECDC", "#F6F5ED"
SERIF = "Georgia, 'Times New Roman', serif"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"


def e(s):
    return html.escape(str(s or ""), quote=True)


def pad(n):
    return "%02d" % int(n)


def label(txt, color=BX):
    return ('<div style="font-family:%s;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:%s;margin:0 0 6px;">%s</div>'
            % (SANS, color, e(txt)))


def construire(n):
    num = pad(n["numero"])
    lien = "%s#n%d" % (PAGE, int(n["numero"]))
    ed = n.get("fil_rouge", {})
    ins = n.get("inspiration", {})
    t = ins.get("tendance", {})
    m = n.get("marche", {})
    l = n.get("legal", {})
    sp = n.get("note_spirituelle", {})
    cov = n.get("couverture", {})

    sujets = [("01", "Inspiration", ins.get("sommaire") or t.get("nom")),
              ("02", "Marché", m.get("sommaire") or m.get("titre")),
              ("03", "Juridique", l.get("sommaire") or l.get("titre"))]
    au_sommaire = "".join(
        '<tr><td valign="top" style="padding:12px 14px 12px 0;border-top:1px solid %s;font-family:%s;font-size:12px;letter-spacing:1px;color:%s;white-space:nowrap;">%s</td>'
        '<td style="padding:12px 0;border-top:1px solid %s;"><div style="font-family:%s;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:%s;">%s</div>'
        '<a href="%s" style="font-family:%s;font-size:18px;line-height:1.3;color:%s;text-decoration:none;">%s</a></td></tr>'
        % (BX, SANS, CORAL, no, BX, SANS, AQUA, e(rub), e(lien), SERIF, SNOW, e(txt))
        for no, rub, txt in sujets if txt)

    sujet = "La FunVeille #%s · %s" % (num, ed.get("titre", t.get("nom", "")))
    accroche = ed.get("tension") or t.get("accroche", "")

    corps = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><title>%(sujet)s</title></head>
<body style="margin:0;padding:0;background:%(snow)s;">
<div style="display:none;max-height:0;overflow:hidden;">%(preheader)s</div>
<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%(snow)s;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="width:100%%;max-width:560px;">
<tr><td style="background:%(bp)s;padding:30px 32px 34px;border-radius:18px;">
  <div style="font-family:%(sans)s;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:%(eau)s;">Semaine %(semaine)s · %(date)s</div>
  <div style="font-family:%(sans)s;font-size:42px;line-height:1;font-weight:bold;letter-spacing:-1.5px;color:%(snow)s;margin-top:16px;">
    <span style="font-family:%(serif)s;font-style:italic;font-weight:normal;color:%(coral)s;">La</span> FunVeille<span style="font-size:17px;color:%(coral)s;vertical-align:top;"> #%(num)s</span></div>
  <p style="font-family:%(serif)s;font-size:20px;line-height:1.35;color:%(snow)s;margin:22px 0 26px;">Le numéro de la semaine est en ligne : <em style="color:%(eau)s;">%(ed_titre)s</em>.<br><span style="font-size:16px;color:%(eau)s;">%(preheader)s</span></p>
  <div style="font-family:%(sans)s;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:%(coral)s;margin:0 0 4px;">Au sommaire</div>
  <table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="margin:0 0 28px;">%(au_sommaire)s</table>
  <a href="%(lien)s" style="display:inline-block;background:%(coral)s;color:%(bp)s;font-family:%(sans)s;font-size:14px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;text-decoration:none;padding:15px 26px;border-radius:999px;">Ouvrir La FunVeille</a>
</td></tr>
<tr><td style="padding:16px 8px;font-family:%(sans)s;font-size:11px;line-height:1.6;color:#7A6A66;">La FunVeille, la veille hebdomadaire du projet FunFun.</td></tr>
</table></td></tr></table></body></html>""" % {
        "sujet": e(sujet), "preheader": e(accroche), "snow": SNOW, "bp": BP, "coral": CORAL, "eau": EAU, "sans": SANS, "serif": SERIF,
        "semaine": e(n.get("semaine")), "date": e(n.get("date_label")), "num": num, "ed_titre": e(ed.get("titre")), "lien": e(lien),
        "au_sommaire": au_sommaire,
    }
    return sujet, corps


def envoyer(sujet, corps, a, bcc):
    cle = os.environ.get("BREVO_API_KEY")
    exp = os.environ.get("FUNVEILLE_EXPEDITEUR")
    if not cle or not exp:
        print("Envoi impossible : BREVO_API_KEY et FUNVEILLE_EXPEDITEUR doivent être définis dans l'environnement.")
        sys.exit(2)
    payload = {"sender": {"name": "La FunVeille", "email": exp}, "to": [{"email": a}], "subject": sujet, "htmlContent": corps}
    if bcc:
        payload["bcc"] = [{"email": x} for x in bcc]
    req = urllib.request.Request("https://api.brevo.com/v3/smtp/email", data=json.dumps(payload).encode("utf-8"),
                                 headers={"api-key": cle, "content-type": "application/json", "accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        print("Brevo a refusé l'envoi (%s) : %s" % (err.code, err.read().decode("utf-8", "replace")))
        sys.exit(3)


def main(args):
    if not args or not args[0].isdigit():
        print(__doc__)
        return 1
    num = int(args[0])
    n = json.load(open(os.path.join(SITE, "numeros", "n%02d.json" % num), encoding="utf-8"))
    sujet, corps = construire(n)
    if "--apercu" in args:
        out = args[args.index("--apercu") + 1]
        open(out, "w", encoding="utf-8").write(corps)
        print("Aperçu écrit : %s (sujet : %s)" % (out, sujet))
        return 0
    exp = os.environ.get("FUNVEILLE_EXPEDITEUR", "")
    if "--test" in args:
        code, rep = envoyer("[Test] " + sujet, corps, exp, [])
        print("Test envoyé à l'expéditeur (%s) : %s" % (code, rep))
        return 0
    journal = json.load(open(JOURNAL, encoding="utf-8")) if os.path.isfile(JOURNAL) else {"envois": []}
    if any(x.get("numero") == num for x in journal["envois"]):
        print("Le numéro %d a déjà été envoyé : rien n'est renvoyé." % num)
        return 0
    dest = [x.strip() for x in os.environ.get("FUNVEILLE_DESTINATAIRES", "").split(",") if x.strip()]
    if not dest:
        print("Envoi impossible : FUNVEILLE_DESTINATAIRES est vide.")
        return 2
    code, rep = envoyer(sujet, corps, exp, dest)
    journal["envois"].append({"numero": num, "date": datetime.date.today().isoformat(), "destinataires": len(dest), "reponse": code})
    json.dump(journal, open(JOURNAL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Numéro %d envoyé à %d destinataires (%s)." % (num, len(dest), code))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
