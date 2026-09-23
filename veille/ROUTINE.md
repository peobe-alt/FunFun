# La FunVeille : mode d'emploi de la routine hebdomadaire

Ce fichier est lu par la routine chaque lundi à 8 h 15 (heure de Paris). Il décrit, dans l'ordre, comment produire et publier un nouveau numéro. Le numéro 1 (`veille/site/numeros/n01.json`) sert de modèle de référence pour le ton, la longueur et la structure.

Règle d'écriture absolue : n'utiliser **jamais** le tiret cadratin (caractère Unicode U+2014) ni le tiret demi-cadratin (U+2013). Les remplacer par une virgule, deux-points ou des parenthèses. Le script de vérification les détecte.

## Repères

| Élément | Valeur |
| --- | --- |
| Dépôt | `peobe-alt/FunFun` |
| Branche | `claude/funfun-plaques-funeraires-5sjxbx` (branche par défaut) |
| Page publiée | https://claude.ai/artifact/GjJtYLJvA6AaNui3kNTVSK |
| Gabarit (ne pas modifier sans demande) | `veille/site/index.html` |
| Numéros | `veille/site/numeros/nXX.json` et images dans `veille/site/numeros/nXX/` |
| Liste des numéros | `veille/site/numeros/index.json` |
| Registre anti-répétition | `veille/registre.json` |
| Outils | `veille/outils/images.py`, `veille/outils/verifier.py`, `veille/outils/envoyer.py` |
| Contexte projet | `README.md` et tout le dossier `docs/` (étude de marché, règlements de cimetières...) |

## 1. Préparer

1. Se placer sur la branche, à jour : `git fetch origin claude/funfun-plaques-funeraires-5sjxbx && git checkout claude/funfun-plaques-funeraires-5sjxbx && git pull`.
2. Installer Pillow si besoin : `pip install -q pillow`.
3. Lire `README.md` et les documents de `docs/` pour le contexte FunFun (plaques funéraires et objets de mémoire, design formel et sensoriel).
4. Lire `veille/registre.json` en entier : tout ce qui y figure est **interdit** cette semaine, sauf fait nouveau.
5. Lire le dernier numéro publié pour garder le même niveau d'exigence.
6. Numéro du jour = dernier numéro de `numeros/index.json` + 1. Semaine ISO et date du jour (format « 28 septembre 2026 »).

## 2. Chercher

- Période : les 7 derniers jours en priorité, 30 jours au maximum. La note légale peut porter sur un texte plus ancien s'il n'a jamais été traité.
- Échelle : Europe d'abord. Un signal hors Europe est accepté s'il est vraiment fort pour FunFun.
- Langues : français, anglais, allemand, italien, espagnol, néerlandais.
- Sources fiables : presse design (Dezeen, Wallpaper*, Designboom, Frame, AD), presse économique, presse funéraire (Résonance Funéraire, Funeral Service Times, Bestattungskultur), sites officiels (Légifrance, EUR-Lex, Eurostat, Insee, Destatis), sites des marques.
- Chaque fait, chiffre ou citation doit être vérifié sur au moins une source consultée (pas seulement un résumé de recherche). Aucun chiffre ni citation inventé ou approximé sans le dire.

## 3. Écrire le numéro

Créer `veille/site/numeros/nXX.json` (XX sur deux chiffres) en reprenant **exactement** la structure de `n01.json`.

### La posture : écrire comme un planneur stratégique

La FunVeille n'est pas une revue de presse. C'est une lecture de la société à travers la mort, le deuil et la mémoire, écrite comme le ferait un planneur stratégique d'agence (référence de ton : « La TrendRoom du Planning » de Lonsdale). Chaque sujet suit la même mécanique :

1. **L'accroche** : une observation culturelle ou une question qui donne envie de lire (« Et si l'urne devenait la dernière pièce de design qu'on achète pour quelqu'un ? »).
2. **Le fait** : précis, daté, chiffré, sourcé. Qui, quoi, où, combien.
3. **Ce que ça révèle** : le déplacement de société derrière le fait (« le deuil entre dans le registre du goût »). C'est la partie la plus importante : sans elle, le sujet n'a pas sa place.
4. **La tension** : ce qui frotte. Un besoin contrarié, une contradiction entre ce que les gens font et ce que les institutions proposent.
5. **Le « et alors ? »** pour FunFun : concret, actionnable, jamais générique.

