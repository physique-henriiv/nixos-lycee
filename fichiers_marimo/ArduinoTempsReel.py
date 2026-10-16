import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    # Import séquentiel ici, DANS la toute première cellule : l'import de
    # ipywidgets (déclenché par anywidget) en parallèle de l'initialisation
    # marimo cause un deadlock sur IPython.display. Fait une seule fois, avant
    # que les autres cellules ne s'exécutent.
    import IPython.display  # noqa: F401

    import anywidget as anywidget

    import ipywidgets as ipywidgets

    from Arduino_lib import connexion_arduino, get_ser, lire_ligne, parse_ligne

    return (anywidget, connexion_arduino, get_ser, ipywidgets, lire_ligne, parse_ligne, mo)


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


@app.cell
def _(mo):
    mo.md(r"""
    # Acquisition en temps réel — Arduino

    La carte Arduino émet en continu la tension mesurée sur `A0` (lignes `temps_us,tension` à 115200 bauds, programme `acquisition_continue.ino`). Choisissez la durée puis **Démarrer** : la courbe se trace en temps réel. « Arrêter » met fin à l'acquisition.
    """)
    return


@app.cell(hide_code=True)
def _(connexion_arduino, mo):
    # Connexion à la carte AU CHARGEMENT (avant toute mesure) : le reset DTR
    # qui accompagne l'ouverture fait redémarrer l'Arduino (~1 à 2 s). Fait une
    # seule fois ici, les clics suivants n'attendent plus rien. Un message
    # confirme la carte détectée et prête.
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
    # État réactif « une acquisition tourne » : quand la cellule logique
    # change cette valeur, marimo re-exécute la cellule du panneau qui la lit,
    # ce qui recrée le bouton avec le bon label (Démarrer / Arrêter).
    en_cours, set_en_cours = mo.state(False)
    return (en_cours, set_en_cours)


@app.cell(hide_code=True)
def _(en_cours, graphique, mo):
    # L'état partagé vit sur le widget (persistant, jamais recréé entre les
    # re-exécutions de cette cellule) → il n'est pas réinitialisé à chaque clic.
    _w_graph = graphique.widget
    if not hasattr(_w_graph, "_etat_acquisition"):
        _w_graph._etat_acquisition = {
            "clics": 0, "thread": None, "arret": False,
            "message": "Prêt. Cliquez sur Démarrer."}
    _etat = _w_graph._etat_acquisition

    # Champ durée libre : virgule tolérée, champ vide = illimité. La durée
    # n'est prise en compte qu'au clic sur Démarrer (jamais pendant la saisie).
    # Chaque frappe est recopiée dans l'état persistant (sur le widget de tracé)
    # via on_change : ainsi la valeur lue au clic est toujours celle affichée,
    # même si marimo ne synchronise pas la valeur Python du widget en direct.
    if "duree_saisie" not in _etat:
        _etat["duree_saisie"] = ""

    def _sauvegarder_duree(valeur):
        _etat["duree_saisie"] = valeur

    duree = mo.ui.text(
        value=_etat["duree_saisie"],
        on_change=_sauvegarder_duree,
        label="Durée d'acquisition (s) :",
        placeholder="vide = durée illimitée",
        full_width=False,
    )

    # Bouton recréé à chaque re-exécution de cette cellule (clic, ou état
    # en_cours qui change) : label Démarrer/Arrêter selon l'acquisition. La
    # valeur est le compteur de clics publié par on_click ; on la réinitialise
    # à gerard_clics (dernier clic traité) pour que recréer le bouton ne
    # remette jamais le compteur à zéro — sinon un « Arrêt » fantôme part.
    demarrer = mo.ui.button(
        value=_etat["clics"],
        on_click=lambda valeur: valeur + 1,
        label="Arrêter" if en_cours() else "Démarrer",
        kind="danger" if en_cours() else "neutral",
    )

    # Actualisation périodique de l'état : quand l'acquisition se termine
    # d'elle-même (durée atteinte), aucun clic ne survient et le bouton
    # resterait bloqué sur « Arrêter ». Sa valeur change régulièrement et
    # re-provoque la cellule de statut (plus bas) qui remet « en_cours »
    # à False dès que le thread de mesure n'est plus vivant. NB : marimo
    # n'accepte pas d'intervalle < 1 s (minimum du composant refresh).
    rafraichir = mo.ui.refresh(default_interval=1, label="maj auto")

    mo.Html(
        "<div class='panneau'>"
        "<div class='panneau-titre'>Réglages de l'acquisition temps réel</div>"
        f"<div class='ligne'>{duree} {demarrer}</div>"
        # Le minuteur « maj auto » reste monté (DOM caché) mais invisible : il
        # ne doit pas déranger les élèves pendant la manipulation.
        f"<div style='display:none'>{rafraichir}</div>"
        "</div>"
    )
    return (demarrer, rafraichir, duree)


