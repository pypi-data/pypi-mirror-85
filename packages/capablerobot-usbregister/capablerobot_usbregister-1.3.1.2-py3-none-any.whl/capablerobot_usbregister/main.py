#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2020 Chris Osterwood for Capable Robot Components
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, sys, inspect
import time
import argparse
import logging
import platform
import subprocess
import tempfile
import shutil

import click

IFACETYPES = ['winusb', 'libusb-win32', 'libusbk', 'usbser', 'custom']

DATA = {}

DATA['usbhub'] = dict(vid=0x0424, pid=0x494C, 
    interfaces=[dict(iid=0, type=2), dict(iid=1, type=3)],
    vendor="Capable Robot", product="Programmable USB Hub"
)

def setup_logging():
    fmtstr = '%(asctime)s | %(filename)25s:%(lineno)4d %(funcName)20s() | %(levelname)7s | %(message)s'
    formatter = logging.Formatter(fmtstr)

    handler   = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def get_tree_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def wdi(args):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    arch = platform.architecture()[0]

    ## platform.architecture() returns information on the python EXE
    ## But, 32-bit python on 64-bit Windows should actually load the 64-bit DLL.
    if arch == '32bit' and platform.machine() == 'AMD64':
        arch = '64bit'

    exe_path = os.path.join(this_dir, "binaries", "wdi-{}.exe".format(arch))

    if not os.path.exists(exe_path):
        logging.warn("{} was not located".format(os.path.basename(exe_path)))
        return

    dest_dir = None
    dest_dir_delete = True

    ## Normalize the unpacking folder name, if specified with -d form
    if "-d" in args:
        args[args.index("-d")] = "--dest"

    ## Extract the directory and see if it exists and therefore
    ## if it should be deleted after the registration is complete
    if "--dest" in args:
        dest_dir = args[args.index("--dest")+1]

        if os.path.exists(dest_dir):
            dest_dir_delete = False 
    else:
        ## Assign default unpacking folder, if none has been set.
        ## This folder will be automatically deleted
        dest_dir = tempfile.mkdtemp()

        args.append("--dest")
        args.append(dest_dir)

    logging.debug("Unpacking folder : {}".format(dest_dir))

    if " " in dest_dir:
        dest_dir_delete = False
        print("WARN : space detected in the unpacking folder")

    cmd = [exe_path] + [str(arg) for arg in args]
    results = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.debug("CMD {}".format(" ".join(cmd)))
    logging.debug("WDI exit code {}".format(results.returncode))

    for line in results.stdout.decode("utf-8").split("\n"):
        if len(line) > 0:
            logging.debug(line)

    for line in results.stderr.decode("utf-8").split("\n"):
        if len(line) > 0:
            logging.warn(line)

    if dest_dir_delete:
        folder_bytes = get_tree_size(dest_dir)
        expected_bytes = 3858037.0

        if folder_bytes > expected_bytes * 0.9 and folder_bytes < expected_bytes * 1.1:
            logging.debug("Deleting unpacking directory")
            shutil.rmtree(dest_dir)
        else:
            logging.debug("Not deleting unpacking directory, size is incorrect")

    return results

def register(device, stdout=False):
    if stdout:
        name = ''
        if 'vendor' in device and 'product' in device:
            name = "{} {}".format(device['vendor'], device['product'])

        print("Starting registration of {} (VID {} PID {})".format(
            name, device['vid'], device['pid']
        ))

    for iface in device['interfaces']:
        driver_string = IFACETYPES[iface['type']]

        if stdout:
            print("  Assigning interface {} to {} driver".format(iface['iid'], driver_string))

        wdi([
            "--vid", device['vid'], "--pid", device['pid'], 
            "--iid", iface['iid'], "--type", iface['type']
        ])

    if stdout:
        print("Registration complete")

@click.group()
@click.option('--verbose', default=False, is_flag=True, help='Increase logging level.')
def cli(verbose):
 
    if verbose:
        setup_logging()
        logging.debug("Logging Setup")

@cli.command('list')
def cmd_list():
    """ Print the known devices which can be registered to drivers. """

    print()
    print("Known devices which can be registered:")
    print()

    for key, meta in DATA.items():
        print("  {} -> {} {}".format(key, meta['vendor'], meta['product']))

    print()

@cli.command('device')
@click.argument('device')
def cmd_device(device):
    """Register the specified device.  To list known devices, run `list` command."""

    if not device in DATA.keys():
        print("ERROR : Device '{}' is not known by this registration tool.".format(device))
        return

    register(DATA[device], stdout=True)
    

@cli.command('register')
@click.option('--vid', help='Vendor ID', required=True, type=int)
@click.option('--pid', help='Product ID', required=True, type=int)
@click.option('--iid', help='Interface ID', required=True, type=int)
@click.option('--type', help="Drive name. One of ({})".format(" ".join(IFACETYPES)), required=True)
def cmd_register(vid, pid, iid, type):
    """ Registers driver based on Vendor ID, Product ID, and interface ID"""

    if not type in IFACETYPES:
        print("ERROR : Type must be one of [{}]".format(" ".join(IFACETYPES)))
        return

    type = IFACETYPES.index(type)

    register(dict(vid=vid, pid=pid, interfaces=[dict(iid=iid, type=type)]), stdout=True)

def console():
    if not sys.platform.startswith('win'):
        print("This tool is only required on Windows. Exiting.")
        sys.exit(0)

    cli()
    
if __name__ == '__main__':
    console()