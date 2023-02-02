# tfcatflap
Work in progress
## Training the model
Look at the repository [tfcatflap-training](https://github.com/swisscheese38/tfcatflap-training) to see how the custom model has been trained.
## Install on a Raspberry Pi Zero 2 W
Setup the Pi with Raspbian (preferably the Lite version in 32 bit) and then install all necessary packages:
```
sudo apt-get update 
sudo apt-get install git pip virtualenv
```
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
Create the directories where the images will be stored inside so they can be used for further training the model:
```
mkdir /home/pi/images/
mkdir /home/pi/images/original/
mkdir /home/pi/images/detected/
```
Verify that the script is working by executing it:
```
python detect.py
```
If there's no errors, you should see images getting created under `/home/pi/images/` if cat snouts have been detected. Afterwards you can deactivate out of your virtual environment and install the script as a systemd service:
```
deactivate
sudo cp tfcatflap.service /lib/systemd/system/.
sudo systemctl start tfcatflap.service
sudo systemctl enable tfcatflap.service
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
sudo apt-get install libatlas-base-dev libopenjp2-7 libavcodec-dev libavformat-dev libswscale-dev libgtk-3-dev
```