@app.cell(hide_code=True)
def _(rafraichir, en_cours, set_en_cours, graphique):
    # La valeur de mo.ui.refresh change ~1 fois par seconde : lire _tick force
    # cette cellule à se re-exécuter à chaque tick (c'est la « maj auto »).
    _tick = rafraichir.value
    # Elle détecte la fin spontanée de l'acquisition (durée atteinte, carte
    # déconnectée…) : le thread n'est plus vivant sans qu'aucun clic ne soit
    # arrivé, on remet alors l'état « en cours » à False pour que le bouton
    # repasse à Démarrer.
    _etat = getattr(graphique.widget, "_etat_acquisition", None)
    if _etat is not None:
        _thread = _etat["thread"]
        _vivant = _thread is not None and _thread.is_alive()
        if en_cours() and not _vivant:
            set_en_cours(False)
    return ()


@app.cell(hide_code=True)
def _(demarrer, duree, en_cours, mo, set_en_cours, graphique, get_ser, lire_ligne, parse_ligne):
    import os

    # Fenêtre glissante du mode infini : la courbe affichée garde les 60
    # dernières secondes (l'axe des temps, lui, s'adapte en permanence au
    # dernier point : voir la fonction de dessin du widget).
    FENETRE_AFFICHAGE_S = 60

    def _sauvegarder_csv(t_brut, u_brut):
        """Écrit TOUTES les mesures reçues (temps en s, tension en V) dans un CSV.

        Reprend la mise en forme de `sauvegarder_csv` du notebook original :
        en-tête « t,U », 6 décimales, enregistrement dans ASCII simple.
        Renvoie le chemin du fichier écrit, ou None si l'acquisition est vide.
        """
        if not t_brut:
            return None
        try:
            dossier = os.path.dirname(os.path.abspath(__file__))
        except (NameError, AttributeError):
            dossier = os.getcwd()
        chemin = os.path.join(dossier, "arduino.csv")
        with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write("t,U\n")
            for ti, ui in zip(t_brut, u_brut):
                fichier.write(f"{ti:.6f},{ui:.6f}\n")
        return chemin

    # L'état partagé vit sur le widget (persistant, jamais recréé entre les
    # re-exécutions de cette cellule) → il n'est pas réinitialisé à chaque clic.
    widget = graphique.widget
    if not hasattr(widget, "_etat_acquisition"):
        widget._etat_acquisition = {
            "clics": 0, "thread": None, "arret": False,
            "message": "Prêt. Cliquez sur Démarrer."}
    etat = widget._etat_acquisition
    if "duree_eff" not in etat:
        etat["duree_eff"] = 2.0

    # Une acquisition tourne tant que le thread de la boucle est vivant.
    acquisition_en_cours = (
        etat["thread"] is not None and etat["thread"].is_alive()
    )

    # La valeur du bouton est un compteur de clics : on détecte un nouveau
    # clic quand elle diffère du nombre de clics déjà traités.
    duree_valide = False
    if demarrer.value == etat["clics"]:
        # Aucun nouveau clic (saisie durée, état en_cours, etc.) : on ne
        # réagit PAS à la saisie — la durée n'est prise en compte qu'au
        # prochain clic sur Démarrer. Seul cas géré ici : le thread s'est
        # terminé sans clic (durée atteinte) → on recale l'état du bouton.
        thread_vivant = etat["thread"] is not None and etat["thread"].is_alive()
        if en_cours() and not thread_vivant:
            set_en_cours(False)
    elif acquisition_en_cours:
        # Nouveau clic pendant qu'une acquisition tourne : demande d'arrêt.
        etat["clics"] = demarrer.value
        etat["arret"] = True
        widget.message = "Arrêt demandé…"
        set_en_cours(False)
    else:
        # Nouveau clic, aucune acquisition en cours : en lancer une nouvelle.
        etat["clics"] = demarrer.value
        etat["arret"] = False
        # Durée saisie librement : virgule tolérée, champ vide = illimité.
        # On lit la valeur recopiée par on_change dans l'état persistant (au
        # clic, la valeur Python du widget peut être en retard par rapport à
        # ce qui est affiché), avec repli sur duree.value.
        saisie = str(etat.get("duree_saisie", "") or duree.value or "").strip().replace(",", ".")
        duree_valide = True
        if saisie:
            try:
                duree_eff = float(saisie)
                if duree_eff <= 0:
                    raise ValueError
            except ValueError:
                duree_eff = None
                duree_valide = False
        else:
            duree_eff = float("inf")
        if not duree_valide:
            widget.message = "Durée invalide : saisir un nombre positif (ex. 2 ou 3,5)."
            etat["clics"] = 0
        else:
            etat["duree_eff"] = duree_eff
            widget.xs = [0.0]
            widget.ys = [0.0]
            widget.message = "Acquisition en cours…"
            widget.lim = 0 if duree_eff == float("inf") else duree_eff

        def boucle():
            try:
                # Réglages du notebook d'origine (Arduino.ipynb) :
                #   • durée finie ≥ 0,1 s : ~100 points max à l'écran, un point
                #     par interval = max(durée/100, 0,02 s) ;
                #   • durée < 0,1 s : aucun rafraîchissement pendant la mesure,
                #     tracé unique final ;
                #   • durée infinie : un point par 0,1 s, fenêtre glissante de
                #     60 s / 600 points visibles, tout reste dans t_brut/u_brut.
                if etat["duree_eff"] == float("inf"):
                    interval = 0.1
                elif etat["duree_eff"] >= 0.1:
                    interval = etat["duree_eff"] / 100 if etat["duree_eff"] / 100 > 0.02 else 0.02
                else:
                    interval = 0
                affichage_temps_reel = interval > 0
                MAX_POINTS_VISIBLES = 600

                ser = get_ser()
                ser.timeout = 0.1
                # La carte émet en continu : entre deux acquisitions le buffer
                # série s'est rempli de données "anciennes". On les jette pour
                # que temps_initial parte de la première mesure fraîche.
                ser.reset_input_buffer()
                for _ in range(10):
                    ser.readline()
                t_brut = []
                u_brut = []
                t = []
                u = []
                temps_initial = None
                dernier_temps = 0
                last_update_time = -interval  # premier point tracé dès t = 0
                silencieux = 0
                while not etat["arret"]:
                    parse = parse_ligne(lire_ligne(ser))
                    if parse is None:
                        silencieux += 1
                        if silencieux > 10:
                            widget.message = "Aucune donnée reçue : vérifier le câble USB."
                            break
                        continue
                    silencieux = 0
                    temps_us, tension = parse
                    # L'horodatage de la carte (micros()) peut repartir en
                    # arrière brutalement en début d'acquisition (reset lié à la
                    # connexion série / à un rechargement) : on ancre la
                    # référence sur la plus PETITE valeur rencontrée pour ne
                    # produire aucun temps négatif dans la mesure ni le CSV.
                    if temps_initial is None or temps_us < temps_initial:
                        temps_initial = temps_us
                    temps_relatif = (temps_us - temps_initial) / 1e6
                    dernier_temps = temps_relatif
                    # Tous les échantillons (plein débit, CSV) sont conservés.
                    t_brut.append(temps_relatif)
                    u_brut.append(tension)
                    # Affichage : un point par intervalle en temps réel.
                    if temps_relatif >= last_update_time + interval:
                        t.append(temps_relatif)
                        u.append(tension)
                        last_update_time += interval
                        if affichage_temps_reel:
                            # Fenêtre glissante (durée infinie) : 60 s / 600 pts.
                            if etat["duree_eff"] == float("inf"):
                                while (
                                    len(t) > MAX_POINTS_VISIBLES
                                    and t[0] < t[-1] - FENETRE_AFFICHAGE_S
                                ):
                                    t.pop(0)
                                    u.pop(0)
                            widget.xs = list(t)
                            widget.ys = list(u)
                    if etat["duree_eff"] != float("inf") and dernier_temps >= etat["duree_eff"]:
                        break
                if not affichage_temps_reel:
                    # Durée très courte : tracé unique, tous les points d'un coup.
                    widget.xs = list(t)
                    widget.ys = list(u)
                # Sauvegarde CSV de TOUS les échantillons reçus (plein débit),
                # comme dans le notebook d'origine (arduino.csv).
                _chemin = _sauvegarder_csv(t_brut, u_brut)
                if _chemin is None:
                    widget.message = (
                        f"Acquisition terminée : {len(t)} points à l'écran, "
                        f"{len(t_brut)} plein débit. Aucune donnée à enregistrer."
                    )
                else:
                    widget.message = (
                        f"Acquisition terminée : {len(t)} points à l'écran, "
                        f"{len(t_brut)} plein débit. Enregistré en {_chemin}."
                    )
            except Exception as e:
                widget.message = f"Erreur : {e}"
            etat["message"] = widget.message
            etat["thread"] = None

        if duree_valide:
            thread = mo.Thread(target=boucle, daemon=True)
            etat["thread"] = thread
            thread.start()
            set_en_cours(True)

    # La cellule logique n'affiche rien (le panneau est dans la cellule qui
    # définit la durée et le bouton) : on ne retourne pas d'objet affiché.
    return ()


