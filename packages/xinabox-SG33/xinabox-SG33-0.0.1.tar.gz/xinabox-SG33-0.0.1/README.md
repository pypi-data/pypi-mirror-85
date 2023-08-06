[![GitHub Issues](https://img.shields.io/github/issues/xinabox/Python-SG33.svg)](https://github.com/xinabox/Python-SG33/issues)
![GitHub Commit](https://img.shields.io/github/last-commit/xinabox/Python-SG33)
![Maintained](https://img.shields.io/maintenance/yes/2020)
![Build status badge](https://github.com/xinabox/Python-SG33/workflows/Python/badge.svg)
![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)

# Python-SG33
TODO - Insert description

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
    upip.install("xinabox-sg33")
    ```

### CC03, CS11 and CW03
- Download the .UF2 file for CC03/CS11/CW03 [CircuitPython](https://circuitpython.org/board/xinabox_cs11/) and flash it to the board.
- TO DO

### MicroBit
- TO DO

## Raspberry Pi

Requires Python 3
```
pip3 install xinabox-sg33
```

# Example
```python
from xCore import xCore
from xSG33 import xSG33

SG33 = xSG33()

while True:
    if SG33.dataAvailable() == True:
        SG33.getAlgorithmResults()

        print(SG33.getTVOC())
        print(SG33.getCO2())
    xCore.sleep(1000)
```
