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
def _(mo):
    mo.md(r"""
    Importation des bibliothèques nécessaires, et calcul des caractéristiques du modèle. Attention : NE PAS EFFACER !
    """)
    return


@app.cell(hide_code=True)
def _():
    from Import_bibliotheques import tableurVersVariables, Calcul_modele, incertitudes_barres, inf, go, np

    return Calcul_modele, go, incertitudes_barres, inf, tableurVersVariables


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Importation de tableaux enregistrés localement en fichiers csv :
    """)
    return


@app.cell
def _(mo):
    nom_fichier = mo.ui.text(value="tableau.csv", label="Nom du fichier CSV à lire")
    mo.vstack([nom_fichier])
    return (nom_fichier,)


@app.cell(hide_code=True)
def _(nom_fichier, tableurVersVariables):
    tableau = tableurVersVariables(nom_fichier.value)
    return (tableau,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Tracé du graphique et du modèle** : les choix se règlent dans les champs ci-dessous (équation, colonnes, incertitudes, titre, axes). Les réglages avancés (contraintes, plages) restent dans le code, modifiables avec `marimo edit`.
    """)
    return


@app.cell
def _(mo):
    equation = mo.ui.text(value="a * x + b", label="Équation du modèle (variable : x ou le nom de l'abscisse)")
    abscisse = mo.ui.text(value="x", label="Colonne en abscisse")
    ordonnee = mo.ui.text(value="y", label="Colonne en ordonnée")
    incertitudeAbscisse = mo.ui.number(value=0, start=0, stop=1000, step=0.1, label="Incertitude type en abscisse (0 : aucune)")
    incertitudeOrdonnee = mo.ui.number(value=0, start=0, stop=1000, step=0.1, label="Incertitude type en ordonnée (0 : aucune)")
    titre = mo.ui.text(value="Mon titre", label="Titre du graphique")
    nom_x = mo.ui.text(value="", label="Nom de l'axe des abscisses")
    nom_y = mo.ui.text(value="", label="Nom de l'axe des ordonnées")
    mo.vstack([equation, abscisse, ordonnee, incertitudeAbscisse, incertitudeOrdonnee, titre, nom_x, nom_y])
    return (
        abscisse,
        equation,
        incertitudeAbscisse,
        incertitudeOrdonnee,
        nom_x,
        nom_y,
        ordonnee,
        titre,
    )


@app.cell(hide_code=True)
def _(
    Calcul_modele,
    abscisse,
    equation,
    go,
    incertitudeAbscisse,
    incertitudeOrdonnee,
    incertitudes_barres,
    inf,
    nom_x,
    nom_y,
    ordonnee,
    tableau,
    titre,
):
    debut = None    # indice du premier élément à prendre en compte pour le modèle (None : le premier de la liste)
    fin = None    # indice du dernier élément à prendre en compte pour le modèle (None : le dernier de la liste)
    debutCourbe = None    # valeur de l'abscisse où débute le tracé du modèle (None : la plus petite valeur de l'abscisse)
    finCourbe = None    # valeur de l'abscisse où se termine le tracé du modèle (None : la plus grande valeur de l'abscisse)
    contraintes = [["a", 1, True, -inf, inf]]    # ['nomDuParametre', valeurInitiale, variabilité, min, max]   à remplir pour chaque paramètre du modèle si la recherche automatique ne trouve pas de valeurs cohérentes

    xMod, yMod, expression, valeurs, x_exp, y_exp, modele, parametres = Calcul_modele(tableau, abscisse.value, ordonnee.value, equation.value, debut, fin, debutCourbe, finCourbe, contraintes)    # Calcul des valeurs du modèle, ne pas modifier

    fig = go.Figure()

    # Points expérimentaux, avec leurs incertitudes :
    fig.add_trace(go.Scatter(
        x=x_exp, y=y_exp,
        mode="markers",    # "markers" points, "lines" courbe, "lines+markers" les deux
        name="mesures",    # texte de la légende
        marker=dict(symbol="x", size=10, color="blue"),    # ex. : symbol="+", size=12, color="red" ; autres couleurs : green, orange, purple, black...
        error_x=incertitudes_barres(incertitudeAbscisse.value or None),    # barres d'incertitude (0 : aucune)
        error_y=incertitudes_barres(incertitudeOrdonnee.value or None)))

    # Courbe du modèle :
    fig.add_trace(go.Scatter(
        x=xMod, y=yMod,
        mode="lines",
        name=f"Modèle : {expression}<br>{valeurs.strip().replace(chr(10), '<br>')}",    # légende sur plusieurs lignes : équation, puis valeurs des paramètres
        line=dict(color="crimson", width=2)))    # ex. : dash="dash" pour une ligne pointillée

    # Cosmétique du graphique :
    #fig.update_yaxes(scaleanchor="x", scaleratio=1)    # à décommenter pour un repère orthonormé
    #fig.update_yaxes(type="log")    # à décommenter pour une échelle logarithmique
    fig.update_xaxes(showgrid=True)    # grille verticale ; ex. : showgrid=False pour l'enlever
    fig.update_yaxes(showgrid=True)    # grille horizontale ; ex. : showgrid=False pour l'enlever
    fig.update_layout(showlegend=True,    # légende du graphique
                      title=titre.value,    # titre saisi ci-dessus
                      xaxis_title=nom_x.value,    # nom de l'axe des abscisses
                      yaxis_title=nom_y.value,    # nom de l'axe des ordonnées
                      height=600)    # hauteur du graphique en pixels ; ex. : 450, 700...
    return modele, parametres


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Calcul de valeurs particulières :
    """)
    return


@app.cell
def _(mo):
    valeur_de_x = mo.ui.number(value=1, start=-1000, stop=1000, step=1, label="Valeur de x")
    mo.vstack([valeur_de_x])
    return (valeur_de_x,)


@app.cell
def _(modele, parametres, valeur_de_x):
    valeur_de_y = modele.eval(parametres, x = valeur_de_x.value)    # calcul dans le sens direct
    return


if __name__ == "__main__":
    app.run()