@app.cell(hide_code=True)
def _(anywidget, mo):
    import traitlets

    # Widget de tracé "maison" au format AFM (`export default { render }`), le
    # seul format accepté par le frontend marimo 0.23.16. La FigureWidget plotly
    # ne marche plus : son ESM (bundle minifié) n'a pas de default export.
    ESM = """
    function tracerCache(model, el) {
      function dessiner() {
        try {
        var xs = model.get("xs") || [];
        var ys = model.get("ys") || [];
        var msg = model.get("message") || "";
        var L = 56, R = 16, T = 24, B = 48, W = 920, H = 380;
        var pw = W - L - R, ph = H - T - B;
        var xmax = 0;
        var xlim = Number(model.get("lim")) || 0;
        if (xlim > 0) { xmax = xlim; } else {
          for (var i = 0; i < xs.length; i++) if (xs[i] > xmax) xmax = xs[i];
        }
        var x1 = xlim > 0 ? xlim : (xmax > 1e-6 ? xmax * 1.15 : 1);
        var y0 = 0, y1 = 5;
        function SX(v) { return L + (v / x1) * pw; }
        function SY(v) { return T + ((y1 - v) / (y1 - y0)) * ph; }
        var parts = [];
        parts.push('<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H
          + '" style="border:1px solid #dfe5ee;border-radius:10px;background:#fff">');
        var bornes = 10;
        var pas = x1 / bornes;
        for (var bi = 0; bi <= bornes; bi++) {
          var v = bi * pas;
          parts.push('<line x1="' + SX(v) + '" y1="' + T + '" x2="' + SX(v) + '" y2="' + (T + ph)
            + '" stroke="#e3e8f0" stroke-width="1"/>');
        }
        for (var yv = 0; yv <= 5; yv++) {
          parts.push('<line x1="' + L + '" y1="' + SY(yv) + '" x2="' + (L + pw) + '" y2="' + SY(yv)
            + '" stroke="#e8ecf3" stroke-width="1"/>');
        }
        for (var bi = 0; bi <= bornes; bi++) {
          var v = bi * pas;
          var texte = v.toFixed(v < 1 ? 2 : 1);
          parts.push('<text x="' + SX(v) + '" y="' + (T + ph + 16) + '" font-size="11"'
            + ' fill="#64748b" text-anchor="middle">' + texte + '</text>');
        }
        for (var yv = 0; yv <= 5; yv++) {
          parts.push('<text x="' + (L - 6) + '" y="' + (SY(yv) + 4) + '" font-size="11"'
            + ' fill="#64748b" text-anchor="end">' + yv.toFixed(0) + '</text>');
        }
        parts.push('<rect x="' + L + '" y="' + T + '" width="' + pw + '" height="' + ph
          + '" fill="none" stroke="#94a3b8" stroke-width="1"/>');
        parts.push('<line x1="' + L + '" y1="' + (T + ph) + '" x2="' + (L + pw) + '" y2="' + (T + ph)
          + '" stroke="#475569" stroke-width="1.5"/>');
        parts.push('<line x1="' + L + '" y1="' + T + '" x2="' + L + '" y2="' + (T + ph)
          + '" stroke="#475569" stroke-width="1.5"/>');
        if (xs.length > 1) {
          var d = "";
          for (var i = 0; i < xs.length; i++) {
            d += (i === 0 ? "M" : "L") + SX(xs[i]).toFixed(2) + " " + SY(ys[i]).toFixed(2) + " ";
          }
          parts.push('<path d="' + d + '" fill="none" stroke="#2563eb" stroke-width="2"'
            + ' stroke-linejoin="round" stroke-linecap="round"/>');
        }
        parts.push('<text x="' + L + '" y="' + (T - 8) + '" font-size="13" font-weight="600"'
          + ' fill="#1e2b45">Tension (V)</text>');
        parts.push('<text x="' + (L + pw) + '" y="' + (T + ph + 44) + '" font-size="11"'
          + ' fill="#94a3b8" text-anchor="end">Temps (s)</text>');
        parts.push('</svg>');
        parts.push('<div style="font-size:.85rem;color:#43536e;margin-top:6px">' + msg + '</div>');
        parts.push('<div style="font-size:.7rem;color:#94a3b8">points: ' + xs.length + ', xdernier: '
          + (xs.length ? xs[xs.length - 1] : "-") + '</div>');
        el.innerHTML = parts.join("");
        } catch (e) {
          el.innerHTML = '<pre style="color:#b91c1c">JS ERROR: ' + e.message + '</pre>';
        }
      }
      dessiner();
      model.on("change:xs", dessiner);
      model.on("change:ys", dessiner);
      model.on("change:message", dessiner);
      model.on("change:lim", dessiner);
    }

    export default {
      render: ({ model, el }) => tracerCache(model, el)
    };
    """

    class TraceurTemps(anywidget.AnyWidget):
        _esm = ESM
        xs = traitlets.List(trait=traitlets.Float(), default_value=[0.0]).tag(sync=True)
        ys = traitlets.List(trait=traitlets.Float(), default_value=[0.0]).tag(sync=True)
        message = traitlets.Unicode(default_value="Prêt. Cliquez sur Démarrer.").tag(sync=True)
        # Dernier point attendu sur l'axe des temps : échelle fixe pendant
        # l'acquisition (0 → limite), sinon 0 = échelle automatique.
        lim = traitlets.Float(default_value=0).tag(sync=True)

    graphique = mo.ui.anywidget(TraceurTemps())
    mo.Html(f"<div>{graphique}</div>")
    return (graphique,)


if __name__ == "__main__":
    app.run()