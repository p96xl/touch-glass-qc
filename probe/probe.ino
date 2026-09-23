// Host-driven probe for a 5-wire panel on A0..A4.
// Send 5 chars + newline, one per pin: H=out high, L=out low, U=input pullup, Z=hi-Z.
// Replies with the 5 averaged ADC readings. All the logic lives on the PC side.
const int P[5] = {A0, A1, A2, A3, A4};
char b[8]; int n = 0;

void setup() { Serial.begin(115200); }

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\r') continue;
    if (c != '\n') { if (n < 8) b[n++] = c; continue; }
    if (n == 5) {
      for (int i = 0; i < 5; i++) {
        if (b[i] == 'H') { pinMode(P[i], OUTPUT); digitalWrite(P[i], HIGH); }
        else if (b[i] == 'L') { pinMode(P[i], OUTPUT); digitalWrite(P[i], LOW); }
        else if (b[i] == 'U') pinMode(P[i], INPUT_PULLUP);
        else pinMode(P[i], INPUT);
      }
      delay(3);  // settle: ~35k pullup x panel capacitance
      for (int i = 0; i < 5; i++) {
        analogRead(P[i]);  // throw away first read after mux switch
        long s = 0; for (int k = 0; k < 16; k++) s += analogRead(P[i]);
        Serial.print(s / 16); Serial.print(i < 4 ? ' ' : '\n');
      }
      for (int i = 0; i < 5; i++) pinMode(P[i], INPUT);  // never leave the panel driven: 5-wire sheet is ~tens of ohms, pins would overcurrent
    }
    n = 0;
  }
}
