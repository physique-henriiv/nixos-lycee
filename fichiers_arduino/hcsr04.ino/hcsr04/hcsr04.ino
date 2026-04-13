/* Senseur de distance Ultrason HC-SR04:
 VCC sur Arduino 5v 
 GND sur Arduino GND
 Echo sur Arduino broche 7 
 Trig sur Arduino broche 8
 */

const byte ECHO_PIN = 7; // broche 7 associée au signal  Echo 
const byte TRIG_PIN = 8; // broche 8 associée au Trigger (declenchement)

const unsigned long MEASURE_TIMEOUT = 25000UL; // délais maximum de mesure

int counter = 0; // définition d'un compteur initialisé à 0

void setup() {
 
 Serial.begin (9600); // Activation de la communication série

 pinMode(ECHO_PIN, INPUT); // activation de la broche ECHO_PIN en entrée
 pinMode(TRIG_PIN, OUTPUT); // activitation de la broche TRIG_PIN en sortie
 digitalWrite(TRIG_PIN, LOW); // Initialisation de la broche TRIG_PIN à un niveau bas
}

void loop() {
 counter = counter + 1; // incrementation du compteur
 digitalWrite(TRIG_PIN, HIGH); // emmission d'une impulsion sur la broche TRIG_PIN
 delayMicroseconds(10); // durée de impulsion de 10 ms
 digitalWrite(TRIG_PIN, LOW); // arrêt de l'impulsion sur la broche TRIG_PIN

 // Arduino calcule le retard en microseconde entre l'émission et la reception
 // (broche Echo passe au niveau HAUT) du signal
 long retard = pulseIn(ECHO_PIN, HIGH, MEASURE_TIMEOUT);
  
 Serial.println(retard / 2, 8);  // envoi du délai entre l'émission et la réception. Ce délai est égal à la moitié de la durée de l'impulsion.
 
 delay(50); //Attendre 50ms avant d'effectuer la lecture suivante.
 if (counter > 99){    // arrêt après 100 mesures 
    exit(0) ; 
}
}