Règles de ton :
- **Gras** : dans chaque bloc de texte, mettre en gras (`**passage**`) un ou deux passages clés, jamais plus : le chiffre qui frappe, la phrase qui révèle. Le gras sert à lire en diagonale.
- Titres courts, avec une idée ou un jeu de mots, jamais descriptifs (« L'urne passe en galerie », « Les morts ne tiennent plus en place »).
- Phrases courtes, verbes forts, pas de jargon de consultant. Une chute avec de l'esprit est bienvenue.
- On parle de la mort : l'humour est tendre, jamais moqueur envers les personnes en deuil.
- Lentilles sociétales à mobiliser : rapport au temps, à l'intime, au corps, à la foi et à la sécularisation, aux générations, à la technologie, à l'écologie, à la solitude, aux inégalités, à la ville et aux lieux.
- Sources sociétales utiles : Ifop, Crédoc, SAF (ex-CSNAF), Insee, Eurostat, Fondapol, The Conversation, revues de sciences humaines (Mortality, Death Studies, Geographica Helvetica...), sociologues et anthropologues de la mort, presse culturelle.

### L'édito de la semaine (ouverture, champ `fil_rouge`)
- Un vrai édito de la rédaction. `titre` : une formule qui résume la semaine. `tension` : une phrase courte qui frappe. `texte` : 2 paragraphes qui relient les signaux de la semaine à un mouvement de société, avec au moins un chiffre sociétal sourcé. `sources`.

### Inspiration (lecture Nelly Rodi, profondeur de planneur)
- Une **tendance** nommée d'un mot ou deux, évocateur, jamais générique. `accroche` (une phrase forte).
- `tension` : la contradiction culturelle qui fait naître la tendance.
- `insight` : une vérité humaine formulée **à la première personne**, comme un planneur (« Je n'ai pas besoin d'un endroit où aller le voir. J'ai besoin d'une façon de le garder avec moi. »). La page précise qu'il est formulé par la rédaction : ne jamais le présenter comme une vraie citation.
- `lecture` : « Ce que ça dit de nous », 1 ou 2 paragraphes qui ancrent la tendance dans la société (chiffres, théorie, histoire), sourcés.
- Quatre focus, chacun avec **sa propre image** forte et inspirante (`image` : `src`, `alt`, `credit`), souvent un détail recadré dans une photo de la semaine :
  - `couleur` : nom poétique, code HEX **relevé sur une image de la semaine** (pas inventé), une phrase ;
  - `matiere` : une matière précise vue cette semaine, une phrase sensorielle ;
  - `forme` : une forme précise vue cette semaine, une phrase ;
  - `citation` : une citation **réelle et vérifiable**, avec son auteur et son contexte.
- 3 à 5 `mots_cles`.
- **4 signaux**, dont au moins un produit et au moins un service. Pour chacun : `id` (minuscules, tirets), `nom`, `url`, `lieu` (« Ville / date »), `type` (Produit, Service, Produit + service, Produit + plateforme...), `maturite` (1 émergent, 2 en diffusion, 3 installé), `rubrique` (un mot qui qualifie le signal : Objet d'auteur, Lumière, Institution, Service, Rituel, Numérique, Lieu, Matière...), `titre` (une idée, pas une description), `texte` (100 à 130 mots, suivant la mécanique accroche, fait, révélation), `pour_funfun`, `sources`, `image`.
- Un **signal faible** (`signal_faible`) : quelque chose de petit, de précoce ou d'étrange, encore peu visible, mais relié à un mouvement de fond (une recherche, une pratique marginale, une niche, un usage détourné, une initiative locale). `lien` (une phrase de transition qui rattache le signal à l'édito ou à la tendance de la semaine : le signal faible ne doit jamais arriver sans raison), `titre`, `lieu`, `texte` (le fait, précis), `pourquoi` (pourquoi ça pourrait compter demain, une phrase forte), `pour_funfun`, `sources`. Jamais une tendance déjà installée.

### Marché (lecture McKinsey)
- `titre` : la conclusion, pas le sujet. `accroche` : le « so what » en une phrase. `chapo` : le contexte chiffré.
- Une `figure` honnête, à l'échelle : `chaine` (chaîne de valeur), `empile` (barre empilée en %), ou `barres` (liste `{label, valeur, affiche, accent}`). Toujours une `note` de sources.
- 3 `constats`, chacun avec un chiffre. `lecture` : « Ce que les chiffres disent de nous », une ou deux phrases de lecture sociétale du marché. 3 `implications` pour FunFun (`gras` + `texte`). Un point `a_suivre`. `sources` avec liens.
- S'il n'y a pas d'actualité, approfondir un segment non encore traité (un pays, la crémation, les prix, l'assurance obsèques, les cimetières, les columbariums...) avec des chiffres datés et sourcés absents du registre.

### Note légale
- Un seul point de droit utile à FunFun, absent du registre et des documents de `docs/`. France en priorité, sinon un autre pays européen ou l'UE, avec la comparaison France si pertinent.
- `articles` : références exactes, citations mot pour mot. `listes` facultatives (`type` : `non`, `oui` ou `info`). `impact` : ce que ça change pour FunFun, et ce que ce droit dit de notre rapport aux morts. Sources officielles.

### Pour finir (note spirituelle)
- `note_spirituelle` : le numéro se termine par une note plus profonde sur le deuil, hors menu. Une citation **réelle, vérifiée sur la source d'origine** (texte, discours, livre, entretien), qui résonne avec l'édito de la semaine.
- Varier les horizons d'une semaine à l'autre : littérature, poésie, philosophie, anthropologie, psychologie du deuil, sagesses et spiritualités du monde entier, sans prosélytisme. Jamais deux fois le même auteur à moins de dix numéros d'écart (vérifier dans le registre).
- Champs : `citation` (sans guillemets, extrait exact ; signaler une coupe par « […] »), `auteur`, `contexte` (œuvre, date), `reflexion` (2 à 3 phrases de la rédaction qui relient la citation à la semaine et au projet FunFun), `source` (`titre`, `url`).

