import uasyncio as asyncio

import lamps


# Start de hoofdfunctie waarin de lampen worden aangestuurd
async def main():

    # Voer de run-functie van het lamps-bestand uit
    # asyncio.gather maakt het mogelijk om meerdere async functies tegelijk uit te voeren
    await asyncio.gather(
        lamps.run()
    )


try:
    # Start de asyncio event loop en voer de main-functie uit
    # Hierdoor blijft het programma draaien en worden de lampen aangestuurd
    asyncio.run(main())

except KeyboardInterrupt:
    # Zorg dat de lampen uitgaan wanneer het programma handmatig wordt gestopt
    # Bijvoorbeeld door op CTRL + C te drukken
    lamps.turn_off()