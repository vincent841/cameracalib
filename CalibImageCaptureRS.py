
import pyrealsense2 as rs
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

#Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

dirFrameImage = makeFrameImageDirectory()
#dirFrameImage = 'calibimgs'

print("press 'c' to capture an image or press 'q' to exit...")

iteration = 0

try:
    while(True):
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # display the captured image
        cv2.imshow('Capture Images',color_image)
        pressedKey = (cv2.waitKey(1) & 0xFF)

        # handle key inputs
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('c'):
            cv2.imwrite(os.path.join(dirFrameImage, str(iteration) + '.jpg'),color_image)
            print('Image caputured - ' + os.path.join(dirFrameImage, str(iteration) + '.jpg'))

            #TODO: get robot's rotation & translation matrix here
            #...

            iteration+=1
finally:
    # Stop streaming
    pipeline.stop()

cv2.destroyAllWindows()