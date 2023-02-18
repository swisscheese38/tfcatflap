# tfcatflap
Work in progress

## Hardware

* SureFlap Microchip Pet Door
* Raspberry Pi Zero 2 W
* MH-SR602 Mini Motion Sensor
* TB6612 Motor Driver
* Night Vision Wide Angle Fisheye 5MP Raspi Cam
* Infrared IR LED Light
* Some cables

## Training the model
Look at the repository [tfcatflap-training](https://github.com/swisscheese38/tfcatflap-training) to see how the custom model has been trained.

## Install the software
Setup the Pi with Raspbian (preferably the Lite version in 32 bit) and then install all necessary packages:
```
sudo apt-get update 
sudo apt-get install git pip virtualenv
```
You have to enable legacy camera support, as it is disabled by default. To do so, type `sudo raspi-config` in a terminal and then choose `Interface Options` and enable `Legacy Camera` and then reboot.

Then clone the respsitory into your home directory:
```
cd
git clone https://github.com/swisscheese38/tfcatflap.git
```

Create a new virtual environment:
```
cd tfcatflap/
virtualenv venv
source venv/bin/activate
```

Once you have sourced the new virtual environment `venv` you should install the required dependencies inside of it:
```
pip install -r requirements.txt
```

Afterwards you can deactivate out of your virtual environment and change the URL in `tfcatflap.service` to your Home Assistant's Push Camera Webhook URL:
```
deactivate
vi tfcatflap.service
```

Install the script as a systemd service and start it (it will now automatically be started on each boot):
```
sudo cp tfcatflap.service /lib/systemd/system/.
sudo systemctl start tfcatflap.service
sudo systemctl enable tfcatflap.service
```

Verify that the script is working by checking it's log output:
```
journalctl -u tfcatflap.service
```

## Errors you might encounter
When running on raspbian you might get any of the following errors:
```
libcblas.so.3: cannot open shared object file: No such file or directory
libopenjp2.so.7: cannot open shared object file: No such file or directory
libavcodec.so.58: cannot open shared object file: No such file or directory
libavformat.so.58: cannot open shared object file: No such file or directory
libswscale.so.5: cannot open shared object file: No such file or directory
libgtk-3.so.0: cannot open shared object file: No such file or directory
```
in that case you need install the following packages:
```
sudo apt-get install libatlas-base-dev
sudo apt-get install libopenjp2-7
sudo apt-get install libavcodec-dev
sudo apt-get install libavformat-dev
sudo apt-get install libswscale-dev
sudo apt-get install libgtk-3-dev
```