import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    import os
    from time import sleep

    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go
    from numpy import gradient, linspace
    from scipy import interpolate

    from Arduino_lib import connexion_arduino, get_ser, lire_ligne, parse_ligne

    return (
        connexion_arduino,
        get_ser,
        go,
        gradient,
        interpolate,
        linspace,
        lire_ligne,
        mo,
        np,
        os,
        parse_ligne,
        sleep,
    )


@app.cell
def _(get_ser, lire_ligne, np, os, parse_ligne, sleep):
    # Réinitialisation de l'Arduino : bascule DTR (comme reset_arduino() du
    # notebook d'origine) — remet la carte dans un état propre avant mesure.
    def reset_arduino():
        ser = get_ser()
        ser.reset_input_buffer()
        ser.setDTR(False)
        sleep(0.1)
        ser.reset_input_buffer()
        ser.setDTR(True)

    # Mesure unique de tension de la sonde, débruitée par élimination des
    # valeurs aberrantes (méthode IQR) — identique à mesure_unique() d'origine.
    def mesurer_une_fois():
        ser = get_ser()
        while ser.in_waiting:
            ser.read(ser.in_waiting)
        tensions = []
        for _ in range(10):
            parse = parse_ligne(lire_ligne(ser))
            if parse is not None:
                tensions.append(parse[1])
        if len(tensions) == 0:
            raise Exception(
                "Aucune mesure reçue de l'Arduino : vérifier le câble USB et le "
                "programme acquisition_continue.ino."
            )
        q1 = np.percentile(tensions, 25)
        q3 = np.percentile(tensions, 75)
        ecart = q3 - q1
        borne_basse = q1 - 1.5 * ecart
        borne_haute = q3 + 1.5 * ecart
        tensions_propres = [v for v in tensions if borne_basse <= v <= borne_haute]
        return np.mean(tensions_propres)

    # Chemin du CSV dans le dossier du notebook marimo (repli : répertoire courant).
    def chemin_csv(nom_fichier):
        try:
            dossier = os.path.dirname(os.path.abspath(__file__))
        except (NameError, AttributeError):
            dossier = os.getcwd()
        return os.path.join(dossier, nom_fichier)

    # Écriture du fichier titragepH.csv (en-tête V,pH, comme dans l'original).
    def ecrire_csv_titrage(lignes):
        chemin = chemin_csv("titragepH.csv")
        with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write(
                "\n".join(",".join(str(v) for v in ligne) for ligne in lignes) + "\n"
            )

    return (
        reset_arduino,
        mesurer_une_fois,
        chemin_csv,
        ecrire_csv_titrage,
    )


