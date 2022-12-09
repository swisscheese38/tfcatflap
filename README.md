# tfcatflap
Work in progress
## Training the model
Checkout the Jupyter notebook (using Colab) I used to create the model: [training_material/train.ipynb](training_material/train.ipynb)
## Play around with the model
There's a different Jupyter notebook that you can use to try out different sources of data (images, videos) for the model to detect objects in: [training_material/tryoutmodel.ipynb](training_material/tryoutmodel.ipynb)
## Install on a Raspberry Pi Zero 2 W
Clone the respsitory into your home directory:
```
cd
git clone https://github.com/swisscheese38/tfcatflap.git
```
Make sure you have python, pip and virtualenvironment installed and then create a new virtual environment:
```
cd tfcatflap/
virtualenv venv
source venv/bin/activate
```
Once you have sourced the new virtual environment `venv` you should install the required dependencies inside of it:
```
pip install -r requirements.txt
```
Verify that the script is working by executing it:
```
python detect.py
```
If there's no errors, you should see images getting created under `/home/pi/images/' if cat snouts have been detected. Afterwards you can deactivate out of your virtual environment and install the script as a systemd service:
```
deactivate
cp tfcatflap.service /lib/systemd/system/.
sudo systemctl start tfcatflap.service
sudo systemctl enable tfcatflap.service
```
## Errors you might encounter
When running on raspbian you might get any of the following errors:
```
Original error was: libcblas.so.3: cannot open shared object file: No such file or directory
ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory
ImportError: libavcodec.so.58: cannot open shared object file: No such file or directory
ImportError: libavformat.so.58: cannot open shared object file: No such file or directory
ImportError: libswscale.so.5: cannot open shared object file: No such file or directory
ImportError: libgtk-3.so.0: cannot open shared object file: No such file or directory

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