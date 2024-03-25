import machine
import network
import time
import config
from umqtt.simple import MQTTClient
from mpl3115a2 import MPL3115A2

led = machine.Pin(2, machine.Pin.OUT)
i2c = machine.SoftI2C(sda=machine.Pin(config.SDA), scl=machine.Pin(config.SCL))
mpl = MPL3115A2(i2c, mode=MPL3115A2.PRESSURE)


def wifi_connect():
    print("connecting to wifi...")
    sta_if = network.WLAN(network.STA_IF)
    wifi_connected = sta_if.isconnected()
    if not sta_if.active():
        sta_if.active(True)
    while not wifi_connected:
        print(f"connecting to ssid {config.wifi_ssid}...")
        try:
            sta_if.connect(config.wifi_ssid, config.wifi_password)
        except OSError:
            pass
        wifi_connected = sta_if.isconnected()
        if not wifi_connected:
            # wait 1 second before trying again
            time.sleep_ms(1000)
        else:
            wifi_connected = True
            print("wifi connected...")
    blink_led(2)
    return sta_if


def mqtt_connect():
    print("connecting to mqtt...")
    c = MQTTClient(
        client_id=config.dhcp_hostname,
        server=config.mqtt_server,
        port=config.mqtt_port,
    )
    c.connect()
    blink_led(2)
    return c


# def get_temp_f():
def c_to_f(c: float):
    f = (c * 9 / 5) + 32
    return f

def format_mqtt_float(v: float):
    return b"{:.2f}".format(v)

def get_temp_pressure():
    t = format_mqtt_float(mpl.temperature() * (9 / 5) + 32)
    p = format_mqtt_float(mpl.pressure() / 1000)  # Pa to kPa

    return (t, p)

def read_and_publish(client: MQTTClient):
    print("reading data from sensor...")
    t, p = get_temp_pressure()
#     print(f"found {len(roms)} devices...")
#     print("reading temp...")
#     ds.convert_temp()
#     time.sleep_ms(750)
#     temps = [[d, c_to_f(ds.read_temp(d))] for d in roms]
    print("publishing to mqtt")
    topic_prefix = f"{config.mqtt_group}/{config.mqtt_device}/sensor"
    temp_topic = f"{topic_prefix}/temp_f"
    press_topic = f"{topic_prefix}/press_kpa"
    print(temp_topic, t)
    client.publish(temp_topic,t)
    print(press_topic,p)
    client.publish(press_topic,p)
    blink_led(1)


def blink_led(c: int = 2):
    for i in range(c):
        led.on()
        time.sleep_ms(50)
        led.off()
        time.sleep_ms(50)


# Startup
wifi = wifi_connect()
mqtt = mqtt_connect()
tim = machine.Timer(1)
tim.init(period=config.sample_period_ms, callback=lambda t: read_and_publish(mqtt))