@app.cell
def _(mo):
    # Typographie « publication scientifique » : TeX Gyre Pagella (dérivée de
    # Palatino, police classique des revues) avec replis serif, et habillage
    # des panneaux de mesure.
    style_global = mo.Html(
        "<style>"
        "html, body, .App {"
        "  font-family: 'TeX Gyre Pagella', 'STIX Two Text', 'Palatino Linotype', Georgia, serif !important;"
        "  font-size: 17px;"
        "  line-height: 1.6;"
        "}"
        ".markdown { font-family: inherit !important; color: #232b33 !important; }"
        ".markdown h1 {"
        "  font-size: 2.05em;"
        "  font-weight: 700;"
        "  letter-spacing: 0.5px;"
        "  color: #0f2b46;"
        "  border-bottom: 3px solid #2e5e8c;"
        "  padding-bottom: 0.35em;"
        "  margin-bottom: 0.5em;"
        "}"
        ".markdown h2 { color: #1f4a70; border-bottom: 1px solid #b9cbd9; padding-bottom: 0.2em; }"
        ".markdown strong { color: #17405f; }"
        ".markdown code {"
        "  font-family: 'DejaVu Sans Mono', 'Fira Code', monospace;"
        "  font-size: 0.8em;"
        "  font-weight: 600;"
        "  color: #14304e;"
        "  background: #edf1f6;"
        "  border: 1px solid #ccd9e6;"
        "  border-radius: 4px;"
        "  padding: 1px 6px;"
        "}"
        ".panneau {"
        "  background: #fcfdfe;"
        "  border: 1px solid #d5e0ea;"
        "  border-left: 5px solid #2e5e8c;"
        "  border-radius: 10px;"
        "  padding: 16px 20px;"
        "  margin: 16px 0;"
        "  box-shadow: 0 2px 8px rgba(15, 43, 70, 0.07);"
        "}"
        ".panneau-titre {"
        "  font-variant: small-caps;"
        "  font-weight: 700;"
        "  font-size: 1.15em;"
        "  letter-spacing: 1px;"
        "  color: #1f4a70;"
        "  margin-bottom: 8px;"
        "  border-bottom: 1px dotted #9db3c6;"
        "  padding-bottom: 5px;"
        "}"
        ".ligne { display: flex; flex-wrap: wrap; gap: 14px; align-items: center; margin: 10px 0; }"
        ".etat { margin: 8px 0; font-style: italic; color: #2e4156; }"
        "body[data-theme='dark'] .markdown { color: #d7e1ea !important; }"
        "body[data-theme='dark'] .markdown h1 { color: #a8c8e6; border-color: #3f6a94; }"
        "body[data-theme='dark'] .markdown h2 { color: #9fc1e0; border-color: #3a5066; }"
        "body[data-theme='dark'] .markdown strong { color: #9fc1e0; }"
        "body[data-theme='dark'] .markdown code { color: #dbe9f7; background: #1f2c3a; border-color: #32465a; }"
        "body[data-theme='dark'] .panneau { background: #151f2a; border-color: #2b3d4e; box-shadow: none; }"
        "body[data-theme='dark'] .panneau-titre { color: #9fc1e0; border-color: #3a5066; }"
        "body[data-theme='dark'] .etat { color: #b7c7d6; }"
        "</style>"
    )
    style_global
    return (style_global,)


@app.cell
def _(mo):
    mo.md(r"""
    # Titrage pH-métrique — Arduino

    **Protocole expérimental.** Relier la borne **Vout** du capteur de pH à la
    borne **A0** de la carte Arduino (programme `acquisition_continue.ino`).

    1. **Étalonner** la sonde avec les solutions tampons pH 7 puis pH 4 : les
       tensions mesurées déterminent la droite d'étalonnage pH = *a*·*U* + *b*.
    2. **Ajouter le titrant** par petites portions : saisir à chaque fois le
       volume versé (mL), puis cliquer sur « Mesurer le pH ».
    3. Chaque relevé est enregistré dans `titragepH.csv` et tracé en direct :
       points expérimentaux, courbe lissée et dérivée dpH/dV.

    **Vérifier la connexion** à la carte Arduino ci-dessous avant de commencer.
    """)
    return


@app.cell
def _(mo, connexion_arduino):
    # Connexion à la carte au chargement (reset DTR une seule fois) : toutes
    # les mesures (calibration et titrage) supposent le port série ouvert.
    try:
        message_connexion = connexion_arduino()
    except Exception as erreur:
        message_connexion = f"Arduino indisponible : {erreur}"
    presentation = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Connexion Arduino</div>"
        f"<div class='etat'>{message_connexion}</div>"
        "</div>"
    )
    presentation
    return (presentation,)


@app.cell(hide_code=True)
def _(mo):
    # État partagé persistant entre les cellules : conservé en mémoire pendant
    # toute la session (jamais recréé à chaque clic).
    donnees_titrage = {
        "valeurs": [["V", "pH"]],  # en-tête + relevés [volume, pH]
        "clics_etalon7": 0,
        "clics_etalon4": 0,
        "clics_mesure": 0,
        "clics_raz": 0,
        "volume_saisi": "",
        "message": "Étalonner d'abord aux pH 7 puis 4, ensuite ajouter les volumes.",
    }
    return (donnees_titrage,)


