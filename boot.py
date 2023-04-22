# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)

import machine

machine_freq_hz = 240000000
print("booting...")
print(f"setting machine frequency from {machine.freq()} to {machine_freq_hz}")
machine.freq(machine_freq_hz)
