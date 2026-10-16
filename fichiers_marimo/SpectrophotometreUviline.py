import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
    <style>
      html, body, .App { font-family: 'TeX Gyre Pagella', 'STIX Two Text', 'Palatino Linotype', Georgia, serif !important; font-size: 17px; line-height: 1.6; }
      button { white-space: normal !important; height: auto !important; min-height: 2.2em; }
      .markdown { font-family: inherit !important; color: #232b33 !important; }
      .markdown h1 { font-size: 2.05em; font-weight: 700; letter-spacing: 0.5px; color: #0f2b46; border-bottom: 3px solid #2e5e8c; padding-bottom: 0.35em; margin-bottom: 0.5em; }
      .markdown h2 { color: #1f4a70; border-bottom: 1px solid #b9cbd9; padding-bottom: 0.2em; }
      .markdown strong { color: #17405f; }
      .markdown code { font-family: 'DejaVu Sans Mono', 'Fira Code', monospace; font-size: 0.8em; font-weight: 600; color: #14304e; background: #edf1f6; border: 1px solid #ccd9e6; border-radius: 4px; padding: 1px 6px; }
      .panneau { background: #fcfdfe; border: 1px solid #d5e0ea; border-left: 5px solid #2e5e8c; border-radius: 10px; padding: 16px 20px; margin: 16px 0; box-shadow: 0 2px 8px rgba(15, 43, 70, 0.07); }
      .panneau-titre { font-variant: small-caps; font-weight: 700; font-size: 1.15em; letter-spacing: 1px; color: #1f4a70; margin-bottom: 8px; border-bottom: 1px dotted #9db3c6; padding-bottom: 5px; }
      .ligne { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin: 10px 0; }
      .etat { margin: 8px 0; font-style: italic; color: #2e4156; }
      .resultat { font-size: 1.02rem; line-height: 1.7; color: #333333; }
      .grande { font-weight: 800; color: #10213e; }
      body[data-theme='dark'] .markdown { color: #d7e1ea !important; }
      body[data-theme='dark'] .markdown h1 { color: #a8c8e6; border-color: #3f6a94; }
      body[data-theme='dark'] .markdown h2 { color: #9fc1e0; border-color: #3a5066; }
      body[data-theme='dark'] .markdown strong { color: #9fc1e0; }
      body[data-theme='dark'] .markdown code { color: #dbe9f7; background: #1f2c3a; border-color: #32465a; }
      body[data-theme='dark'] .panneau { background: #151f2a; border-color: #2b3d4e; box-shadow: none; }
      body[data-theme='dark'] .panneau-titre { color: #9fc1e0; border-color: #3a5066; }
      body[data-theme='dark'] .etat { color: #b7c7d6; }
      body[data-theme='dark'] .resultat { color: #d7e1ea; }
      body[data-theme='dark'] .grande { color: #a8c8e6; }
    </style>
    """
    )
    return


@app.cell(hide_code=True)
def _():
    import os
    import re
    from time import time

    import plotly.graph_objects as go
    from numpy import arange, zeros
    from plotly.subplots import make_subplots
    from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial

    from Import_bibliotheques import tableurVersVariables

    # Chemin du dossier du notebook marimo (repli : répertoire courant).
    def dossier_notebook():
        try:
            return os.path.dirname(os.path.abspath(__file__))
        except (NameError, AttributeError):
            return os.getcwd()

    # Chemin d'un CSV (par ex. un spectre) dans le dossier du notebook.
    def chemin_csv(nom_fichier):
        return os.path.join(dossier_notebook(), nom_fichier)

    # Mémorisation d'une courbe dans l'état partagé. Si le même nom est
    # re-saisi, sa courbe précédente est remplacée (comme dans l'original).
    def enregistrer_courbe(etat, colorant, tableau):
        etat["courbes"] = [c for c in etat["courbes"] if c["name"] != colorant]
        etat["courbes"].append({
            "name": colorant,
            "x": list(tableau["longueurs_ondes"]),
            "y": list(tableau["A"]),
        })

    # Création/config du port série (réglages fixes, identiques à l'original).
    # On retourne un objet NON ouvert : son ouverture est gérée une seule fois
    # par la cellule d'acquisition (port persistant dans l'état partagé).
    def ouvrir_port():
        s = Serial()
        s.port = "/dev/ttyUSB0"
        s.baudrate = 19200
        s.bytesize = EIGHTBITS
        s.stopbits = STOPBITS_ONE
        s.parity = PARITY_NONE
        s.timeout = 2            # temps d'attente (en s) des données du spectrophotomètre
        s.xonxoff = False     # disable software flow control
        s.rtscts = False     # disable hardware (RTS/CTS) flow control
        s.dsrdtr = False       # disable hardware (DSR/DTR) flow control
        s.writeTimeout = 2     # timeout for write
        return s

    # Acquisition d'un spectre depuis le spectrophotomètre. Réglages fixes du
    # port (identiques au notebook d'origine). Reçoit un port série DÉJÀ OUVERT
    # (persistant : ouvert une fois, réutilisé). Le buffer est vidé APRÈS chaque
    # acquisition (quand le spectro est silencieux), jamais AVANT la lecture :
    # ainsi, quand on lit, on part du vrai début de la salve (sinon le reset
    # jetterait les premières longueurs d'onde déjà émises).
    def acquerir_spectre(s, tps):
        donnees = ""
        precedente = None    # dernière longueur d'onde lue (pour détecter la fin d'un balayage)
        fin = tps() + 10    # durée maximale d'attente (en s)
        while tps() < fin:
            ligne = s.readline()
            if ligne:
                texte = ligne.decode("utf8", errors="ignore")
                texte = re.sub(r"[^0-9.,\-\s]", "", texte)    # chiffres, points, virgules, signes, espaces
                texte = re.sub(r"[\t ]+", ",", texte)          # tabulations / espaces -> virgule (séparateur)
                texte = texte.replace("\r", "").strip()
                champs = texte.split(",")
                if len(champs) == 2:    # ligne de mesure : longueur d'onde, valeur
                    try:
                        lo = float(champs[0])
                        if 300 <= lo <= 1100:    # longueur d'onde plausible (nm)
                            # Un retour en arrière des longueurs d'onde (ex. 800 puis 400)
                            # signale le début de la salve suivante : on arrête pour ne
                            # conserver qu'une seule salve complète.
                            if precedente is not None and lo < precedente:
                                break
                            donnees += texte + "\n"
                            precedente = lo
                            fin = tps() + 1    # 1 s de silence -> acquisition terminée
                    except ValueError:
                        pass
        # Nettoyage APRÈS acquisition (spectro silencieux) : vide les éventuels
        # restes pour que la prochaine lecture parte d'un buffer propre.
        try:
            s.reset_input_buffer()
        except Exception:
            pass
        return donnees

    return (
        EIGHTBITS,
        PARITY_NONE,
        STOPBITS_ONE,
        Serial,
        acquerir_spectre,
        arange,
        chemin_csv,
        go,
        make_subplots,
        os,
        ouvrir_port,
        re,
        tableurVersVariables,
        time,
        zeros,
        enregistrer_courbe,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    # Spectre UV visible — Spectrophotomètre

    Acquisition des spectres envoyés par le spectrophotomètre sur le port série `/dev/ttyUSB0` (19200 bauds). Chaque spectre est enregistré dans `Spectres/<nom>.csv` et ajouté au graphique.

    ### Déroulement

    1. **Saisir un nom** de colorant, puis cliquer sur **« Acquérir le spectre »**.
    2. **Déclencher l'envoi** sur l'appareil **aussitôt après** le clic (délai max. 1 à 2 s).
    3. Répéter pour superposer plusieurs spectres.

    **Lecture sauvegardée** : sans spectrophotomètre, activer « Lecture sauvegardée » pour re-lire les spectres déjà enregistrés dans `Spectres/`.
    """
    )
    return


@app.cell(hide_code=True)
def _():
    # État partagé persistant entre les cellules : accumulateur des spectres
    # mesurés, conservé en mémoire pendant toute la session.
    etat_spectres = {
        "clics": 0,
        "courbes": [],        # liste de dicts {"name", "x", "y"}
        "message": "Saisir un nom puis cliquer sur « Acquérir le spectre ».",
        "nom_saisi": "",
        "port": None,         # port série persistant (ouvert une seule fois)
    }
    return (etat_spectres,)


@app.cell(hide_code=True)
def _(etat_spectres, mo):
    # Champ nom + bouton d'acquisition + bascule lecture sauvegardée. Le nom saisi est
    # recopié dans l'état persistant via on_change (marimo ne synchronise pas
    # la valeur Python en direct) pour être lu au moment du clic.
    def _memoriser_nom(valeur):
        etat_spectres["nom_saisi"] = valeur

    champ_nom = mo.ui.text(
        value=etat_spectres.get("nom_saisi", ""),
        on_change=_memoriser_nom,
        label="Nom du spectre (colorant) :",
        placeholder="ex. Bleu patenté",
        full_width=False,
    )
    acquerir = mo.ui.button(
        value=etat_spectres["clics"],
        on_click=lambda valeur: valeur + 1,
        label="Acquérir le spectre",
        kind="neutral",
    )
    mode_lecture = mo.ui.switch(value=False, label="Lecture sauvegardée (relire un spectre déjà enregistré)")
    zone_saisie = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Acquisition d'un spectre</div>"
        f"<div class='ligne'>{champ_nom} {acquerir}</div>"
        f"<div class='ligne'>{mode_lecture}</div>"
        "</div>"
    )
    zone_saisie
    return acquerir, champ_nom, mode_lecture


@app.cell(hide_code=True)
def _(
    acquerir,
    acquerir_spectre,
    champ_nom,
    chemin_csv,
    etat_spectres,
    enregistrer_courbe,
    mode_lecture,
    os,
    ouvrir_port,
    tableurVersVariables,
    time,
):
    # Traitement d'un clic « Acquérir » : collecte des données du spectro (ou
    # relecture d'un spectre sauvegardé), enregistrement et ajout de la courbe.
    _etat = etat_spectres

    if acquerir.value != _etat["clics"]:
        _etat["clics"] = acquerir.value
        colorant = str(_etat.get("nom_saisi", "")).strip()
        if colorant == "":
            # Valider sans saisir de nom met fin aux enregistrements.
            _etat["message"] = "Aucun nom saisi : fin des enregistrements."
        else:
            dossier = os.path.dirname(chemin_csv("."))
            os.makedirs(os.path.join(dossier, "Spectres"), exist_ok=True)
            fichier = chemin_csv(f"Spectres/{colorant}.csv")

            if mode_lecture.value:    # relecture d'un spectre sauvegardé (sans spectrophotomètre)
                if not os.path.exists(fichier):
                    _etat["message"] = (
                        f"Fichier {fichier} introuvable : placer un spectre sauvegardé dans Spectres/."
                    )
                else:
                    _etat["message"] = f"Lecture sauvegardée : {fichier}"
                    tableau = tableurVersVariables(fichier)
                    enregistrer_courbe(_etat, colorant, tableau)
            else:
                # Port série persistant : ouvert une seule fois puis réutilisé.
                # Le buffer est vidé APRÈS chaque acquisition (dans
                # acquerir_spectre), jamais AVANT la lecture, pour partir du
                # début de la salve et ne rien perdre en tête du spectre.
                if _etat["port"] is None:
                    port = ouvrir_port()
                    if not port.is_open:
                        port.open()
                    _etat["port"] = port
                # Collecte jusqu'à 1 s de silence : l'utilisateur déclenche
                # L'ENVOI sur l'appareil, puis clique « Acquérir ».
                _etat["message"] = "Acquisition en cours… (déclencher l'envoi sur l'appareil)"
                donnees = acquerir_spectre(_etat["port"], time)
                if not donnees.strip():    # aucune donnée reçue (mesure non déclenchée)
                    _etat["message"] = (
                        f"Aucune donnée reçue pour {colorant} : vérifier le déclenchement de la mesure."
                    )
                else:
                    # Ligne d'en-tête puis données ; l'en-tête du spectro est
                    # éliminé par la validation des longueurs d'onde.
                    with open(fichier, "w") as f:
                        f.write("longueurs_ondes,A\n" + donnees)
                    tableau = tableurVersVariables(fichier)
                    _etat["message"] = f"{len(tableau['longueurs_ondes'])} points enregistrés pour {colorant}"
                    enregistrer_courbe(_etat, colorant, tableau)

    # etat_spectres["courbes"] est réassigné à une NOUVELLE liste à chaque
    # courbe ajoutée → l'objet renvoyé change d'identité et provoque la
    # re-exécution des cellules de tracé et de statut qui en dépendent.
    message = _etat["message"]
    courbes = _etat["courbes"]
    return courbes, message


@app.cell(hide_code=True)
def _(mo, zeros, arange, go, make_subplots, courbes):
    # Graphique à deux volets : courbes des spectres (en haut), bandeau de
    # couleurs (en bas). Reconstruit à chaque modification de l'état partagé.
    def couleurs_spectre(l):
        if l < 380 or l > 780:
            return (0, 0, 0)
        if l < 440:
            r, g, b = (440 - l) / 60, 0.0, 1.0
        elif l < 490:
            r, g, b = 0.0, (l - 440) / 50, 1.0
        elif l < 510:
            r, g, b = 0.0, 1.0, (510 - l) / 20
        elif l < 580:
            r, g, b = (l - 510) / 70, 1.0, 0.0
        elif l < 645:
            r, g, b = 1.0, (645 - l) / 65, 0.0
        else:
            r, g, b = 1.0, 0.0, 0.0
        if l < 420:
            f = 0.3 + 0.7 * (l - 380) / 40
        elif l > 700:
            f = 0.3 + 0.7 * (760 - l) / 60
        else:
            f = 1.0
        # les composantes sont déjà dans [0, 1], donc <= 255 après multiplication par 255
        return (int(f * r * 255), int(f * g * 255), int(f * b * 255))

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.92, 0.08], vertical_spacing=0.02,
    )

    # Bandeau coloré : couleurs réelles du spectre visible (conversion λ → RGB) :
    longueurs = arange(350, 750, 1)
    couleurs = [f"rgb({r},{g},{b})" for r, g, b in (couleurs_spectre(int(l)) for l in longueurs)]
    fig.add_trace(go.Scatter(
        x=longueurs, y=zeros(len(longueurs)), mode="markers",
        marker=dict(color=couleurs, size=24, symbol="square"),
        showlegend=False, hoverinfo="skip",
    ), row=2, col=1)    # bandeau sous l'axe des abscisses
    fig.update_yaxes(showticklabels=False, showgrid=False, row=2, col=1)
    fig.update_xaxes(title="Longueur d'onde (nm)", row=2, col=1)

    # Courbes des spectres mesurés, par-dessus les précédents :
    for courbe in courbes:
        fig.add_trace(go.Scatter(
            x=courbe["x"], y=courbe["y"], mode="lines", name=courbe["name"],
            line=dict(width=2),
        ), row=1, col=1)

    # Réglage du graphique :
    #fig.update_yaxes(scaleanchor="x", scaleratio=1, row=1, col=1)    # à décommenter pour un repère orthonormé
    fig.update_xaxes(showgrid=True, row=2, col=1)    # grille verticale (par défaut)
    fig.update_yaxes(showgrid=True, row=1, col=1)    # grille horizontale (par défaut)
    fig.update_layout(
        showlegend=True,    # légende du graphique
        title="Spectre UV visible",    # mettre le titre désiré entre les guillemets
        yaxis_title="Absorbance",    # nom de l'axe des ordonnées
        height=600)    # hauteur du graphique en pixels ; ex. : 450, 700...

    graf = mo.ui.plotly(fig)
    graf
    return (graf,)


@app.cell(hide_code=True)
def _(message, courbes, mo):
    # Statut de l'acquisition : dernier message et liste des spectres tracés.
    _noms = [c["name"] for c in courbes]
    if _noms:
        _chaine = " · ".join(_noms)
    else:
        _chaine = "aucun spectre pour l'instant"
    statut = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Suivi des spectres</div>"
        f"<div class='etat'>{message}</div>"
        f"<div class='resultat'>Spectres tracés : <span class='grande'>{_chaine}</span></div>"
        "</div>"
    )
    statut
    return (statut,)


if __name__ == "__main__":
    app.run()
