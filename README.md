# pi-hq-camera
Raspberry Pi high quality camera project - capture still and video images

Python3 script to control the Raspberry Pi High Quality Camera module using a push button with the following features:

Three camera modes. Pressing and holding the button for 2 seconds cycles through each mode indicated by an LED:
* Mode 1 (default) - Still capture - slow flash
* Mode 2 Video capture - fast flash
* Mode 3 Safe shutdown - Raspberry Pi safe power off - solid on

Camera functions are controlled by short button presses:
* Mode 1 - Still capture - press and release button to capture an image
* Mode 2 - Video capture - press and release button to start video recording, press and release again to stop video recording
* Mode 3 - Safe shutdown - press and release button to perform Raspberry Pi safe shutdown

## Installation
Clone the repository to your Raspberry Pi home directory:

```
git clone https://github.com/milnepe/pi-hq-camera.git
```

Before running the script enable the camera interface using the Raspberry Pi Configuration from the Preferences menu or raspi-config and reboot:

```
cd pi-hq-camera
python3 pi-hq-camera.py
```

## Automatic start
To run the script automatically when the Raspberry Pi boots up install the systemd unit:

```
sudo cp hq-camera.service /etc/systemd/system/
sudo systemctl enable hq-camera.service
sudo reboot
```

## Image directories
By default images and video are saved to the following directories:
```
/home/pi/Pictures
/home/pi/Videos
```

## Hardware
This script has been designed to use DFRobot Gravity LED & Button modules. These modules can be safely connected directly to the GPIO header using the standard Gravity cables as below:

**Warning - check that it is safe to connect any other type of module in this way as you may damage your Raspberry Pi**

Button
Pin | GPIO   | Func | Colour
--- | ------ | ---- | ------
09  | GND    | GND  | BLACK
11  | GPIO17 | VCC  | RED
23  | GPIO27 | CTL  | ORANGE

LED
Pin | GPIO   | Func | Colour
--- | ------ | ---- | ------
16  | GPIO23 | CTL  | ORANGE
18  | GPIO24 | VCC  | RED
20  | GND    | GND  | BLACK
