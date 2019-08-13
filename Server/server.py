from flask import Flask, request, Response
import jsonpickle

#Librerias y variables necesarias para el reconocimineto
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import numpy as np
import tensorflow as tf

# load and evaluate a saved model
from numpy import loadtxt
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import json

# load model
# Model reconstruction from JSON file
with open('model.json', 'r') as f:
    model = model_from_json(f.read())

# Load weights into the new model
model.load_weights('model.h5')

graph = tf.get_default_graph()

#--------------------------------------------------------------------------------------------INICIAN LOS PROCESOS DE RECONOCIMIENTO
def identificar(imageP):
    global graph
    with graph.as_default():
        img = cv2.resize(imageP,(300,300))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        pred = model.predict(img_data)
        #print(pred)

        if((np.amax(pred)*100)<80):
            result = -1
        else:
            result = np.where(pred == np.amax(pred))
        #print(np.amax(pred)*100)
    return result

def proceso(imageP):
    
    image = imageP
    cascPath = "haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    """
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)
    """
    cut = image
    #for (x, y, w, h) in faces:
    #    cut = image[y-20:y+h+20,x:x+w]
    #    cv2.imshow("Faces found", cut)
        #cv2.waitKey(0)

    #Se procesa la imagen para identificar al sujeto
    return identificar(cut)


#-----------------------------------------------------------------------------------Inicia el proceso para la comunicacion con el cliente
# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    #cv2.imshow("Faces found", img)
    #cv2.waitKey(0)

    bbb, msg = proceso(img)
    nombre = ""
    if msg==-1:
        nombre="Desconocido"
    if msg==0:
        nombre="Draven"
    if msg==1:
        nombre="Caty"
    if msg==2:
        nombre="Alfredo"
    if msg==3:
        nombre="Armando"
    if msg==4:
        nombre="Linda"
    if msg==5:
        nombre="Karen"
    if msg==6:
        nombre="Eluis"
    if msg==7:
        nombre="Fernanda"
    if msg==8:
        nombre="Yu"
    if msg==9:
        nombre="Alan"
    if msg==10:
        nombre="Genaro"

    # build a response dict to send back to client
    response = nombre
    #response = {msg}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)