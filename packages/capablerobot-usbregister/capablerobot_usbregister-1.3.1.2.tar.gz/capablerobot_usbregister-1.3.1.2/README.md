# Capable Robot : USB Register

Windows command line tool & python library to assist in registering USB drivers.

This repository includes binaries built from the [libwdi](https://github.com/pbatard/libwdi) project.  Specifically:

- `wdi-64bit.exe` : 64-bit binary of [wdi-simple](https://github.com/pbatard/libwdi/blob/master/examples/wdi-simple.c), version v1.3.1.
- `wdi-32bit.exe` : 32-bit binary of [wdi-simple](https://github.com/pbatard/libwdi/blob/master/examples/wdi-simple.c), version v1.3.1.

The python wrapper automatically runs the appropiate binary based on your computers's architecture.

The wrapper also includes registration settings for the following products, enabling error-free device registration.

- [Capable Robot Programmable USB Hub](https://capablerobot.com/products/programmable-usb-hub/)


Pull requests to add additional devices will be gladly accepted.

## Installation

```
    pip install capablerobot_usbregister
```

## Usage

```

    Usage: usbregister [OPTIONS] COMMAND [ARGS]...

    Options:
      --verbose  Increase logging level.
      --help     Show this message and exit.

    Commands:
      list      Print the known devices which can be registered to drivers.
      device    Register the specified device.
      register  Registers driver based on Vendor ID, Product ID, and interface ID.

```
