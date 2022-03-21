from machine import Pin, I2C
import mcp4728

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

dac=mcp4728.MCP4728(i2c,0x60)


def write_dials(dial1, dial2, dial3, dial4):
    dac.a.value = dial1
    dac.b.value = dial2
    dac.c.value = dial3
    dac.d.value = dial4

def self_test():
    # TODO: make self test