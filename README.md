# esp32-iot

## Flash Firmware

```shell
esptool --chip esp32 --port COM5 write_flash -z 0x1000 ./firmware/ESP32_GENERIC-20240222-V1.22.2.bin
```