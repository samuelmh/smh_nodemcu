#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://www.youtube.com/watch?v=kNke39OZ2k0

import click
from serial import Serial

from smh_nodemcu.terminal import Terminal


class Config(object):

    def __init__(self):
        self.port = None
        self.baudrate = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--port', default='/dev/ttyUSB0', help='Nodemcu device file.')
@click.option('--baudrate', default=115200, help='Nodemcu baudrate connection.')
@pass_config
def cli(config, port, baudrate):
    config.port = port
    config.baudrate = baudrate


#
### Terminal
#

@cli.command()
@click.option('--file', default=None, help='Load this script before launching the terminal.')
@pass_config
def terminal(config, file):
    """Interactive terminal."""
    connector = Serial(config.port, config.baudrate, timeout=1)
    terminal = Terminal(
        connector=connector,
        func_read=raw_input,
        func_write=lambda x: click.echo(x, nl=False)
    )
    if file:
        with open(file,'r') as f:
            for line in f:
                response = terminal.send_msg_then_read(line)
                click.echo(response)
    terminal.start()
    connector.close()

#
### File Management
#

@cli.group()
@pass_config
def file(config):
    """File management."""
    pass_config

@file.command()
@pass_config
def ls(config):
    """Show files and sizes inside the board."""
    connector = Serial(config.port, config.baudrate, timeout=1)
    terminal = Terminal(connector, None, None)
    response = terminal.send_msg_then_read('l=file.list();for name,size in pairs(l) do  print(name.."<->"..size) end')
    click.echo("{:<20}|{:>14}".format("Filename","Size (Bytes)"))
    click.echo("="*35)
    for l in response.split("\r\n")[1:-1]:
        name, size = l.split("<->")
        click.echo("{:<20}|{:>14}".format(name, size))
    response = terminal.send_msg_then_read('remaining, used, total=file.fsinfo();print("\\nFile system info:\\n Total : "..total.." Bytes\\n Used : "..used.." Bytes\\n Remain: "..remaining.." Bytes\\n")')
    click.echo("\n".join(response.split("\r\n")[1:-1]))
    connector.close()



@file.command()
@click.argument('origin')
@click.argument('destination')
@pass_config
def mv(config, origin, destination):
    """Rename a file inside the board."""
    connector = Serial(config.port, config.baudrate, timeout=1)
    terminal = Terminal(connector, None, None)
    response = terminal.send_msg_then_read('if file.exists("{0}") then if file.exists("{1}") then print("Destination file EXISTS") else file.rename("{0}","{1}"); print("OK") end else print("Origin file does NOT exist.") end'.format(origin, destination))
    click.echo(response.split("\r\n")[1])
    connector.close()


@file.command()
@click.argument('filename')
@pass_config
def rm(config, filename):
    """Remove a file from the board."""
    connector = Serial(config.port, config.baudrate, timeout=1)
    terminal = Terminal(connector, None, None)
    response = terminal.send_msg_then_read('if file.exists("{0}") then file.remove("{0}");print("OK") else print("File does NOT exist.") end'.format(filename))
    click.echo(response.split("\r\n")[1])
    connector.close()


@file.command()
@click.argument('origin')
@click.argument('destination')
@pass_config
def add(config, origin, destination):
    """Upload a file to the board."""
    try:
        with open(origin,'r') as f_origin:
            data = f_origin.read()
    except:
        click.echo("Origin file {0} does NOT exist.".format(origin))
    else:
        connector = Serial(config.port, config.baudrate, timeout=1)
        terminal = Terminal(connector, None, None)
        response = terminal.send_msg_then_read('if file.exists("{0}") then print("Destination file EXISTS, remove it first.") else file.open("{0}","w");print("OK") end'.format(destination))
        response = response.split("\r\n")[1]
        if response=="OK":
            bs = 200
            chunks = [
                'file.write(\'{0}\')'.format(data[offset:offset+bs].replace("\\","\\\\").replace("'","\\'").replace("\n","\\n"))
                for offset
                in range(0,len(data),bs)
            ]
            for chunk in chunks:
                #print chunk
                print terminal.send_msg_then_read(chunk)
            terminal.send_msg_then_read('file.flush();file.close()')
            click.echo("OK")
        else:
            click.echo(response)
        connector.close()


@file.command()
@click.argument('filename')
@pass_config
def cat(config, filename):
    """Read a file from the board."""
    connector = Serial(config.port, config.baudrate, timeout=1)
    terminal = Terminal(connector, None, None)
    response = terminal.send_msg_then_read('if file.exists("{0}") then bs=512;file.open("{0}","r");flag_read=true;while flag_read do s=file.read(bs);uart.write(0,s);if string.len(s)<bs then flag_read=false end;end;file.close();else print("File does NOT exist.") end'.format(filename))
    click.echo(("\n".join(response.split("\n")[1:])[:-2]), nl=False)




if __name__ == '__main__':
    cli()
