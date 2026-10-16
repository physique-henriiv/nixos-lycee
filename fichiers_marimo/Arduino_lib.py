# Module de bas niveau pour les notebooks marimo pilotant un Arduino.
# Contient la détection des ports, l'ouverture de la connexion série,
# et la lecture/parsing des lignes émises par la carte.
# Aucun effet de bord à l'import : seule l'appel de connexion_arduino() agit.

from time import sleep, time

import serial
import serial.tools.list_ports

BAUDRATE = 115200  # doit correspondre à Serial.begin() dans le programme Arduino


def parse_ligne(ligne):
    """Renvoie (temps_us, tension_V) si la ligne 'temps_us,tension' est valide, sinon None."""
    ligne = ligne.decode("utf-8", errors="replace").strip() if isinstance(ligne, bytes) else ligne.strip()
    if not ligne or "," not in ligne:
        return None
    try:
        temps, tension = ligne.split(",")
        return float(temps), float(tension)
    except ValueError:
        return None


def detect_arduino():
    """Renvoie le chemin du port série de l'Arduino ; lève une exception sinon."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or port.vid == 0x2341:
            return port.device
    for port in ports:
        if "ttyACM" in port.device or "ttyUSB" in port.device:
            return port.device
    raise Exception("Arduino non détecté. Vérifier la connexion USB.")


def lire_ligne(ser, delai_max=0.2):
    """Lit une ligne série en ignorant les exceptions sporadiques
    (pyserial peut lever 'device reports readiness to read but returned no data'
    juste après un reset de la carte). Lève si le problème persiste."""
    debut = time()
    while True:
        try:
            return ser.readline()
        except serial.SerialException:
            if time() - debut > delai_max:
                raise


def lire_ligne_valide(ser):
    """Attend une ligne 'temps_us,tension' exploitable et la renvoie."""
    lectures_vides = 0
    while True:
        ligne = lire_ligne(ser)
        parse = parse_ligne(ligne)
        if parse is not None:
            return parse
        if ligne:
            lectures_vides = 0
        else:
            lectures_vides += 1
            if lectures_vides > 10:
                raise Exception("Aucune donnée reçue de l'Arduino : vérifier le câble USB.")


_ser = None


def connexion_arduino():
    """Ouvre le port série si nécessaire ; ne fait rien s'il est déjà ouvert.

    Renvoie un message d'état. Lève une exception si aucun Arduino n'est détecté
    ou si la carte ne répond pas.
    """
    global _ser
    if _ser is not None and _ser.is_open:
        return f"Connexion déjà ouverte sur {_ser.port}."
    port = detect_arduino()
    message = f"Arduino détecté sur {port}."
    _ser = serial.Serial(port, BAUDRATE, timeout=1)
    # Reset DTR : remet la carte dans un état propre et évite les lectures
    # vides « readiness » juste après l'ouverture du port.
    _ser.setDTR(False)
    sleep(0.1)
    _ser.reset_input_buffer()
    _ser.setDTR(True)
    lire_ligne_valide(_ser)
    return message


def get_ser():
    if _ser is None or not _ser.is_open:
        raise Exception("Port série non ouvert : appeler connexion_arduino() d'abord.")
    return _ser


def fermer_connexion():
    global _ser
    if _ser is not None and _ser.is_open:
        _ser.close()
    _ser = None