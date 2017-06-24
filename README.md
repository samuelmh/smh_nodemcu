# smh_nodemcu
This project is a recopilation of utilities and howto documentation to ease software development into the [NodeMCU](http://nodemcu.com/index_en.html) IoT platform based on the ESP8266 chip.

## Table of contents
* [Getting started](#getting_started)
* [Commands](#commands)
* [Firmware](#firmware)
* [Examples](#examples)
* [Links](#links)


## Getting started <a name="getting_started"></a>

### Requirements
* git
* make
* Python2.7
* virtualenv


### Installation
Clone the project.
```bash
cd
mkdir projects
cd projects
git clone https://github.com/samuelmh/smh_nodemcu.git
```

Install the environment
```bash
cd ~/projects/smh_nodemcu
make install
```

It will create a virtualenv for the project in `~/projects/venvs/smh_nodemcu`

### Permissions
You have to be a member of the `dialout` group. Check it!
```bash
groups
```

If you are not a member, add your user to the group.
```bash
sudo adduser $USER dialout
```

You will need to log again in your system to see if you are in the group.


### Activation
This commands have to be executed prior to operate inside the new environment.
```bash
cd ~/projects/venvs/smh_nodemcu
source bin/activate
```
Now you have access to the `nodemcu` command in the shell.


### Port
To detect the device or port of your board, plug it to the USB port of your computer and type.
```bash
dmesg|tail
```

You will get a message like:
```bash
[  859.743947] usb 3-1: New USB device found, idVendor=1a86, idProduct=7523
[  859.743953] usb 3-1: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[  859.743956] usb 3-1: Product: USB2.0-Serial
[  859.784581] usbcore: registered new interface driver usbserial
[  859.784601] usbcore: registered new interface driver usbserial_generic
[  859.784619] usbserial: USB Serial support registered for generic
[  859.785465] usbcore: registered new interface driver ch341
[  859.785484] usbserial: USB Serial support registered for ch341-uart
[  859.785506] ch341 3-1:1.0: ch341-uart converter detected
[  859.786420] usb 3-1: ch341-uart converter now attached to ttyUSB0
```
The last line, shows the board port is the device `/dev/ttyUSB0`.

*NOTE: by default, the programs use `/dev/ttyUSB0` as the default port, so if this is your case, you don't have to worry. If your port is different, you will have to type the port argument every time you call a program.*


#### Test
Connect to the board. You will have to change the port to your case.

Example:
```bash
nodemcu --port=/dev/ttyUSB0 terminal
```
You will be in the terminal, press the reset button of the board and some letters will appear in the screen. Press Ctrl+D to exit.


## Commands  <a name="commands"></a>
Once the installation is done, there will be the `nodemcu` command available inside the virtualenv. It provides some useful features.

Type `nodemcu --help` to get the available options and commands.


### Terminal
The terminal is a convenient way to interact directly with the board.

Type `nodemcu terminal --help` to get the available options.

Type `nodemcu terminal` to connect to the board. Then you can send commands.
If you press the reset button, you will get a message like this.
```
NodeMCU 1.5.4.1 (SMH all-modules) build 27-Nov-2016 powered by Lua 5.1.4 on SDK 1.5.4.1(39cb9a32)
lua: cannot open init.lua
>
```

To exit the terminal, just press CTRL+D.

#### Testing files
It is possible to execute the lines of a file in the board and then open a terminal.
This is done with the `--file` option and it is useful to test the correctness of a script before uploading it as a permanent file.


### File manager
The `file` command is the way to manage the files/scripts that will go in the board.

These are the subcommands:
* `add`: upload a file to the board.
* `cat`: read a file from the board.
* `ls`: show files and sizes inside the board.
* `mv`: rename a file inside the board.
* `rm`: remove a file from the board.

If you want a script to be executed when the board boots up, name it `init.lua`.

Type `nodemcu file --help` to get more information.




## Firmware <a name="firmware"></a>
Some boards do not have the latest firmware or can cause trouble. For these cases, this project provides binaries and utilites to ease the process of flashing the chip.

The `Makefile` provides some commands, so if you type
`make flash-float-4mb` or `flash-integer-4mb`, the latest firmware will be uploaded to the board.

Example:
```bash
make flash-float-4mb port=/dev/ttyUSB0
```

For more information, please see the [firmware documentation](doc/firmware.md)


## Examples <a name="examples"></a>
There are some samples in the `lua-utils` folder that can be used to test the NodeMCU capabilities as well to inspire your code. These are the current scripts:
* `examples/wifi_ntp_http-server.lua`: connects to an access point, takes the UTC time from a NTP server, set its internal clock and servers timestamps through a HTTP server.
* `utils/GM009605.lua`: class to print messages on a GM009605 128x64 screen.

### External projects
* [iot-gateway-custom](https://github.com/beeva-samuelmunoz/iot-gateway-custom): example of a 3 layer architecture: thing-gateway-MQTT broker.
* [iot-project-feelings](https://github.com/beeva-samuelmunoz/iot-project-feelings): set a feeling on a dial servo wheel controlled over MQTT.
* [iot-project-presence](https://github.com/beeva-samuelmunoz/iot-project-presence): detect presence with a PIR sensor and communicate over WiFi-MQTT.



### Tutorials - Hands On
* [Introduction](https://beeva-samuelmunoz.github.io/iot-workshop-intro/01%20Introduction/intro.html#/)
* [Communications](https://beeva-samuelmunoz.github.io/iot-workshop-intro/02%20Communications/communications.html#/)


## Links <a name="links"></a>
* [NodeMCU Official page](http://nodemcu.com/index_en.html)
* [Official NodeMCU documentation](https://nodemcu.readthedocs.io/en/master/)
* [Firmware (Github)](https://github.com/nodemcu/nodemcu-firmware)
