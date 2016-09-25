# nodemcu-smh_nodemcu
This project is a recopilation of utilities and howto documentation to ease software development into the NodeMCU IoT platform based on the ESP8266 chip.


## Getting started

### Requirements
* git
* python
* virtualenv


### Installation
Clone the project.
```bash
git clone https://github.com/samuelmh/smh_nodemcu.git
```

Install the virtualenv (inside the cloned folder).
```bash
make install
```

It will create a virtualenv for the project in `~/projects/venvs/smh_nodemcu`

This commands have to be executed prior to operate inside the new environment.
```bash
cd ~/projects/venvs/smh_nodemcu
source bin/activate
cd smh_nodemcu
```


### Flashing the firmware
Some boards do not have the latest firmware or can cause trouble. For these cases this project provides binaries and utilites to ease the process of flashing the circuit.

The `Makefile` provides some commands, so if you type
`make flash-float-4mb` or `flash-integer-4mb`, the latest firmware will be uploaded to the board.

For more information, please see: `doc/firmware.md`


## Connectig to the board
Once the installation is done, there will be the `nodemcu` command available inside the virtualenv. It provides some useful features.

Type `nodemcu --help` to get the available options and commands.


### The terminal
The terminal is a convenient way to interact directly with the board.

Type `nodemcu terminal --help` to get the available options.

Type `nodemcu terminal` to connect to the board. Then you can send commands.
If you press the reset button, you will get a message like this.
```
NodeMCU 1.5.4.1 (SMH custom) build 17-Sep-2016 powered by Lua 5.1.4 on SDK 1.5.4.1(39cb9a32)
lua: cannot open init.lua
>
```

To exit the terminal, just press CTRL+D.

### Testing files
It is possible to execute the lines of a file in the board and then open a terminal.
This is done with the `--file` option and it is useful to test the correctness of a script before uploading it as a permanent file.


## The file manager
The `file` command is the way to manage the files/scripts that will go in the board.

These are the subcommands:
* `add`: upload a file to the board.
* `cat`: read a file from the board.
* `ls`: show files and sizes inside the board.
* `mv`: rename a file inside the board.
* `rm`: remove a file from the board.

If you want a script to be executed on the startup of the board, name it as `init.lua`.

Type `nodemcu file --help` to get more information.


## Scripts
In the folder `scripts`, there are some samples that can be used to test the NodeMCU capabilities as well to inspire your code. These are the current scripts:
* `wifi_ntp_http-server.lua`: connects the ESP8266 chip to an access point, takes the UTC time from a NTP server, set its internal clock and servers timestamps through a HTTP server.


## More
There is more documentation in the `docs` folder!

## Links
* [Official documentation](https://nodemcu.readthedocs.io/en/dev/)
