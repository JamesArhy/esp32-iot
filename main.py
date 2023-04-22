import machine
import network
import time
import config
from umqtt.simple import MQTTClient
import ds18x20
import onewire

led = machine.Pin(2, machine.Pin.OUT)
ow = onewire.OneWire(machine.Pin(config.ow_pin))
ds = ds18x20.DS18X20(ow)


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


def read_ow_and_publish(client: MQTTClient):
    print("reading data from onewire...")
    roms = ds.scan()
    print(f"found {len(roms)} devices...")
    print("reading temp...")
    ds.convert_temp()
    time.sleep_ms(750)
    temps = [[d, c_to_f(ds.read_temp(d))] for d in roms]
    print("publishing to mqtt")
    for i, record in enumerate(temps):
        topic = f"{config.mqtt_group}/{config.mqtt_device}/sensor/ow-{i}/temp_f"
        value = format_mqtt_float(record[1])
        print(topic, value)
        client.publish(topic, value)
        blink_led(1)

    # blink_led(int)


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
tim.init(period=5000, callback=lambda t: read_ow_and_publish(mqtt))
