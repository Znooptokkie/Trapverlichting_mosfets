# Wiring

Dit document beschrijft de elektrische aansluitingen van het automatische trapverlichtingssysteem, inclusief de GPIO-toewijzing, de voedingslijnen en de MOSFET-aansturing.

---

## GPIO-overzicht

De Raspberry Pi Pico 2 leest twee bewegingssensoren uit en stuurt drie lampen aan via PWM-signalen.

|        Onderdeel         | Pico 2-aansluiting |                     Functie                      |
|--------------------------|--------------------|--------------------------------------------------|
|        PIR-sensor 1      |        GP16        | Activeert de verlichting van lamp 1 naar lamp 3. |
|        PIR-sensor 2      |        GP22        | Activeert de verlichting van lamp 3 naar lamp 1. |
|         MOSFET 1         |        GP18        |            PWM-aansturing van lamp 1.            |
|         MOSFET 2         |        GP19        |            PWM-aansturing van lamp 2.            |
|         MOSFET 3         |        GP20        |            PWM-aansturing van lamp 3.            |
| Gemeenschappelijke massa |        GND         |      Referentie voor de besturingssignalen.      |
|       Sensorvoeding      |        VBUS        |         5V-voeding voor de PIR-sensoren.         |

---

## Voedingsaansluitingen

### 24V-voeding

De Mean Well LRS-100-24 levert de 24V-gelijkspanning voor het systeem.

- De positieve uitgang (+24V) voedt de positieve aansluitingen van de drie lampen.
- De positieve uitgang (+24V) voedt ook de ingang van de DC-DC buckconverter via een zekering.
- De negatieve uitgang (V-) vormt de gemeenschappelijke voedingsreferentie voor de low-side-MOSFET-schakeling.

### DC-DC buckconverter

De buckconverter verlaagt de 24V-ingangsspanning naar 5V voor de Raspberry Pi Pico 2.

|      Buckconverter      |                        Aansluiting                       |
|-------------------------|----------------------------------------------------------|
|  Ingang positief (IN+)  |                    +24V via de zekering                  |
|  Ingang negatief (IN-)  |         Negatieve aansluiting van de 24V-voeding         |
| Uitgang positief (OUT+) | 5V-voeding naar de USB-voedingsaansluiting van de Pico 2 |
| Uitgang negatief (OUT-) |                       GND-referentie                     |

### PIR-sensoren

Beide HC-SR505 Mini PIR-sensoren worden gevoed met 5V vanaf VBUS van de Pico 2.

| HC-SR505-aansluiting |       Verbinding       |
|----------------------|------------------------|
|         VCC          |     5V vanaf VBUS      |
|         GND          | Gemeenschappelijke GND |
|     OUT sensor 1     |          GP16          |
|     OUT sensor 2     |          GP22          |

---

## MOSFET-aansluitingen

De drie RFP30N06LE N-kanaal-MOSFETs worden gebruikt als low-side-schakelaars. Iedere MOSFET regelt één lamp.

### Aansluiting per lamp

|    Onderdeel   |                    Verbinding                        |
|----------------|------------------------------------------------------|
|  Lamp positief |                       +24V                           |
|  Lamp negatief |           Drain van de bijbehorende MOSFET           |
|  MOSFET source |        Negatieve aansluiting van de 24V-voeding      |
|  MOSFET gate   | Bijbehorende Pico 2-GPIO via een weerstand van 220 Ω |
| Gate-pull-down |      Weerstand van 10 kΩ tussen gate en source       |

### Overzicht van de drie kanalen

|   Kanaal      |     GPIO      | Gateweerstand | Pull-downweerstand |  Lamp  |
|---------------|---------------|---------------|--------------------|--------|
|    MOSFET 1   |      GP18     |      220 Ω    |        10 kΩ       | Lamp 1 |
|    MOSFET 2   |      GP19     |      220 Ω    |        10 kΩ       | Lamp 2 |
|    MOSFET 3   |      GP20     |      220 Ω    |        10 kΩ       | Lamp 3 |

De gateweerstand wordt in serie geplaatst tussen de GPIO-pin en de gate van de MOSFET.

De pull-downweerstand wordt aangesloten tussen de gate en de source. Hierdoor blijft de MOSFET uitgeschakeld wanneer de GPIO-pin geen actief besturingssignaal levert.

De source-aansluitingen van de MOSFETs zijn verbonden met de negatieve voedingsreferentie. De drain-aansluiting wordt verbonden met de negatieve aansluiting van de bijbehorende lamp.

---

## Gemeenschappelijke GND

De besturing en de MOSFET-schakeling moeten dezelfde elektrische referentie gebruiken.

Verbind daarom de volgende aansluitingen met elkaar:

- GND van de Raspberry Pi Pico 2.
- GND van beide HC-SR505-sensoren.
- OUT- van de DC-DC buckconverter.
- Negatieve aansluiting van de 24V-voeding.
- Source-aansluitingen van de drie MOSFETs.

De verbinding met de negatieve aansluiting van de 24V-voeding zorgt ervoor dat de gate-spanning van iedere MOSFET wordt gemeten ten opzichte van dezelfde referentie als de Pico 2.

De gemeenschappelijke GND is een elektrische referentie en vervangt niet de afzonderlijke positieve voedingsaansluitingen.

---

## PWM-aansturing

De Pico 2 gebruikt PWM-signalen om de helderheid van de lampen te regelen.

| GPIO | PWM-frequentie |          Functie           |
|------|----------------|----------------------------|
| GP18 |    1000 Hz     | Helderheidsregeling lamp 1 |
| GP19 |    1000 Hz     | Helderheidsregeling lamp 2 |
| GP20 |    1000 Hz     | Helderheidsregeling lamp 3 |

De PWM-dutycycle bepaalt hoe lang de MOSFET tijdens iedere periode wordt ingeschakeld. Hierdoor kan de gemiddelde geleverde energie aan de lamp worden geregeld.

De software gebruikt een stapgrootte van `500` voor de helderheidsregeling.

---

## Zekering

De zekering bevindt zich in de positieve 24V-leiding tussen de Mean Well LRS-100-24 en de ingang van de DC-DC buckconverter.

Deze zekering beschermt de voedingslijn naar de buckconverter tegen overstroom.
