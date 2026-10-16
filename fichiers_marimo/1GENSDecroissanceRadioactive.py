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
    from Import_bibliotheques import arange, random, go

    return (arange, go, random)


@app.cell
def _(mo):
    mo.md(r"""
    # Décroissance radioactive

    On simule l'évolution d'un échantillon de **N₀** noyaux radioactifs : à chaque étape, chaque noyau a la même probabilité **λ** de se désintégrer. On suit le nombre **N** de noyaux restants au cours du temps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # N₀ sur une échelle semi-logarithmique (1 → 10 000, fine pour les petites valeurs)
    etapes_N0 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                 12, 15, 18, 22, 26, 30, 35, 40, 45, 50,
                 60, 70, 80, 90, 100,
                 120, 150, 180, 220, 260, 300, 350, 400, 450, 500,
                 600, 700, 800, 900, 1000,
                 1200, 1500, 1800, 2200, 2600, 3000, 3500, 4000, 4500, 5000,
                 6000, 7000, 8000, 9000, 10000]
    nb0 = mo.ui.slider(steps=etapes_N0, value=100, label="N₀ — nombre de noyaux initiaux", full_width=True)
    proba = mo.ui.slider(value=0.1, start=0, stop=1, step=0.01, label="λ — probabilité de désintégration", full_width=True)
    duree = mo.ui.slider(value=50, start=5, stop=200, step=5, label="Durée de la simulation (étapes)", full_width=True)
    relancer = mo.ui.button(label="Relancer la simulation")
    return duree, nb0, proba, relancer


@app.cell(hide_code=True)
def _(duree, mo, nb0, proba, relancer):
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Paramètres de la simulation</div>"
        "<div style='display:flex; flex-direction:column; gap:12px;'>"
        f"{nb0} {proba} {duree} {relancer}"
        "</div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(arange, duree, nb0, proba, random, relancer):
    _ = relancer.value  # relancer régénère la séquence aléatoire
    NbNoyaux = nb0.value
    t = arange(0, duree.value, 1)
    proba_desintegration = proba.value
    N = [NbNoyaux]

    for i in t[:-1]:
        alea = random(NbNoyaux)
        NoyauxDesintegres = (sum(alea < proba_desintegration))
        NbNoyaux = NbNoyaux - NoyauxDesintegres
        N.append(NbNoyaux)

    return N, t


@app.cell(hide_code=True)
def _(go, N, nb0, t):
    fig = go.Figure()

    # Courbe simulée :
    fig.add_trace(go.Scatter(
        x=t, y=N, mode="lines",
        name=f"Simulation (N₀ = {nb0.value})",
        line=dict(color="#10213e", width=3)))

    # Cosmétique du graphique :
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        showlegend=True,
        title="Évolution du nombre de noyaux restants",
        xaxis_title="Temps (étapes)",
        yaxis_title="N",
        height=600,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#fbfcfe",
        font=dict(size=14))
    return (fig,)


@app.cell
def _(N, mo, nb0, proba, t):
    N_final = N[-1]
    t_1_2 = 0.693 / proba.value
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Résultats</div>"
        "<div class='resultat'>"
        f"N restants après {len(t) - 1} étapes : <span class='grande'>{N_final}</span> "
        f"(soit <span class='grande'>{N_final / nb0.value:.1%}</span> de l'état initial)<br>"
        f"Temps de demi-vie théorique : <span class='grande'>{t_1_2:.1f}</span> étapes"
        "</div>"
        "</div>"
    )
    return


if __name__ == "__main__":
    app.run()