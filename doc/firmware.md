# NodeMCU firmware

This project provides some binary firmwares in the `bin` folder.

All of them have been compiled folowing the docker method stated in the
[official documentation](https://nodemcu.readthedocs.io/en/dev/en/build/).

The process is explained in https://hub.docker.com/r/marcelstoer/nodemcu-build/ .

## Customization
From the [official firmware Github repo](https://github.com/nodemcu/nodemcu-firmware/blob/master/README.md).

* Choose modules in `app/include/user_modules.h`.
* Tag the build in `app/include/user_version.h`.
* Set UART bitrate in `app/include/user_config.h`.

## Docker built
Clone the repo.
```
git clone https://github.com/nodemcu/nodemcu-firmware.git
```
Get into the folder.

Compile the firmware.
```
docker run --rm -ti -v `pwd`:/opt/nodemcu-firmware marcelstoer/nodemcu-build
```
The result is the local `bin` folder.


## Release log

### v20160917
* **Date: 17-Sep-2016**
* **Modules:** ADC, BIT, CRYPTO, DHT, FILE, GPIO, HTTP, I2C, MQTT, NET, NODE, OW, RTCTIME, SNTP, SPI, TMR.
