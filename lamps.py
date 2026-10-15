from machine import Pin, PWM
import uasyncio as asyncio


# Stel beide sensoren in als input
sensor_2 = Pin(22, Pin.IN, Pin.PULL_DOWN)
sensor_1 = Pin(16, Pin.IN, Pin.PULL_DOWN)


# Stel de PWM in voor elke lamp
# De frequentie is 1000 Hz en de beginhelderheid is 0
lamp_1 = PWM(Pin(18), freq=1000, duty_u16=0)
lamp_2 = PWM(Pin(19), freq=1000, duty_u16=0)
lamp_3 = PWM(Pin(20), freq=1000, duty_u16=0)


# Hoe lager het cijfer, hoe langer het duurt voor volledige helderheid
# STEP bepaalt hoeveel de helderheid per stap wordt verhoogd of verlaagd
STEP = 500

# Hoeveel seconden de lampen op maximale helderheid blijven branden
KEEP_SECS_ON = 20

# IN hoeveel stappen de lampen op hun helderst zijn
# 65535 is de maximale waarde voor duty_u16
max_steps = 65535 // STEP


async def fade_in(order):
    # Loop door alle stappen totdat de maximale helderheid bijna is bereikt
    for i in range(max_steps):

        # Steeds een stukje feller licht
        # Totdat de maximale helderheid van 65535 is bereikt
        brightness = i * STEP

        # Zet de eerste lamp steeds een stukje feller
        if i >= 0:
            order[0].duty_u16(brightness)

        # Zorgt voor een interval voordat de tweede lamp aangaat
        if i >= 20:
            order[1].duty_u16(brightness)

        # Zorgt voor een interval voordat de derde lamp aangaat
        if i >= 40:
            order[2].duty_u16(brightness)

        # Wacht 0.025 seconden voordat de volgende stap wordt uitgevoerd
        # Hierdoor wordt de overgang naar volledige helderheid geleidelijk
        await asyncio.sleep(0.025)

    # Behoud de maximale helderheid voor elke lamp
    # Dit zorgt ervoor dat alle lampen volledig branden na het infaden
    for lamp in order:
        lamp.duty_u16(65535)


# Zorg dat de lampen weer van maximale helderheid terug gaan naar uit
async def fade_out(lamps):
    # Verlaag de helderheid in stappen van 500
    # Begin bij maximale helderheid en eindig vlak boven 0
    for brightness in range(65535, 0, -500):

        # Pas de helderheid van alle lampen tegelijk aan
        for lamp in lamps:
            lamp.duty_u16(brightness)

        # Wacht 0.025 seconden voordat de volgende stap wordt uitgevoerd
        # Hierdoor gaan de lampen geleidelijk uit
        await asyncio.sleep(0.025)

    # Zorg dat alle lampen daadwerkelijk volledig uit zijn
    turn_off()


# Zorg dat de lampen daadwerkelijk uit zijn
# Zet de helderheid van elke lamp op 0
def turn_off():
    lamp_1.duty_u16(0)
    lamp_2.duty_u16(0)
    lamp_3.duty_u16(0)


async def run():
    # Blijf controleren of een van de sensoren beweging detecteert
    while True:

        # Lees de huidige status van beide sensoren uit
        sensor_1_state = sensor_1.value()
        sensor_2_state = sensor_2.value()

        # Controleer of een van de sensoren beweging detecteert
        if sensor_1_state or sensor_2_state:

            # Controleer welke sensor beweging heeft gedetecteerd
            if sensor_1_state:
                # Laat de lampen in volgorde van lamp_1 naar lamp_3 aangaan
                await fade_in([lamp_1, lamp_2, lamp_3])

            else:
                # Laat de lampen in omgekeerde volgorde van lamp_3 naar lamp_1 aangaan
                await fade_in([lamp_3, lamp_2, lamp_1])

            # Houd de lampen gedurende KEEP_SECS_ON seconden op maximale helderheid
            # Tijdens deze periode worden beide sensoren niet opnieuw uitgelezen
            await asyncio.sleep(KEEP_SECS_ON)

            # Laat alle lampen geleidelijk uitgaan
            await fade_out([lamp_1, lamp_2, lamp_3])

        # Wacht 0.01 seconden voordat beide sensoren opnieuw worden uitgelezen
        await asyncio.sleep(0.01)
