
from __future__ import print_function
import requests
import json
import cv2

addr = 'http://192.168.43.105:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

cam = cv2.VideoCapture(0)
ii=0
while True:
	ret_val, img = cam.read()
	ii+=1
	if(ii>=30):
		#cv2.imshow('my webcam', img)
		cv2.imwrite("img.png",img);
		# encode image as jpeg
		_, img_encoded = cv2.imencode('.png', img)
		# send http request with image and receive response
		response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
		# decode response
		print(json.loads(response.text))
		#print("----------------------------------")
		if cv2.waitKey(1) == 27:
			break  # esc to quit
		ii=0
cv2.destroyAllWindows()
