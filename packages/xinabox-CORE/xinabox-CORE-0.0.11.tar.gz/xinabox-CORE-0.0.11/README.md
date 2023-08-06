[![GitHub Issues](https://img.shields.io/github/issues/xinabox/Python-CORE.svg)](https://github.com/xinabox/Python-CORE/issues)
![GitHub Commit](https://img.shields.io/github/last-commit/xinabox/Python-CORE)
![Maintained](https://img.shields.io/maintenance/yes/2020)
![Build status badge](https://github.com/xinabox/Python-CORE/workflows/Python/badge.svg)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

# Python-CORE
I2C Core for CC03/CS11/CW03, CW02, CW01, Raspberry Pi and Microbit

# Usage

## Mu-editor
Download [Mu-editor](https://github.com/xinabox/mu-editor/releases/tag/v1.1.0a2)

### CW01 and CW02
- Use [XinaBoxUploader](https://github.com/xinabox/XinaBoxUploader/releases/latest) and flash MicroPython to the CW01/CW02.
- Download Python packages from the REPL with the following code:
    ```python
    import network
    import upip
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("ssid", "password")
    upip.install("xinabox-CORE")
    ```

### CC03, CS11 and CW03
- Download the .UF2 file for CC03/CS11/CW03 [CircuitPython](https://circuitpython.org/board/xinabox_cs11/) and flash it to the board.
- TO DO

### MicroBit
- TO DO

## Raspberry Pi

Requires Python 3
```
pip3 install xinabox-CORE
```