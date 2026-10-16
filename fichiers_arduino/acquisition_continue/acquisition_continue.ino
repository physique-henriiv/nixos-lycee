// Acquisition continue optimisée pour une cadence élevée :
//  - 115200 bauds (12x plus rapide qu'à 9600)
//  - pas de delay() : le rythme est limité par l'émission série
//  - horodatage en microsecondes (micros())
// Chaque ligne émise : temps_en_microsecondes,tension_en_V
// NB : micros() déborde après ~71 min d'alimentation : arrêter avant.

void setup() {
  Serial.begin(115200); // précise le taux de transfert en bauds
  delay(10); // laisse l'ADC et le circuit d'entrée se stabiliser après le reset
  
  // Configuration des broches digitales en sortie
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  
  // État initial des broches (toutes à LOW)
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
}

String commandeEntree = ""; // Pour stocker les commandes entrantes
boolean commandeComplete = false; // Indique si une commande est complète

void loop() {
  // Vérifier si des commandes sont disponibles sur le port série
  lireCommandeSerie();
  
  // Traiter la commande si elle est complète
  if (commandeComplete) {
    traiterCommande();
    commandeEntree = "";
    commandeComplete = false;
  }
  
  // Échantillon immédiat (pas de delay) : l'émission série règle la cadence
  // (~1000 échantillons/s à 115200 bauds)
  Serial.print(micros()); // temps en microsecondes
  Serial.print(","); // séparateur
  Serial.println(analogRead(0)*5./1023.); // tension en V
}

// Fonction pour lire les commandes entrantes sur le port série
void lireCommandeSerie() {
  while (Serial.available() > 0 && !commandeComplete) {
    char caractereRecu = (char)Serial.read();
    
    // Considère la commande complète si on reçoit un retour à la ligne
    if (caractereRecu == '\n') {
      commandeComplete = true;
    } else {
      commandeEntree += caractereRecu;
    }
  }
}

// Fonction pour traiter les commandes reçues
void traiterCommande() {
  // Format de commande: "DX:Y" où X est le numéro de la broche (2-5) et Y est l'état (0 ou 1)
  if (commandeEntree.startsWith("D") && commandeEntree.length() >= 4) {
    int broche = commandeEntree.substring(1, commandeEntree.indexOf(':')).toInt();
    int etat = commandeEntree.substring(commandeEntree.indexOf(':') + 1).toInt();
    
    // Vérifier que la broche est dans la plage valide (2-5)
    if (broche >= 2 && broche <= 5) {
      digitalWrite(broche, etat == 1 ? HIGH : LOW);
      Serial.print("OK:D");
      Serial.print(broche);
      Serial.print(":");
      Serial.println(etat);
    } else {
      Serial.println("ERREUR:Broche invalide");
    }
  } else {
    Serial.println("ERREUR:Format invalide");
  }
}
