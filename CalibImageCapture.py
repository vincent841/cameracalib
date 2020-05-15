
import numpy as np
import cv2
import os
import datetime

# create a directory to save captured images 
def makeFrameImageDirectory():
    now = datetime.datetime.now()
    dirString = now.strftime("%Y%m%d%H%M%S")
    try:
        if not(os.path.isdir(dirString)):
            os.makedirs(os.path.join(dirString))
    except OSError as e:
        print("Can't make the directory: %s" % dirFrameImage)
        raise
    return dirString

# start camera capture work
cap = cv2.VideoCapture(0)

dirFrameImage = makeFrameImageDirectory()
#dirFrameImage = 'calibimgs'

print("press 'c' to capture an image or press 'q' to exit...")

iteration = 0
while(True):
    # get a frame
    ret, frame = cap.read()
    if not ret:
        print("Can't read a frame data")
        break

    # display the captured image
    cv2.imshow('Capture Images',frame)
    pressedKey = (cv2.waitKey(1) & 0xFF)

    # handle key inputs
    if pressedKey == ord('q'):
        break
    elif pressedKey == ord('c'):
        cv2.imwrite(os.path.join(dirFrameImage, str(iteration) + '.jpg'),frame)
        print('Image caputured - ' + os.path.join(dirFrameImage, str(iteration) + '.jpg'))

        #TODO: get robot's rotation & translation matrix here
        #...

        iteration+=1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()