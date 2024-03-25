wifi_ssid = ""
wifi_password = ""
wifi_connect_max_retries = 5
dhcp_hostname = "esp32_water_heater"
mqtt_server = "172.16.50.150"
mqtt_port = 1883
mqtt_group = "home"
mqtt_device = dhcp_hostname
ow_pin = 23
sample_period_ms = 60000
watchdog_enabled = True
watchdog_timeout_ms = 5000
sensor_name_map = {
    "esp32_water_heater": {
        0 : "hot/temp_f",
        1 : "cold/temp_f"
    }
}
