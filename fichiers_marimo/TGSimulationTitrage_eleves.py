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
    # Titrage par conductimétrie — simulation

    On simule le titrage conductimétrique d'une solution inconnue par une solution titrante.
    """)
    return


@app.cell(hide_code=True)
def _():
    # Remplace le « %run Import_bibliotheques.ipynb » du notebook Jupyter d'origine
    from Import_bibliotheques import linspace, maximum, minimum, go

    return (go, linspace, maximum, minimum)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Équation de la réaction** : à adapter en fonction du cas traité.

    $$aA + bB \rightarrow cC + dD$$

    Entrer les formules chimiques des espèces en présence et les nombres stoechiométriques :
    """)
    return


@app.cell
def _(mo):
    A = mo.ui.text(value="H3O+", label="Espèce A (titrée)")
    B = mo.ui.text(value="OH-", label="Espèce B (titrante)")
    C = mo.ui.text(value="H2O", label="Produit C")
    D = mo.ui.text(value="(rien)", label="Produit D")

    CatSpect = mo.ui.text(value="Na+", label="Cation spectateur")
    AnSpect = mo.ui.text(value="Cl-", label="Anion spectateur")
    return A, AnSpect, B, C, CatSpect, D


@app.cell
def _(mo):
    a = mo.ui.number(value=1, start=0, stop=4, step=1, label="a")
    b = mo.ui.number(value=1, start=0, stop=4, step=1, label="b")
    c = mo.ui.number(value=1, start=0, stop=4, step=1, label="c")
    d = mo.ui.number(value=1, start=0, stop=4, step=1, label="d")
    return a, b, c, d


