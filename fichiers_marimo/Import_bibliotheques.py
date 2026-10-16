# Import_bibliotheques.py — module partagé (version marimo)
# Utilisation dans un notebook marimo :
#   from Import_bibliotheques import tableurVersVariables, Calcul_modele, incertitudes_barres, inf
# Attention : NE PAS EFFACER !

# Bibliothèques : numpy + graphiques interactifs Plotly (API native) :
import numpy as _np
from numpy import linspace, genfromtxt, inf, pi, e, sin, cos, tan, exp, log, sqrt, array, arange, mean, std, maximum, minimum
from numpy.random import random, normal
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as _pio

# Rendu par défaut des graphiques (ne pas modifier) :
_base = _pio.templates["plotly_white"].to_plotly_json()
_layout = _base.get("layout", {})
_layout.update(
    dict(
        margin=dict(t=70, b=55, l=110, r=35),
        title=dict(x=0.5, xanchor="center", font=dict(size=22, color="#111111")),
        font=dict(size=14, color="#333333"),
        xaxis=dict(title=dict(font=dict(size=16)), showgrid=True,
                   gridcolor="#e6e6e6", zeroline=False),
        yaxis=dict(title=dict(font=dict(size=16)), showgrid=True,
                   gridcolor="#e6e6e6", zeroline=False),
        hovermode="closest",
    )
)
_pio.templates["sciences"] = go.layout.Template(dict(layout=_layout))
_pio.templates.default = "sciences"

# Retirer le logo Plotly (dernière icône) de la barre d'outils des graphiques :
for _renderer in _pio.renderers:
    try:
        _pio.renderers[_renderer].config.update({"displaylogo": False})
    except Exception:
        pass

# Modélisation, acquisition série, tableurs :
from scipy import interpolate
from scipy.optimize import curve_fit    # permet de modéliser selon un modèle personnalisé
from lmfit import minimize, Parameters, Parameter, report_fit
from lmfit.models import ExpressionModel
from time import time, sleep, perf_counter
import re
import numpy as np
import serial


def incertitudes_barres(incertitude):
    """Barres d'erreur : nombre → constante ; liste → une valeur par point."""
    if incertitude is None:
        return None
    if np.isscalar(incertitude):
        return dict(type="constant", value=incertitude, color="black", width=3)
    return dict(type="data", array=list(incertitude), color="black", width=3)


def tableurVersVariables(fichier, delimiter=","):
    """Lit un fichier CSV à en-têtes et renvoie un dictionnaire colonne → valeurs."""
    tableau = genfromtxt(fichier, delimiter=delimiter, skip_header=0, names=True)
    return {i: tableau[i] for i in tableau.dtype.names}


def Modele(expression, x, y, contraintes):
    modele = ExpressionModel(expression)    # si la variable indépendante n'est pas "x", ajouter comme argument independant_vars = ["nom"])

    # Cette partie devine les paramètres et leur attribue une valeur initiale de 1 pour la recherche
    parametres = modele.make_params()
    for i in parametres:
        modele.set_param_hint(i, value=1)

    for j in contraintes:
        if j[0] in parametres:
            modele.set_param_hint(j[0], value=j[1], vary=j[2], min=j[3], max=j[4])

    parametres = modele.make_params()

    resultat = modele.fit(y, parametres, x=x)

    # On affiche les valeurs trouvées pour les paramètres :
    valeurs = ""
    for key in resultat.params:
        stderr = resultat.params[key].stderr
        if stderr is not None:
            valeurs += f"{key} = {resultat.params[key].value:.3g} ; incertitude : {stderr:.2g}\n"
        else:
            valeurs += f"{key} = {resultat.params[key].value:.3g} ; incertitude : non calculée\n"
    return (modele, resultat.params, valeurs, expression)


def Calcul_modele(tableau, abscisse, ordonnee, equation, debut, fin, debutCourbe, finCourbe, contraintes):
    # On arrange les expressions avec "x" comme variable, car lmfit travaille avec x par défaut :
    ord = ordonnee
    eq = equation
    equation = re.sub(r"\b" + abscisse + r"\b", "x", equation)
    abscisse = tableau[abscisse]
    ordonnee = tableau[ordonnee]
    if debutCourbe is None:
        debutCourbe = min(abscisse)
    if finCourbe is None:
        finCourbe = max(abscisse)

    # On calcule maintenant les grandeurs liées au modèle :
    xMod = linspace(debutCourbe, finCourbe, 30)
    modele, parametres, valeurs, expression = Modele(equation, abscisse[debut:fin], ordonnee[debut:fin], contraintes)
    expression = f"{ord} = {eq}"
    yMod = modele.eval(parametres, x=xMod)

    return (xMod, yMod, expression, valeurs, abscisse, ordonnee, modele, parametres)
