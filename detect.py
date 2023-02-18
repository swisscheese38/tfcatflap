from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
import time
from gpiozero import MotionSensor
from RpiMotorLib import rpi_dc_lib
import requests
import sys

def lock_flap():
  print('Flap locked')
  lockMotor.forward(100)
  time.sleep(0.2)
  lockMotor.stop()

def unlock_flap():
  print('Flap unlocked')
  lockMotor.backward(100)
  time.sleep(0.2)
  lockMotor.stop()

# config
min_conf_threshold = 0.5
max_rel_bbox_size = 0.75
min_unlock_seconds = 60
webhook_url = sys.argv[1]

print('Using webhook URL ' + webhook_url)

#init cam, infrared motion sensor and lock motor
cam = cv2.VideoCapture(0)
pir = MotionSensor(4)
lockMotor = rpi_dc_lib.TB6612FNGDc(5, 6, 13)
rpi_dc_lib.TB6612FNGDc.standby(12, True)

# initially lock the flap
lock_flap()
locked = True

# init tensorflow
interpreter = Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

try:
  while True:
    pir.wait_for_motion()
    last_motion = time.time()

    while last_motion + min_unlock_seconds > time.time():

      if pir.motion_detected:
        print('Motion detected')
        last_motion = time.time()

      # get image from webcam and preprocess
      ret, image = cam.read()
      image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      imH, imW, _ = image.shape
      image_resized = cv2.resize(image_rgb, (width, height))
      input_data = np.expand_dims(image_resized, axis=0)

      # Perform the actual detection by running the model with the image as input
      interpreter.set_tensor(input_details[0]['index'], input_data)
      interpreter.invoke()

      # Retrieve detection results
      scores = interpreter.get_tensor(output_details[0]['index'])[0]
      boxes = interpreter.get_tensor(output_details[1]['index'])[0]

      # Loop over all results and draw bounding boxes for all hits
      for i in range(len(scores)):

        if (scores[i] < min_conf_threshold):
          continue

        # Get bounding box coordinates
        ymin = int(max(1,(boxes[i][0] * imH)))
        xmin = int(max(1,(boxes[i][1] * imW)))
        ymax = int(min(imH,(boxes[i][2] * imH)))
        xmax = int(min(imW,(boxes[i][3] * imW)))
        rel_size = ((xmax-xmin)*(ymax-ymin))/(imH*imW)

        if (rel_size > max_rel_bbox_size):
          continue

        # unlock the flap if still locked
        if locked == True:
          unlock_flap()
          locked = False

        # Draw bounding box
        cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

        # Draw label
        label = '%d%%' % (int(scores[i] * 100))
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        label_ymin = max(ymin, labelSize[1] + 10)
        cv2.rectangle(image, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
        cv2.putText(image, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        # Push image to Home Assistant
        requests.post(webhook_url, files={'image': cv2.imencode('.jpg', image)[1]})

    # lock again after minimum unlock time is over
    if locked == False:
      lock_flap()
      locked = True

finally:
  cam.release()
