# Automatische trapverlichting

Een automatisch trapverlichtingssysteem op basis van een Raspberry Pi Pico 2 en MicroPython. Het systeem gebruikt twee PIR-bewegingssensoren om beweging te detecteren en stuurt drie dimbare lampen aan via PWM.

De lampen gaan geleidelijk aan en uit. De volgorde waarin de lampen aangaan, is afhankelijk van welke sensor beweging detecteert.

## Functionaliteiten

- Automatische verlichting met twee bewegingssensoren.
- Aansturing van drie afzonderlijke lampen.
- Geleidelijke in- en uitschakeling met PWM.
- Lampen gaan met een instelbare vertraging achter elkaar aan.
- Verschillende inschakelvolgordes afhankelijk van de geactiveerde sensor.
- Instelbare brandduur op maximale helderheid.

## Hardware

- Raspberry Pi Pico 2
- 2x HC-SR505 PIR-bewegingssensor
- 3x dimbare 24V-lamp
- Mean Well LRS-100-24 voeding
- DC-DC buckconverter
- 3x N-kanaal-MOSFET
- Gateweerstanden en pull-downweerstanden
- Zekering en aansluitmateriaal

Zie [hardware.md](hardware.md) voor de onderdelenlijst en [wiring.md](wiring.md) voor de aansluitingen.

## Software

Het project maakt gebruik van MicroPython.

- `main.py`: start het programma en schakelt de lampen uit wanneer het programma handmatig wordt gestopt.
- `lamps.py`: configureert de sensoren en PWM-uitgangen en regelt de verlichting.

## Instellingen

De belangrijkste instellingen staan in `lamps.py`.

| Instelling | Betekenis | Huidige waarde |
|---|---|---:|
| `STEP` | Helderheidsstap per iteratie | 500 |
| `KEEP_SECS_ON` | Brandduur op maximale helderheid | 20 seconden |
| PWM-frequentie | Frequentie van het PWM-signaal | 1000 Hz |
| Fade-interval | Wachttijd tussen helderheidsstappen | 0,025 seconden |
| Sensorinterval | Wachttijd tussen controles | 0,01 seconden |

## Werking

### Sensor 1

1. Sensor 1 detecteert beweging.
2. Lamp 1 gaat als eerste aan, gevolgd door lamp 2 en lamp 3.
3. De lampen blijven gedurende de ingestelde tijd op maximale helderheid branden.
4. Alle lampen dimmen geleidelijk uit.

### Sensor 2

1. Sensor 2 detecteert beweging.
2. Lamp 3 gaat als eerste aan, gevolgd door lamp 2 en lamp 1.
3. De lampen blijven gedurende de ingestelde tijd op maximale helderheid branden.
4. Alle lampen dimmen geleidelijk uit.

Tijdens een actieve verlichtingscyclus worden beide sensoren tijdelijk niet opnieuw uitgelezen. Nieuwe beweging wordt daardoor genegeerd totdat de cyclus is afgelopen.

## GPIO-aansluitingen

| Onderdeel | GPIO |
|---|---|
| Bewegingssensor 1 | GP16 |
| Bewegingssensor 2 | GP22 |
| Lamp 1 | GP18 |
| Lamp 2 | GP19 |
| Lamp 3 | GP20 |

## Documentatie en PCB

De map `docs/images/` bevat afbeeldingen van het hardwareontwerp en de PCB.

- `docs/images/mosfet_pico_schema.png`: afbeelding van het elektrische schema.
- `docs/images/mosfet_pico_pcb.png`: afbeelding van de PCB-layout.
- `docs/images/mosfet_pico_3d.png`: 3D-weergave van de PCB.

De oorspronkelijke KiCad-projectbestanden staan in `hardware/kicad/`:

- `hardware/kicad/mosfet_pico.kicad_pro`: projectinstellingen.
- `hardware/kicad/mosfet_pico.kicad_sch`: elektrisch schema.
- `hardware/kicad/mosfet_pico.kicad_pcb`: PCB-ontwerp.

De Gerber-bestanden staan in `hardware/production/`. Deze bestanden kunnen worden gebruikt om de PCB bij een PCB-fabrikant te laten produceren.

## Bekende aandachtspunten

De sensor-GPIO's kunnen een ongedefinieerde waarde uitlezen wanneer een sensor of signaaldraad wordt losgekoppeld. Om dit te voorkomen, moeten externe pull-downweerstanden van 10 kΩ worden geplaatst tussen de sensor-GPIO's en GND.

- GP16: pull-downweerstand van 10 kΩ naar GND toevoegen.
- GP22: pull-downweerstand van 10 kΩ naar GND toevoegen.