@app.cell
def _(A, AnSpect, B, C, CatSpect, D, a, b, c, d, mo):
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Équation de réaction</div>"
        f"<div class='ligne'>{a} {b} {c} {d}</div>"
        f"<div class='ligne'>{A} {B} {C} {D}</div>"
        f"<div class='ligne'>{CatSpect} {AnSpect}</div>"
        f"<div class='resultat'>"
        f"{a.value}A (aq) + {b.value}B (aq) &#8594; {c.value}C (aq) + {d.value}D (aq)<br>"
        f"Ions spectateurs : {CatSpect.value} et {AnSpect.value}"
        "</div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Entrer les valeurs connues relatives aux solutions :
    """)
    return


@app.cell
def _(mo):
    cA = mo.ui.number(value=0.010, start=0, stop=0.2, step=0.001, label="cA (mol/L)")
    VA = mo.ui.number(value=20e-3, start=5e-3, stop=50e-3, step=1e-3, label="VA (L)")
    cB = mo.ui.number(value=0.020, start=0, stop=0.5, step=0.001, label="cB (mol/L)")
    return cA, cB, VA


@app.cell
def _(cA, cB, VA, mo):
    _v_eq = cA.value * VA.value / cB.value if cB.value > 0 else float("nan")
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Solutions</div>"
        f"<div class='ligne'>{cA} {VA} {cB}</div>"
        f"<div class='etat'>Volume équivalent théorique : "
        f"V<sub>éq</sub> = cA·VA / cB = <span class='grande'>{_v_eq * 1e3:.2f} mL</span></div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Calcul des quantités de matière de réactifs et produits en fonction du volume VB versé. Saisir les formules issues du tableau d'avancement (variables disponibles : **cA**, **VA**, **cB**, **VB**, **x** ; fonctions : **linspace**, **maximum**, **minimum**).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    formule_nA = mo.ui.text(
        value="",
        label="nA =",
        placeholder="ex. maximum(cA * VA - x, 0)",
        full_width=True,
    )
    formule_nB = mo.ui.text(
        value="",
        label="nB =",
        placeholder="ex. maximum(cB * VB - x, 0)",
        full_width=True,
    )
    formule_nC = mo.ui.text(
        value="",
        label="nC =",
        placeholder="ex. x",
        full_width=True,
    )
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Saisie des formules — quantités de matière</div>"
        f"<div style='display:flex;flex-direction:column;gap:10px;'>{formule_nA} {formule_nB} {formule_nC}</div>"
        "</div>"
    )
    return formule_nA, formule_nB, formule_nC


@app.cell
def _(VB, cA, cB, minimum, VA, linspace, maximum, formule_nA, formule_nB, formule_nC):
    # Tableau d'avancement : x = avancement (en mol), plafonné par le réactif limitant
    VB = linspace(0, 25e-3, 100)
    x = minimum(cA.value * VA.value, cB.value * VB)

    def _eval_formule(chaine, nom):
        import numpy as np  # noqa: PLC0415

        try:
            valeur = eval(chaine, {"__builtins__": {}}, {
                "VB": VB, "x": x, "cA": cA.value, "VA": VA.value, "cB": cB.value,
                "linspace": linspace, "maximum": maximum, "minimum": minimum,
            })
            return np.atleast_1d(np.asarray(valeur, dtype=float))
        except Exception as e:
            raise ValueError(f"Formule {nom} invalide : {e}") from e

    nA = _eval_formule(formule_nA.value, "nA")
    nB = _eval_formule(formule_nB.value, "nB")
    nC = _eval_formule(formule_nC.value, "nC")
    return VB, nA, nB, nC


@app.cell
def _(VB, cB, cA, mo, nA, nB, nC, VA):
    _v_eq = cA.value * VA.value / cB.value
    _x_eq = cA.value * VA.value
    _vb_fin = VB[-1]
    _n_b_fin = cB.value * _vb_fin - _x_eq
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Quantités de matière</div>"
        "<div class='resultat'>"
        f"Avant l'équivalence (VB &lt; {_v_eq * 1e3:.1f} mL) : "
        f"nA = <span class='grande'>{nA[0]:.2g} mol</span> &#8594; 0 &nbsp;·&nbsp; "
        f"nB = 0 &nbsp;·&nbsp; nC = <span class='grande'>0</span><br>"
        f"À l'équivalence (VB = {_v_eq * 1e3:.2f} mL) : "
        f"nA = 0 &nbsp;·&nbsp; nB = 0 &nbsp;·&nbsp; nC = <span class='grande'>{_x_eq:.2g} mol</span><br>"
        f"Après (VB = {_vb_fin * 1e3:.0f} mL) : "
        f"nA = 0 &nbsp;·&nbsp; nB = <span class='grande'>{_n_b_fin:.2g} mol</span> &nbsp;·&nbsp; "
        f"nC = <span class='grande'>{_x_eq:.2g} mol</span>"
        "</div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Calculs des quantités d'ions spectateurs : saisir les formules (variables disponibles : **cA**, **VA**, **cB**, **VB**).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    formule_cat = mo.ui.text(
        value="",
        label="n(cation spectateur) =",
        placeholder="ex. cB * VB",
        full_width=True,
    )
    formule_an = mo.ui.text(
        value="",
        label="n(anion spectateur) =",
        placeholder="ex. cA * VA",
        full_width=True,
    )
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Saisie des formules — ions spectateurs</div>"
        f"<div style='display:flex;flex-direction:column;gap:10px;'>{formule_cat} {formule_an}</div>"
        "</div>"
    )
    return formule_an, formule_cat


@app.cell
def _(cA, cB, VA, VB, formule_an, formule_cat):
    # Ions spectateurs : quantité versée (cation) et quantité initiale (anion, constante)
    def _eval_formule(chaine, nom):
        import numpy as np  # noqa: PLC0415

        try:
            valeur = eval(chaine, {"__builtins__": {}}, {
                "cA": cA.value, "VA": VA.value, "cB": cB.value, "VB": VB,
            })
            return np.atleast_1d(np.asarray(valeur, dtype=float))
        except Exception as e:
            raise ValueError(f"Formule {nom} invalide : {e}") from e

    nCatSpect = _eval_formule(formule_cat.value, "n(cation spectateur)")
    nAnSpect = _eval_formule(formule_an.value, "n(anion spectateur)")
    return nAnSpect, nCatSpect


@app.cell
def _(mo, nAnSpect, nCatSpect, cA, cB, VA):
    _n_cat_eq = cB.value * (cA.value * VA.value / cB.value)
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Ions spectateurs</div>"
        "<div class='resultat'>"
        f"n(anion spectateur) = cA·VA = <span class='grande'>{nAnSpect[0]:.2g} mol</span> (constant)<br>"
        f"n(cation spectateur) = cB·VB, soit <span class='grande'>{_n_cat_eq:.2g} mol</span> à l'équivalence"
        "</div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tracé des quantités de matière en fonction du volume de solution titrante versé :
    """)
    return


