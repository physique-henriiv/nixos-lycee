import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html("""
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
    """)
    return


@app.cell(hide_code=True)
def _():
    from numpy import array, mean, sqrt, std

    from Arduino_lib import connexion_arduino, get_ser, lire_ligne, parse_ligne

    from Import_bibliotheques import go

    from time import sleep

    return (
        array,
        connexion_arduino,
        get_ser,
        go,
        lire_ligne,
        mean,
        parse_ligne,
        sleep,
        sqrt,
        std,
    )


@app.cell(hide_code=True)
def _(get_ser, sleep):
    import os

    # Réinitialisation de l'Arduino : bascule DTR (comme reset_arduino() du
    # notebook d'origine) — remet la carte dans un état propre avant mesure.
    def reset_arduino():
        ser = get_ser()
        ser.reset_input_buffer()
        ser.setDTR(False)
        sleep(0.1)
        ser.reset_input_buffer()
        ser.setDTR(True)

    # Chemin du CSV dans le dossier du notebook marimo (repli : répertoire courant).
    def chemin_csv(nom_fichier):
        try:
            dossier = os.path.dirname(os.path.abspath(__file__))
        except (NameError, AttributeError):
            dossier = os.getcwd()
        return os.path.join(dossier, nom_fichier)

    # Sauvegarde des tensions dans statistiques.csv (en-tête « tension », comme l'original).
    def sauvegarder_csv(liste_donnees):
        chemin = chemin_csv("statistiques.csv")
        with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write("tension\n" + "\n".join(map(str, liste_donnees)) + "\n")

    return (chemin_csv, reset_arduino, sauvegarder_csv)


@app.cell
def _(mo):
    mo.md(r"""
    # Statistiques d'une série de mesures — Arduino

    La carte Arduino émet en continu la tension mesurée sur la broche **A0** (programme `acquisition_continue.ino`, lignes `temps_us,tension` à 115 200 bauds).

    1. **Choisir le nombre de mesures** à effectuer, puis cliquer sur **« Démarrer l'acquisition »**.
    2. Les mesures sont lues sur le port série, puis sauvegardées dans `statistiques.csv`.
    3. La moyenne, l'écart-type et l'incertitude-type sont calculés, puis l'histogramme est tracé.

    **Vérifier la connexion** à la carte Arduino ci-dessous avant de commencer.
    """)
    return


@app.cell(hide_code=True)
def _(connexion_arduino, mo):
    # Connexion à la carte AU CHARGEMENT (reset DTR une seule fois) : toutes
    # les mesures supposent le port série ouvert. Si la carte est absente, un
    # message l'indique sans bloquer l'application.
    try:
        message_connexion = connexion_arduino()
    except Exception as erreur:
        message_connexion = f"Arduino indisponible : {erreur}"

    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Connexion Arduino</div>"
        f"<div class='etat'>{message_connexion}</div>"
        "</div>"
    )
    return (message_connexion,)


@app.cell(hide_code=True)
def _(mo):
    nb_mesures = mo.ui.number(
        value=100,
        start=1,
        stop=1_000_000,
        step=1,
        label="Nombre de mesures à effectuer",
    )
    demarrer = mo.ui.button(
        value=0,
        on_click=lambda valeur: valeur + 1,
        label="Démarrer l'acquisition",
    )
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Réglages de l'acquisition</div>"
        f"<div class='ligne'>{nb_mesures} {demarrer}</div>"
        "<div class='etat'>Cliquez sur « Démarrer l'acquisition » pour lancer la mesure.</div>"
        "</div>"
    )
    return (demarrer, nb_mesures)


@app.cell(hide_code=True)
def _():
    # État partagé persistant entre les cellules (jamais recréé à chaque clic).
    acquisition = {
        "clics": 0,
        "liste_donnees": [],
        "message": "Cliquez sur « Démarrer l'acquisition » pour commencer.",
    }
    return (acquisition,)


