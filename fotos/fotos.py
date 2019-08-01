import cv2
import numpy as np

class Foto:
  def __init__(self):
    print('')
    return
  # Create a imagen object and read from input file
  # If the input is the camera, pass 0 instead of the video file name
  def mainFoto(self, nombre):
    # We load the image from disk
    img = cv2.imread(nombre, cv2.IMREAD_COLOR)

    # We check that our image has been correctly loaded
    if (img.size == 0):
        sys.exit("Error: the image has not been correctly loaded.")

    # We display our image and ask the program to wait until a key is pressed
    img = cv2.resize(img,(1020,720))
    cv2.imshow("Imagen", img)
    cv2.waitKey(0)

    # We close the window
    cv2.destroyAllWindows()