### Le reste
- `chiffres` : exactement 4 chiffres clés tirés du numéro, dont un chiffre de société (rubriques possibles : Marché, Société, Inspiration, Juridique). Chacun a sa `source` courte (« Ifop, 2023 »), affichée en bas du bloc.
- `couverture` : l'image la plus forte des signaux, avec `titre` et `ancre` (= `id` du signal).
- `mot_de_la_fin` : une phrase de clôture, légère, différente chaque semaine, affichée après la note spirituelle.
- `registre` : résumé par rubrique des sujets ajoutés.
- `maquette` : `false`.

## 4. Images

Chaque numéro a 9 images réelles : couverture, 4 images des focus de tendance (couleur, matière, forme, citation), 4 signaux. Jamais d'image générée.

1. Lister les images d'une page source : `python3 veille/outils/images.py candidats <url>`.
2. Télécharger et alléger : `python3 veille/outils/images.py telecharger <url_image> veille/site/numeros/nXX/<nom>.jpg 1400`.
3. **Ouvrir chaque image** pour vérifier qu'elle montre bien le sujet, qu'elle est nette et forte. Écarter logos, captures d'écran de site, bandeaux publicitaires.
4. Crédit systématique : « Photo : Marque · via Média ».
5. Images des focus de tendance : recadrer un détail parlant (la lumière, la texture, la silhouette, l'inscription) avec `python3 veille/outils/images.py recadrer <image> veille/site/numeros/nXX/q-<entrée>.jpg <gauche> <haut> <droite> <bas>`, après avoir ouvert l'image pour choisir le cadre.
6. Si une image arrive dans un format illisible (SVG enveloppant une image, par exemple), extraire l'image intégrée avec Pillow.
7. Relever le HEX de `couleur` sur l'une de ces images (moyenne d'une zone typique avec Pillow).

## 5. Registre anti-répétition

- Ajouter dans `veille/registre.json` une entrée par acteur, chiffre, texte, concept, signal faible et élément de tendance du numéro : `{"numero": XX, "rubrique": "societe|inspiration|marche|legal", "type": "acteur|chiffre|texte|concept|signal faible|tendance", "sujet": "..."}`.
- Un sujet déjà présent ne revient que s'il y a un fait nouveau : ajouter `"mise_a_jour": true` et commencer le texte concerné par « Mise à jour : ».
- Ajouter le numéro à `veille/site/numeros/index.json` : `{"numero", "fichier", "annee", "semaine", "date", "titre"}` (titre = nom de la tendance).

## 6. Vérifier

`python3 veille/outils/verifier.py XX` doit afficher « tout est bon ». Corriger jusqu'à ce que ce soit le cas.

Puis contrôler le rendu : servir `veille/site` en local (`npx --no-install http-server -p 8765 -s veille/site`) et faire une capture avec Playwright (Chromium est préinstallé) pour vérifier que les images s'affichent et que rien ne déborde.

## 7. Publier

1. `git add veille && git commit -m "La FunVeille, numéro XX : <tendance>"`, puis `git push -u origin claude/funfun-plaques-funeraires-5sjxbx`.
2. Mettre à jour la page publiée (outil Artifact) :
   - lister ses fichiers : action `list`, `scope: "files"`, `url` de la page ;
   - publier : `file_path` = `veille/site/index.html`, `url` = la page, `root` = racine du dépôt, `files` = les nouveaux fichiers et `numeros/index.json`, chacun sous son chemin publié (`numeros/...`) pointant vers `veille/site/numeros/...`.
3. Si l'outil Artifact n'est pas disponible, le dire clairement dans le message final : le numéro reste enregistré dans le dépôt.
4. Envoyer l'e-mail aux lecteurs : `python3 veille/outils/envoyer.py XX`. Le script lit `BREVO_API_KEY`, `FUNVEILLE_EXPEDITEUR` et `FUNVEILLE_DESTINATAIRES` dans l'environnement, envoie l'annonce du numéro avec le lien de la page, et note l'envoi dans `veille/envois.json` (il refuse de renvoyer un numéro déjà envoyé). Si une variable manque, le dire dans le message final. Puis commit et push de `veille/envois.json`.
5. Pour l'image de l'e-mail (facultative) : renseigner `couverture.image_email` avec l'adresse publique d'une photo JPG ou PNG de la source (jamais un fichier de la page, qui n'est pas public).

## 8. Message final

Quelques lignes : numéro, édito, tendance, les 4 signaux, le signal faible, le titre marché, la note légale, et le lien de la page.

## 9. Heure d'été et d'hiver

La routine est réglée en heure UTC. Si le décalage de Paris a changé (heure d'hiver fin octobre, heure d'été fin mars), mettre à jour son horaire pour rester à 8 h 15 à Paris : `15 7 * * 1` en heure d'hiver, `15 6 * * 1` en heure d'été (outil `update_trigger`, routine « La FunVeille »).