@app.cell
def _(A, B, C, VB, go, mo, nA, nB, nC):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=VB * 1e3, y=nA, mode="lines", name=f"n({A.value})",
        line=dict(width=2)))

    fig.add_trace(go.Scatter(x=VB * 1e3, y=nB, mode="lines", name=f"n({B.value})",
        line=dict(width=2)))

    fig.add_trace(go.Scatter(x=VB * 1e3, y=nC, mode="lines", name=f"n({C.value})",
        line=dict(width=2)))

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    fig.update_layout(
        showlegend=True,
        title="Évolution des quantités au cours du titrage",
        xaxis_title="VB (mL)",
        yaxis_title="n (mol)",
        height=480)
    plot1 = mo.ui.plotly(fig)
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Quantités en fonction de VB</div>"
        f"<div style='margin-top:6px'>{plot1}</div>"
        "</div>"
    )
    return (plot1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Valeurs des conductivités molaires ioniques (en S·m²/mol), et volume initial de la solution titrée :
    """)
    return


@app.cell
def _(mo):
    LA = mo.ui.number(value=34.98e-3, start=0, stop=0.05, step=0.5e-3, label="λ(A)")
    LB = mo.ui.number(value=19.91e-3, start=0, stop=0.05, step=0.5e-3, label="λ(B)")
    LC = mo.ui.number(value=0.0, start=0, stop=0.05, step=0.5e-3, label="λ(C)")
    LD = mo.ui.number(value=0.0, start=0, stop=0.05, step=0.5e-3, label="λ(D)")
    LCatSpect = mo.ui.number(value=5.01e-3, start=0, stop=0.05, step=0.5e-3, label="λ(cation spectateur)")
    LAnSpect = mo.ui.number(value=7.63e-3, start=0, stop=0.05, step=0.5e-3, label="λ(anion spectateur)")
    Vi = mo.ui.number(value=20e-3, start=5e-3, stop=50e-3, step=1e-3, label="Vi (L)")
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Conductivités molaires ioniques</div>"
        f"<div class='ligne'>{LA} {LB} {LC} {LD}</div>"
        f"<div class='ligne'>{LCatSpect} {LAnSpect} {Vi}</div>"
        "</div>"
    )
    return LA, LB, LC, LD, LCatSpect, LAnSpect, Vi


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Calcul des valeurs de la conductivité de la solution (formule à adapter dans le code) :
    """)
    return


@app.cell
def _(LA, LB, LCatSpect, LAnSpect, Vi, VB, nA, nB, nCatSpect, nAnSpect):
    # Conductivité = somme des concentrations molaires ioniques × conductivités molaires ioniques
    Vtotal = Vi.value + VB
    sigma = (nA * LA.value + nB * LB.value + nCatSpect * LCatSpect.value + nAnSpect * LAnSpect.value) / Vtotal
    return sigma


@app.cell
def _(LA, LB, LCatSpect, LAnSpect, Vi, VB, cA, cB, go, mo, sigma, VA):
    _v_eq = cA.value * VA.value / cB.value
    _x_eq = cA.value * VA.value
    _nB_fin = cB.value * 25e-3 - _x_eq
    sigma0 = cA.value * VA.value * (LA.value + LAnSpect.value) / Vi.value
    sigma_eq = (cA.value * VA.value * LAnSpect.value + cB.value * _v_eq * LCatSpect.value) / (Vi.value + _v_eq)
    sigma_fin = (cA.value * VA.value * LAnSpect.value + cB.value * 25e-3 * LCatSpect.value + _nB_fin * LB.value) / (Vi.value + 25e-3)
    fig_1 = go.Figure()
    fig_1.add_trace(go.Scatter(x=VB * 1e3, y=sigma, mode="lines", name="Conductivité", line=dict(width=2)))
    fig_1.add_vline(
        x=_v_eq * 1e3, line_dash="dash", line_color="gray",
        annotation_text="Véq", annotation_position="top")
    fig_1.update_xaxes(showgrid=True)
    fig_1.update_yaxes(showgrid=True)
    fig_1.update_layout(
        showlegend=True,
        title="Évolution de la conductivité au cours du titrage",
        xaxis_title="VB (mL)",
        yaxis_title="conductivité (S/m)",
        height=480)
    plot2 = mo.ui.plotly(fig_1)
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Conductivité de la solution</div>"
        "<div class='resultat'>"
        f"σ initiale = <span class='grande'>{sigma0:.3g} S/m</span> &#8594; "
        f"σ à l'équivalence = <span class='grande'>{sigma_eq:.3g} S/m</span> &#8594; "
        f"σ en fin de titrage = <span class='grande'>{sigma_fin:.3g} S/m</span>"
        "</div>"
        f"<div style='margin-top:6px'>{plot2}</div>"
        "</div>"
    )
    return (plot2,)