# tfcatflap
Work in progress
## Training the model
Checkout the Jupyter notebook (using Colab) I used to create the model: [training_material/train.ipynb](training_material/train.ipynb)
## Play around with the model
There's a different Jupyter notebook that you can use to try out different sources of data (images, videos) for the model to detect objects in: [tryoutmodel.ipynb](tryoutmodel.ipynb)
## Install on a Raspberry Pi Zero 2 W
Clone the respsitory into your home directory:
```
cd
git clone https://github.com/swisscheese38/tfcatflap.git
```
Make sure you have python, pip and virtualenvironment installed and then create a new virtual environment:
```
cd tfcatflap/
cd raspberrypi/
virtualenv venv
cd venv/
source bin/activate
```
Once you have sourced the new virtual environment `venv` you should install the required dependencies inside of it:
```
pip install -r ../requirements.txt
```
After that you can try to run the script (it doesn't do anything yet):
```
cd ../
python run.py
```
When running on raspbian you might get the following error:
```
Original error was: libcblas.so.3: cannot open shared object file: No such file or directory
```
in that case you need install the following package:
```
sudo apt-get install libatlas-base-dev
```