@app.cell(hide_code=True)
def _(donnees_titrage, mo):
    # Étalonnage : un bouton par solution tampon (création seule — la détection
    # du clic se fait dans une autre cellule, car marimo interdit de lire la
    # valeur d'un élément dans la cellule qui le crée).
    _etat = donnees_titrage

    etalon7 = mo.ui.button(
        value=_etat["clics_etalon7"],
        on_click=lambda valeur: valeur + 1,
        label="Étalonner à pH 7",
    )
    etalon4 = mo.ui.button(
        value=_etat["clics_etalon4"],
        on_click=lambda valeur: valeur + 1,
        label="Étalonner à pH 4",
    )
    return etalon4, etalon7


@app.cell(hide_code=True)
def _(donnees_titrage, etalon4, etalon7, mesurer_une_fois, mo, reset_arduino):
    # Détection des clics d'étalonnage : mesure la tension de la sonde (reset
    # puis lecture débruitée), puis calcule a et b de la droite pH = a.U + b —
    # mêmes formules que dans le notebook d'origine.
    _etat = donnees_titrage

    _statut = _etat["message"]
    if etalon7.value != _etat["clics_etalon7"]:
        _etat["clics_etalon7"] = etalon7.value
        reset_arduino()
        _etat["tension7"] = mesurer_une_fois()
        _statut = f"Tension mesurée à pH 7 : {_etat['tension7']:.3f} V."
    if etalon4.value != _etat["clics_etalon4"]:
        _etat["clics_etalon4"] = etalon4.value
        reset_arduino()
        _etat["tension4"] = mesurer_une_fois()
        _statut = f"Tension mesurée à pH 4 : {_etat['tension4']:.3f} V."
    if "tension7" in _etat and "tension4" in _etat and "a" not in _etat:
        # pH = a.U + b avec a = 3×(U7 − U4) et b = 7 − a·U7.
        _etat["a"] = 3.0 * (_etat["tension7"] - _etat["tension4"])
        _etat["b"] = 7.0 - _etat["a"] * _etat["tension7"]
        _statut = (
            f"Étalonnage OK : a = {_etat['a']:.3f} pH/V, b = {_etat['b']:.3f} "
            f"(U7 = {_etat['tension7']:.3f} V, U4 = {_etat['tension4']:.3f} V)."
        )

    affichage = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>1. Étalonnage de la sonde</div>"
        f"<div class='ligne'>{etalon7}{etalon4}</div>"
        f"<div class='etat'>{_statut}</div>"
        "</div>"
    )
    affichage
    return (affichage,)


@app.cell(hide_code=True)
def _(mo, donnees_titrage):
    # Réglages du titrage : champ volume + boutons Mesurer / Recommencer.
    _etat = donnees_titrage

    def _memoriser_volume(valeur):
        _etat["volume_saisi"] = valeur

    champ_volume = mo.ui.text(
        value=_etat["volume_saisi"],
        on_change=_memoriser_volume,
        label="Volume versé (mL) :",
        placeholder="ex. 2 ou 3,5",
        full_width=False,
    )
    b_mesurer = mo.ui.button(
        value=_etat["clics_mesure"],
        on_click=lambda valeur: valeur + 1,
        label="Mesurer le pH",
    )
    b_raz = mo.ui.button(
        value=_etat["clics_raz"],
        on_click=lambda valeur: valeur + 1,
        label="Recommencer",
    )
    zone_saisie = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Saisie du volume versé</div>"
        f"<div class='ligne'>{champ_volume}{b_mesurer}{b_raz}</div>"
        "</div>"
    )
    zone_saisie
    return b_mesurer, b_raz, champ_volume


