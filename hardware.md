# Hardware

Dit document beschrijft de hardware die wordt gebruikt voor het automatische trapverlichtingssysteem.

---

## Controller

### Raspberry Pi Pico 2

De Raspberry Pi Pico 2 voert de MicroPython-code uit, leest de twee bewegingssensoren uit en genereert PWM-signalen om de drie lampen aan te sturen.

- **Voeding:** 5V via USB, afkomstig van de DC-DC buckconverter.
- **Sensoringangen:** GP16 en GP22.
- **PWM-uitgangen:** GP18, GP19 en GP20.
- **Logicaspanning:** 3,3V.

De GPIO-pinnen worden uitsluitend gebruikt voor besturingssignalen en zijn niet bedoeld om de lampen rechtstreeks aan te sturen.

---

## Bewegingssensoren

### HC-SR505 Mini PIR

Het systeem gebruikt twee HC-SR505 Mini PIR-bewegingssensoren om beweging op verschillende plaatsen bij de trap te detecteren.

De sensoren worden gevoed met 5V vanaf de VBUS-aansluiting van de Raspberry Pi Pico 2.

|  Sensor   | GPIO |                                 Functie                                         |
|-----------|------|---------------------------------------------------------------------------------|
| Sensor 1  |  GP16 | Detecteert beweging en activeert de verlichting in de volgorde lamp 1, 2 en 3. |
| Sensor 2  |  GP22 | Detecteert beweging en activeert de verlichting in de volgorde lamp 3, 2 en 1. |

De voedingsspanning en signaaluitgang zijn twee afzonderlijke zaken. Hoewel de sensoren met 5V worden gevoed, moet het uitgangssignaal binnen het toegestane spanningsbereik van de Pico 2 blijven.

## Lampen

Het systeem gebruikt drie dimbare 24V-lampen die afzonderlijk worden aangestuurd met PWM.

|  Lamp  | GPIO |    Besturing     |
|--------|------|------------------|
| Lamp 1 | GP18 | PWM via MOSFET 1 |
| Lamp 2 | GP19 | PWM via MOSFET 2 |
| Lamp 3 | GP20 | PWM via MOSFET 3 |

De lampen worden gevoed vanuit de 24V-voeding. De MOSFETs schakelen de stroom door de lampen, zodat de Pico 2 de helderheid kan regelen.

---

## Voeding

### Mean Well LRS-100-24

De Mean Well LRS-100-24 levert de 24V-gelijkspanning voor het systeem.

De voeding voorziet de drie lampen van energie en levert de ingangsspanning voor de DC-DC buckconverter die de Raspberry Pi Pico 2 van 5V voorziet.

### DC-DC buckconverter

De buckconverter verlaagt de ingangsspanning van 24V naar 5V.

- **Ingangsspanning:** 24V DC.
- **Uitgangsspanning:** 5V DC.
- **Belasting:** Raspberry Pi Pico 2 via USB en de daarop aangesloten sensoren via VBUS.

### Zekering

In de positieve 24V-leiding naar de buckconverter is een zekering geplaatst.

Deze zekering beschermt de voedingslijn van de buckconverter tegen overstroom.

---

## MOSFET-aansturing

De drie lampen worden afzonderlijk aangestuurd met RFP30N06LE N-kanaal-MOSFETs in een low-side-schakeling.

Elke MOSFET schakelt de negatieve aansluiting van één lamp. De positieve aansluiting van de lamp is verbonden met +24V.

|   Onderdeel    |                  Aansluiting                  |
|----------------|-----------------------------------------------|
| MOSFET 1 gate  |     GP18 via een gateweerstand van 220 Ω      |
| MOSFET 2 gate  |     GP19 via een gateweerstand van 220 Ω      |
| MOSFET 3 gate  |     GP20 via een gateweerstand van 220 Ω      |
| Gate-pull-down |          10 kΩ tussen gate en source          |
|     Source     |         Negatieve voedingsreferentie          |
|     Drain      | Negatieve aansluiting van de betreffende lamp |

De gateweerstand beperkt de stroompieken bij het schakelen. De pull-downweerstand houdt de MOSFET uitgeschakeld wanneer er geen besturingssignaal aanwezig is.

De MOSFETs worden aangestuurd met een logisch signaal van 3,3V.

---

## Massa-aansluitingen

De Pico 2, de bewegingssensoren en de MOSFET-besturing gebruiken een gemeenschappelijke GND-referentie.

Bij de beschreven low-side-schakeling is de source van iedere MOSFET verbonden met de negatieve aansluiting van de 24V-voeding. De GND van de Pico 2 is eveneens met deze referentie verbonden.

---

## PCB en elektrisch schema

Het hardwareontwerp is gemaakt met KiCad.

De bronbestanden van het elektrische schema en de PCB zijn te vinden in `hardware/kicad/`.

Het KiCad-schema bevat de Raspberry Pi Pico 2, de bewegingssensoren en de MOSFET-schakeling. De externe 24V-voeding en de DC-DC buckconverter zijn niet opgenomen in dit schema.

De PCB bevat de componenten en verbindingen die in het PCB-ontwerp zijn opgenomen.

Zie `wiring.md` voor de GPIO-aansluitingen en de verdere documentatie van de bedrading.

De Gerber-bestanden staan in `hardware/production`. Deze bestanden kunnen worden gebruikt om de PCB bij een PCB-fabrikant te laten produceren.