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
    # Import des bibliothèques nécessaires
    from numpy import array

    from Import_bibliotheques import tableurVersVariables, Calcul_modele, inf, go

    from time import sleep, time

    from Arduino_lib import connexion_arduino, get_ser, lire_ligne, parse_ligne

    return (
        Calcul_modele,
        array,
        connexion_arduino,
        get_ser,
        go,
        inf,
        parse_ligne,
        sleep,
        tableurVersVariables,
        time,
    )


@app.cell
def _(mo):
    mo.md(r"""
    # Étude d'un circuit RC — Arduino

    On mesure la tension aux bornes d'un condensateur chargé ou déchargé à travers une résistance **R**. La carte Arduino pilote la charge/décharge et transmet la tension, puis l'application ajuste un modèle exponentiel et en déduit la capacité **C = τ / R**.

    ### Conditions du travail

    1. **Programmer la carte** : flasher `acquisition_continue.ino` sur l'Arduino via l'IDE Arduino (carte « Arduino Uno »). Le programme émet en continu sur 115200 bauds des lignes `temps_en_micros,tension_en_V`.
    2. **Branchements** : suivre le schéma ci-dessous. Deux types de broches sont utilisés sur la carte :
       - **D2** : broche numérique (préfixe **D** = *digital*), utilisée comme sortie pour piloter la charge (5 V) ou la décharge (0 V) ;
       - **A0** : broche analogique (préfixe **A** = *analog*), utilisée comme entrée pour mesurer la tension aux bornes du condensateur, au nœud entre **R** et **C**.
    3. **Déroulement** : cette application gère la connexion USB, le déclenchement de la charge/lecture et la sauvegarde dans `rc.csv`. Le bouton « Reconnecter l'Arduino » relance la liaison.

    #### Carte Arduino (vue de dessus) et câblage
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    from pathlib import Path
    dossier = Path(__file__).resolve().parent
    carte = mo.image(dossier / "Arduino.svg", alt="Carte Arduino Uno", width=460, caption="Carte Arduino Uno — schéma de référence")
    schema = mo.Html("""
<div>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 320" width="640" font-family="Arial, sans-serif">
    <!-- Légende des câbles (courte) -->
    <line x1="24" y1="28" x2="100" y2="28" stroke="#c62828" stroke-width="3"/>
    <text x="110" y="33" font-size="12" fill="#c62828">D2 — câble rouge (commande)</text>
    <line x1="24" y1="52" x2="100" y2="52" stroke="#1565C0" stroke-width="3" stroke-dasharray="6,4"/>
    <text x="110" y="57" font-size="12" fill="#1565C0">A0 — câble bleu (mesure uc)</text>
    <line x1="24" y1="76" x2="100" y2="76" stroke="#1e1e1e" stroke-width="3"/>
    <text x="110" y="81" font-size="12" fill="#1e1e1e">GND — câble noir (masse)</text>

    <!-- Boîtier Arduino (schématique) -->
    <rect x="480" y="30" width="150" height="260" rx="10" fill="#f2f4fb" stroke="#233b5f" stroke-width="2"/>
    <text x="555" y="58" font-size="15" font-weight="bold" text-anchor="middle" fill="#1e2b45">Arduino</text>
    <text x="555" y="78" font-size="12" text-anchor="middle" fill="#43536e">Uno</text>

    <!-- Broches (bord gauche) : libellés à l'intérieur -->
    <circle cx="480" cy="120" r="6" fill="#c62828"/>
    <text x="492" y="126" font-size="13" fill="#c62828" font-weight="bold">D2</text>
    <circle cx="480" cy="185" r="6" fill="#1565C0"/>
    <text x="492" y="191" font-size="13" fill="#1565C0" font-weight="bold">A0</text>
    <circle cx="480" cy="265" r="6" fill="#1e1e1e"/>
    <text x="492" y="271" font-size="13" fill="#1e1e1e" font-weight="bold">GND</text>

    <!-- Câble rouge : D2 -> R -->
    <path d="M 480,120 H 420" stroke="#c62828" stroke-width="3" fill="none"/>
    <!-- Résistance R (symbole rectangulaire) -->
    <rect x="340" y="100" width="80" height="40" fill="#ffffff" stroke="#233b5f" stroke-width="2.5"/>
    <text x="380" y="126" font-size="13" text-anchor="middle" fill="#233b5f" font-weight="bold">R</text>
    <path d="M 340,120 H 320 V 185" stroke="#c62828" stroke-width="3" fill="none"/>

    <!-- Nœud de mesure R–C -->
    <circle cx="320" cy="185" r="6" fill="none" stroke="#6a1bb5" stroke-width="4"/>
    <circle cx="320" cy="185" r="2.5" fill="#6a1bb5"/>
    <text x="340" y="170" font-size="11" fill="#6a1bb5" font-weight="bold">nœud R–C</text>

    <!-- Condensateur C -->
    <line x1="320" y1="185" x2="320" y2="215" stroke="#1e1e1e" stroke-width="3"/>
    <line x1="305" y1="215" x2="335" y2="215" stroke="#1e1e1e" stroke-width="3"/>
    <line x1="305" y1="235" x2="335" y2="235" stroke="#1e1e1e" stroke-width="3"/>
    <line x1="320" y1="235" x2="320" y2="265" stroke="#1e1e1e" stroke-width="3"/>
    <text x="340" y="228" font-size="12" fill="#1e1e1e" font-weight="bold">C</text>

    <!-- Câble noir : sortie de C vers GND -->
    <path d="M 320,265 H 480" stroke="#1e1e1e" stroke-width="3" fill="none"/>

    <!-- Câble bleu pointillé : nœud -> A0 -->
    <path d="M 320,185 H 480" stroke="#1565C0" stroke-width="3" fill="none" stroke-dasharray="7,5"/>
  </svg>
  <figcaption style="color: var(--muted-foreground); text-align: center; margin-top: 0.5rem; font-size: 0.85em;">Câblage du circuit RC</figcaption>
</div>
    """)
    mo.hstack([carte, schema])
    return


@app.cell(hide_code=True)
def _(mo):
    charge = mo.ui.switch(value=True, label="Charge du condensateur")
    duree = mo.ui.number(value=0.200, start=0.02, stop=5, step=0.05, label="Durée d'acquisition (s)")
    reconnecter = mo.ui.button(label="Reconnecter l'Arduino")
    return charge, duree, reconnecter


@app.cell(hide_code=True)
def _():
    # Numéros des broches (déjà configurés dans le programme acquisition_continue.ino)
    Analog_pin = 0
    Digital_pin = 2
    return (Digital_pin,)


@app.cell
def _(charge, duree, message_connexion, mo, reconnecter):
    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Réglages de l'acquisition</div>"
        f"<div class='ligne'>{charge} {duree} {reconnecter}</div>"
        f"<div class='etat'><b>Arduino :</b> {message_connexion}</div>"
        "</div>"
    )
    return


@app.cell(hide_code=True)
def _(connexion_arduino, reconnecter):
    # Le bouton "Reconnecter" modifie sa valeur → cette cellule se relance.
    # Détection et connexion à l'Arduino ; si absent, on passera en mode
    # "démo" en relisant le dernier enregistrement rc.csv.
    if reconnecter.value:
        pass
    try:
        message_connexion = connexion_arduino()
        arduino_disponible = True
    except Exception as e:
        message_connexion = f"Arduino indisponible : {e} → mode démo (données rc.csv)"
        arduino_disponible = False
    return arduino_disponible, message_connexion


@app.cell(hide_code=True)
def _(
    Digital_pin,
    arduino_disponible,
    array,
    charge,
    connexion_arduino,
    duree,
    get_ser,
    message_connexion,
    parse_ligne,
    sleep,
    tableurVersVariables,
    time,
):
    if arduino_disponible:
        # Reconnexion si le port s'est fermé entre deux acquisitions
        try:
            connexion_arduino()
        except Exception:
            pass
        materiel = get_ser()

        def set_digital_pin(pin, etat):
            commande = f"D{pin}:{etat}\n"
            materiel.write(commande.encode())
            # L'Arduino émet en continu : on lit jusqu'à la réponse de la commande,
            # sans jamais y passer plus d'une seconde.
            debut = time()
            while time() - debut < 1.0:
                ligne = lire_ligne(materiel)
                if not ligne:
                    continue
                reponse = ligne.decode("utf-8", errors="replace").strip()
                if reponse.startswith(("OK:", "ERREUR:")):
                    return
            print("Pas de réponse confirmée de l'Arduino (commande envoyée quand même).")

        etat = 1 if charge.value else 0
        print(message_connexion)
        print(f"Condition initiale : {'charge' if etat == 1 else 'décharge'}")

        # Mise en place de la condition initiale (inverse de ce qu'on va faire ensuite)
        set_digital_pin(Digital_pin, 1 - etat)
        sleep(0.5)
        materiel.reset_input_buffer()
        print(f"Début de l'acquisition pour {duree.value} secondes...")
        set_digital_pin(Digital_pin, etat)

        temps_brut = []
        tension_brut = []
        temps_initial = None
        lecture_vide = 0
        sortie = time()
        while True:
            try:
                ligne = lire_ligne(materiel)
                parse = parse_ligne(ligne)
                if parse is None:
                    if ligne:
                        lecture_vide = 0
                    else:
                        lecture_vide += 1
                        if lecture_vide > 10:
                            print("Plus de données reçues de l'Arduino : arrêt.")
                            break
                    continue
                temps_us, tension = parse
                if temps_initial is None:
                    temps_initial = temps_us
                temps_brut.append((temps_us - temps_initial) / 1e6)
                tension_brut.append(tension)
                if temps_brut[-1] >= duree.value:
                    break
                if time() - sortie > duree.value + 3:
                    print("Durée maximale dépassée : arrêt.")
                    break
            except KeyboardInterrupt:
                print("Acquisition interrompue.")
                break

        if len(temps_brut) == 0:
            raise Exception("Aucune donnée reçue : vérifier le câble USB et le programme acquisition_continue.ino.")

        temps = array(temps_brut)
        tension = array(tension_brut)
        print(f"Acquisition terminée : {len(temps)} points collectés sur {temps[-1]:.3f} s.")

        # Sauvegarde (réimportable avec tableurVersVariables('rc.csv'))
        with open("rc.csv", "w") as fichier:
            fichier.write("t,uc\n")
            for temps_relatif, tension_ponctuelle in zip(temps, tension):
                fichier.write(f"{temps_relatif:.6f},{tension_ponctuelle:.6f}\n")
        print("Données sauvegardées dans rc.csv.")
    else:
        # Mode démo : on rejoue la dernière acquisition enregistrée
        print(message_connexion)
        tableau = tableurVersVariables("rc.csv")
        temps = tableau["t"]
        tension = tableau["uc"]
    return temps, tension


@app.cell(hide_code=True)
def _(Calcul_modele, charge, inf, temps, tension):
    # Définition des contraintes pour le modèle
    if charge.value:
        equation = "E * (1 - exp(-1 * t / tau))"
    else:
        equation = "E * exp(-1 * t / tau)"

    contraintes = [["tau", 1, True, 0, inf], ["E", 5, True, 0, 6]]

    # Calcul du modèle (linéarise en 'x' la variable 't', nom arg de l'équation)
    xMod, yMod, expression, valeurs, abscisse, ordonnee, modele, parametres = Calcul_modele(
        {"t": temps, "uc": tension}, "t", "uc", equation, 0, len(temps), None, None, contraintes
    )
    return abscisse, expression, ordonnee, parametres, valeurs, xMod, yMod


@app.cell(hide_code=True)
def _(abscisse, expression, go, ordonnee, valeurs, xMod, yMod):
    fig = go.Figure()

    # Tracé des points expérimentaux :
    fig.add_trace(go.Scatter(
        x=abscisse, y=ordonnee,
        mode="markers",
        name="Points expérimentaux",
        marker=dict(symbol="cross", size=10, color="blue")))

    # Tracé du modèle :
    fig.add_trace(go.Scatter(
        x=xMod, y=yMod,
        mode="lines",
        name=f"Modèle : {expression}<br>{valeurs.strip().replace(chr(10), '<br>')}",
        line=dict(color="crimson", width=2)))

    # Cosmétique du graphique :
    #fig.update_yaxes(scaleanchor="x", scaleratio=1)    # à décommenter pour un repère orthonormé
    fig.update_xaxes(showgrid=True)    # grille verticale (par défaut)
    fig.update_yaxes(showgrid=True)    # grille horizontale (par défaut)
    fig.update_layout(
        showlegend=True,
        title="Variation de la tension aux bornes du condensateur",
        xaxis_title="t (s)",
        yaxis_title="uc (V)",
        height=600,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#fbfcfe",
        font=dict(size=14))
    return fig


@app.cell(hide_code=True)
def _(mo):
    resistance = mo.ui.number(label="Résistance R (Ω)")
    return (resistance,)


@app.cell
def _(mo, parametres, resistance, temps):
    R = resistance.value
    tau = parametres["tau"].value
    E = parametres["E"].value
    if R is not None and R > 0:
        chaine_R = f"C = τ / R = <span class='grande'>{tau / R:.3g} F</span> (R = {R:g} Ω)"
    else:
        chaine_R = "Saisir la valeur de R pour calculer C."
    if len(temps):
        resume = f"{len(temps)} points · acquisition sur {temps[-1]:.3f} s"
    else:
        resume = "aucun point pour l'instant · lancer une acquisition pour voir les mesures"
    dom = (
        "<div class='panneau'>"
        "<div class='panneau-titre'>Capacité du condensateur</div>"
        f"<div class='ligne'>{resistance}</div>"
        "<div class='resultat'>"
        f"τ = <span class='grande'>{tau:.3g} s</span> &nbsp;·&nbsp; "
        f"E = <span class='grande'>{E:.3g} V</span><br>"
        f"{chaine_R}"
        "</div>"
        f"<div class='etat'>{resume}</div>"
        "</div>"
    )
    mo.Html(dom)
    return


if __name__ == "__main__":
    app.run()