@app.cell(hide_code=True)
def _(b_mesurer, b_raz, champ_volume, donnees_titrage, ecrire_csv_titrage, mesurer_une_fois, mo, reset_arduino):
    # Traitement d'un clic « Mesurer » : mesure Arduino, calcul du pH à partir
    # de l'étalonnage, ajout du point et mise à jour de titragepH.csv. Traitée
    # quand la valeur du bouton change (re-exécution de cette cellule).
    _etat = donnees_titrage

    if b_mesurer.value != _etat["clics_mesure"]:
        _etat["clics_mesure"] = b_mesurer.value
        saisie = str(_etat.get("volume_saisi", "")).strip().replace(",", ".")
        try:
            volume = float(saisie)
        except ValueError:
            _etat["message"] = "Volume invalide : saisir un nombre positif (ex. 2 ou 3,5)."
        else:
            if "a" not in _etat or "b" not in _etat:
                _etat["message"] = "Étalonner d'abord la sonde (pH 7 puis pH 4)."
            else:
                try:
                    reset_arduino()
                    tension = mesurer_une_fois()
                except Exception as erreur:
                    _etat["message"] = f"Erreur avec l'Arduino : {erreur}"
                else:
                    pH_actuel = _etat["a"] * tension + _etat["b"]
                    _etat["valeurs"].append([volume, pH_actuel])
                    ecrire_csv_titrage(_etat["valeurs"])
                    _etat["message"] = (
                        f"pH mesuré : {pH_actuel:.2f} pour {volume:.3g} mL — "
                        f"{len(_etat['valeurs']) - 1} relevé(s) enregistré(s)."
                    )

    if b_raz.value != _etat["clics_raz"]:
        _etat["clics_raz"] = b_raz.value
        _etat["valeurs"] = [["V", "pH"]]
        _etat["message"] = "Relevés remis à zéro."

    statut_titrage = mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>2. Relevés du titrage</div>"
        f"<div class='etat'>{_etat['message']}</div>"
        "</div>"
    )
    statut_titrage
    return (statut_titrage,)


@app.cell(hide_code=True)
def _(b_mesurer, b_raz, donnees_titrage, go, gradient, interpolate, linspace, mo, np):
    # Tracé temps réel : points mesurés, courbe lissée (spline s = 0.003) et
    # dérivée numérique dpH/dV normalisée — reproduit la cellule de l'original.
    _maj = b_mesurer.value + b_raz.value  # re-trace après chaque action

    _etat = donnees_titrage
    valeurs = _etat["valeurs"]
    if len(valeurs) < 2:
        resultat = mo.Html("<div class='etat'>En attente des premiers relevés…</div>")
    else:
        releves = [[float(ligne[0]), float(ligne[1])] for ligne in valeurs[1:]]
        V = np.array([r[0] for r in releves])
        pH = np.array([r[1] for r in releves])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=V, y=pH, mode="markers", name="pH mesurés",
            marker=dict(symbol="cross", size=10, color="blue"),
        ))
        # splrep (spline cubique) exige au moins 4 points : lissage et dérivée
        # seulement à partir du 4e relevé (avant : seuls les points sont tracés).
        if len(V) >= 4:
            tck = interpolate.splrep(V, pH, s=0.003)
            vecV = linspace(0, max(V), 1000)
            pH_lisse = interpolate.splev(vecV, tck)
            dervpH = gradient(pH_lisse) / gradient(vecV)
            dervpH = dervpH / max(dervpH) * 10
            fig.add_trace(go.Scatter(
                x=vecV, y=pH_lisse, mode="lines",
                name="courbe lissée de pH", line=dict(width=2),
            ))
            fig.add_trace(go.Scatter(
                x=vecV, y=dervpH, mode="lines", name="dpH/dV", line=dict(width=2),
            ))
        fig.update_layout(
            showlegend=True,
            title="Courbe de titrage",
            xaxis_title="Volume versé (mL)",
            yaxis_title="pH ; dpH/dV",
            height=600,
        )
        resultat = mo.ui.plotly(fig)

    resultat
    return (resultat,)