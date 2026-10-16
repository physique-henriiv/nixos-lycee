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
    # Interférences de deux ondes — animation

    Deux ondes sinusoïdales de même période **T** et de même amplitude **Ymax** se superposent. On déphase la seconde et on observe l'interférence, c'est-à-dire la somme des deux ondes. Régler les paramètres, puis déplacer le curseur de déphasage.
    """)
    return


@app.cell(hide_code=True)
def _():
    # Remplace le « %run Import_bibliotheques.ipynb » du notebook Jupyter d'origine
    from Import_bibliotheques import linspace, sin, pi, go

    return (go, linspace, pi, sin)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Réglage des paramètres :
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    Ymax = mo.ui.slider(value=1, start=0.5, stop=3, step=0.1, label="Ymax — amplitude (m)", full_width=True)
    T = mo.ui.slider(value=1, start=0.2, stop=3, step=0.1, label="T — période (s)", full_width=True)
    phases = mo.ui.slider(value=50, start=10, stop=200, step=10, label="phases — nombre de valeurs du déphasage", full_width=True)
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Paramètres</div>"
        f"<div style='display:flex;flex-direction:column;gap:10px;'>{T} {Ymax} {phases}</div>"
        f"<div class='etat'>Fenêtre d'affichage : 3 périodes, soit t<sub>max</sub> = 3·T = "
        f"<span class='grande'>{3 * T.value:.1f} s</span> (100 points)</div>"
        "</div>"
    )
    return T, Ymax, phases


@app.cell(hide_code=True)
def _(T, Ymax, linspace, pi, phases, sin):
    # Ondes : y1 fixe, y2 déphasée de φ = i·dphi (i = position du curseur)
    t = linspace(0, 3 * T.value, 100)
    y1 = sin(2 * pi / T.value * t)
    dphi = 2 * pi / phases.value
    return dphi, t, y1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Choix du déphasage entre les deux ondes :
    """)
    return


@app.cell(hide_code=True)
def _(dphi, mo, phases):
    phi_index = mo.ui.slider(value=0, start=0, stop=phases.value - 1, step=1, label="Curseur de déphasage i", full_width=True)
    phi = phi_index.value * dphi
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Déphasage</div>"
        f"<div style='display:flex;flex-direction:column;gap:10px;'>{phi_index}</div>"
        f"<div class='etat'>φ = i·2π/phases = <span class='grande'>{phi:.3f} rad</span> "
        f"(<span class='grande'>{phi / pi:.3f}</span>·π)</div>"
        "</div>"
    )
    return phi, phi_index


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tracé des ondes et de leur somme :
    """)
    return


@app.cell
def _(Ymax, T, dphi, go, mo, phi, pi, sin, t, y1):
    y2 = Ymax.value * sin(2 * pi / T.value * t + phi)
    y = y1 + y2

    fig = go.Figure()
    fig.add_scatter(x=t, y=y1, mode="lines", name="y1",
                    line=dict(color="#636efa", width=2))
    fig.add_scatter(x=t, y=y2, mode="lines", name="y2 (déphasée)",
                    line=dict(color="#EF553B", width=2))
    fig.add_scatter(x=t, y=y, mode="lines", name="y1 + y2",
                    line=dict(color="#00CC96", width=2))

    fig.update_xaxes(title="t (s)", range=[0, 3 * T.value], showgrid=True)
    fig.update_yaxes(title="y (m)", range=[-Ymax.value - 1, Ymax.value + 1], showgrid=True)
    fig.update_layout(
        title=f"Interférences — déphasage φ = {phi:.3f} rad ({phi / pi:.3f}·π)",
        height=550,
        legend=dict(bgcolor="rgba(255,255,255,0.8)"))

    _phi_mod = phi % (2 * pi)
    if _phi_mod < 0.25 * pi or _phi_mod > 1.75 * pi:
        _type = "Interférences <span class='grande'>constructives</span> : la somme atteint ±2·Ymax (φ ≈ 2kπ)"
    elif 0.75 * pi < _phi_mod < 1.25 * pi:
        _type = "Interférences <span class='grande'>destructives</span> : les deux ondes s'annulent (φ ≈ (2k+1)π)"
    else:
        _type = "Interférences <span class='grande'>intermédiaires</span> : la somme oscille entre les deux cas"

    plot = mo.ui.plotly(fig)
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Interférences</div>"
        f"<div class='etat'>{_type}</div>"
        f"<div style='margin-top:6px'>{plot}</div>"
        "</div>"
    )
    return (plot,)


if __name__ == "__main__":
    app.run()