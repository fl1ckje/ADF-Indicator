# ADF-Indicator
![Maintenance](https://img.shields.io/badge/maintenance-stable-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
[![Discord](https://img.shields.io/badge/chat-on_discord-%237289DA.svg)](https://discordapp.com/users/346979343995633664)

ADF Indicator is a python application for indication direction vector degree received from Arduino UNO.

GUI is implemented with [DearPyGUI]. Serial port communication is implemented with [PySerial].

## Supported operating systems
Application runs on both Windows and Linux:
* Windows:
  - 10 :white_check_mark:
  - 11 :white_check_mark:
* Linux:
  - Ubuntu 22.04 :white_check_mark:
  - Arch Linux :white_check_mark:
 
## Run quick-guide
1. Clone ADFI:
```sh
$ git clone https://github.com/fl1ckje/ADFI
$ cd ADFI
```
2. Install Python dependencies:
```sh
$ pip3 install -r requirements.txt
```
3. Run app:
```sh
$ python3 main.py
```

Check releases page for windows executable builds.

## Screenshots
![Screenshot](https://github.com/fl1ckje/ADFI/blob/master/docs/media/Screenshot.png)

[DearPyGUI]: https://github.com/hoffstadt/DearPyGui/
[PySerial]: https://github.com/pyserial/pyserial/