@app.cell(hide_code=True)
def _(
    acquisition,
    connexion_arduino,
    demarrer,
    get_ser,
    lire_ligne,
    nb_mesures,
    parse_ligne,
    reset_arduino,
    sauvegarder_csv,
):
    # Un clic sur « Démarrer » change la valeur du bouton → l'acquisition se
    # lance. Sans nouveau clic, la cellule renvoie simplement les données déjà
    # mesurées (les cellules suivantes sont recalculées si elles ont changé).
    if demarrer.value != acquisition["clics"]:
        acquisition["clics"] = demarrer.value
        acquisition["message"] = "Acquisition en cours…"
        try:
            connexion_arduino()
            reset_arduino()    # réinitialisation de l'Arduino et purge du tampon
            ser = get_ser()

            # Liste pour stocker les tensions mesurées
            liste_donnees = []
            lectures_vides = 0
            premiers_rejets = 10    # on écarte les 10 premières lectures :
            # juste après le reset de la carte, l'entrée analogique et le buffer
            # série USB ne sont pas encore stabilisés (valeurs aberrantes).

            while len(liste_donnees) < nb_mesures.value:
                ligne = lire_ligne(ser)    # Lire une ligne de données depuis le port série
                parse = parse_ligne(ligne)    # format "temps_us,tension" ; None si ligne invalide
                if parse is None:
                    if ligne:
                        lectures_vides = 0    # ligne reçue mais invalide : on continue
                    else:
                        lectures_vides += 1    # aucune donnée reçue
                        if lectures_vides > 10:
                            print("Plus de données reçues de l'Arduino : arrêt.")
                            break
                    continue
                if premiers_rejets > 0:    # premières lignes instables : non comptées
                    premiers_rejets -= 1
                    continue
                liste_donnees.append(parse[1])    # on ne garde que la tension
                if len(liste_donnees) % 1000 == 0:
                    # Sauvegarde de secours : on ne perd rien si l'application est arrêtée
                    sauvegarder_csv(liste_donnees)
                    print(f"{len(liste_donnees)} mesures enregistrées...")

            acquisition["liste_donnees"] = liste_donnees
            if len(liste_donnees) == 0:
                acquisition["message"] = (
                    "Aucune donnée reçue de l'Arduino : vérifier le câble USB "
                    "et le programme acquisition_continue.ino."
                )
            else:
                # Sauvegarde finale des données
                sauvegarder_csv(liste_donnees)
                acquisition["message"] = (
                    f"Acquisition terminée : {len(liste_donnees)} mesures "
                    "sauvegardées dans statistiques.csv."
                )
        except Exception as erreur:
            acquisition["message"] = f"Erreur avec l'Arduino : {erreur}"

    liste_donnees = acquisition["liste_donnees"]
    message_acquisition = acquisition["message"]
    return (liste_donnees, message_acquisition)


@app.cell
def _(mo):
    mo.md("### Calculs statistiques — moyenne, écart-type et incertitude-type")
    return


@app.cell
def _(array, liste_donnees, mean, sqrt, std):
    # Si aucune mesure n'a encore été effectuée, les valeurs sont indéfinies.
    if len(liste_donnees) == 0:
        donnees = None
        moy = None
        ecartType = None
        incertitudeType = None
    else:
        donnees = array(liste_donnees)
        moy = mean(donnees)
        ecartType = std(donnees, ddof=1)    # ddof=1 permet de calculer l'écart-type expérimental Sn-1
        incertitudeType = ecartType / sqrt(len(donnees))
    return (donnees, ecartType, incertitudeType, moy)


@app.cell
def _(mo):
    mo.md("### Affichage des valeurs statistiques")
    return


@app.cell(hide_code=True)
def _(ecartType, incertitudeType, message_acquisition, mo, moy):
    if moy is None:
        resultat = ""
        panneau = (
            "<div class='panneau'>"
            "<div class='panneau-titre'>Résultats statistiques</div>"
            f"<div class='etat'>{message_acquisition}</div>"
            "</div>"
        )
    else:
        resultat = f"moyenne : {moy:.5} ; incertitude-type : {incertitudeType:.2}"
        panneau = (
            "<div class='panneau'>"
            "<div class='panneau-titre'>Résultats statistiques</div>"
            "<div class='resultat'>"
            f"{resultat}<br>"
            f"écart-type expérimental : <span class='grande'>{ecartType:.5}</span>"
            "</div>"
            "</div>"
        )
    mo.Html(panneau)
    return (resultat,)


@app.cell
def _(mo):
    mo.md("### Histogramme des mesures")
    return


@app.cell(hide_code=True)
def _(donnees, go, mo, resultat):
    if donnees is None:
        graf = mo.Html(
            "<div class='etat'>Effectuer une acquisition pour tracer l'histogramme.</div>"
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=donnees, nbinsx=100, name=resultat))

        # Cosmétique du graphique :
        #fig.update_yaxes(scaleanchor="x", scaleratio=1)    # à décommenter pour un repère orthonormé
        fig.update_xaxes(showgrid=True)    # grille verticale (par défaut)
        fig.update_yaxes(showgrid=True)    # grille horizontale (par défaut)
        fig.update_layout(
            showlegend=True,    # légende du graphique
            title="",    # mettre le titre désiré entre les guillemets
            xaxis_title="x",    # nom de l'axe des abscisses
            yaxis_title="Nombre de tirages",    # nom de l'axe des ordonnées
            height=600)    # hauteur du graphique en pixels ; ex. : 450, 700...
        graf = mo.ui.plotly(fig)

    graf
    return (graf,)


if __name__ == "__main__":
    app.run()