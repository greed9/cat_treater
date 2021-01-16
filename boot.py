# This file is executed on every boot (including wake-boot from deepsleep)
import config
import esp
import network
from machine import Pin

esp.osdebug(None)
#import webrepl
#webrepl.start()

def do_connect():
    red_led = Pin( config.RED_LED, Pin.OUT)
    green_led = Pin( config.GREEN_LED, Pin.OUT)
    green_led.off( )
    red_led.on ( )
    config.wlan = network.WLAN(network.STA_IF)
    config.wlan.active(True)
    if not config.wlan.isconnected():
        print('connecting to network...')
        config.wlan.connect(config.ssid, config.passwd)
        while not config.wlan.isconnected():
            pass
    red_led.off()
    green_led.on()
    print('network config:', config.wlan.ifconfig())

do_connect( )
