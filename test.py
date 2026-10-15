from machine import Pin
import time

pir = Pin(16, Pin.IN)

count = 0

while True:
    if pir.value() == 1:
        count += 1
        print("{} + {}".format(pir.value(), count))
    time.sleep_ms(100)
