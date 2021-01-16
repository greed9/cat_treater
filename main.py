from machine import Pin, I2C, RTC
import time
import boot
import config
import ntptime

from mqtt import MQTTClient

# Needs open-drain to pull relay optocouplers
# down to ground to enable
RELAY1 = Pin(26, Pin.OPEN_DRAIN)
RELAY2 = Pin(25, Pin.OPEN_DRAIN)

def settimeout(duration): 
    pass

# So to turn on RELAY1 for 10 seconds, publish a message of 10 
# to topic /switching/0
def switch( topic, msg ):
    msg_str = str( msg, 'utf-8' )
    topic_str = str( topic, 'utf-8' )

    print( "topic=" + topic_str )
    print( "msg=" + msg_str )

    relay_str = topic_str.split('/')
    if msg is not None:
        secs = int( msg )
        if relay_str is not None:
            if relay_str[1] == '1':
                RELAY2.off()
                time.sleep( secs )
                RELAY2.on()
            elif relay_str[1] == '0':
                RELAY1.off()
                time.sleep( secs )
                RELAY1.on()
    
def main():
    print( "starting")
    time.sleep(1.0)

    # Since open-drain on() means relays OFF and off() means Relays ON
    RELAY1.on()
    RELAY2.on()
    client = MQTTClient("relays1", "192.168.1.145", port=1883)
    client.settimeout = settimeout
    client.connect()
    client.set_callback( switch )
    client.subscribe( "switching/#")
    
    while True:
        client.check_msg( )
        print( "waiting")
        time.sleep(1.0)

if __name__ == "__main__":
    main ( )
