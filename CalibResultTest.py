import numpy as np
import cv2
import glob

def drawAxis(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(9,6,0)
objp = np.zeros((7*10,3), np.float32)
objp[:,:2] = np.mgrid[0:10,0:7].T.reshape(-1,2)


calibFile = cv2.FileStorage("calibData.xml", cv2.FILE_STORAGE_READ)
cmnode = calibFile.getNode("cameraMatrix")
mtx = cmnode.mat()
dcnode = calibFile.getNode("distCoeff")
dist = dcnode.mat()

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

# start camera capture work
cap = cv2.VideoCapture(0)

while(True):
    # get a frame
    ret, frame = cap.read()
    if not ret:
        print("Can't read a frame data")
        break

    gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (10,7),None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

        # Find the rotation and translation vectors.
        _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

        frame = drawAxis(frame, corners2, imgpts)


    # display the captured image
    cv2.imshow('Result Video',frame)

    # handle key inputs
    pressedKey = (cv2.waitKey(1) & 0xFF)
    if pressedKey == ord('q'):
        break

# for fname in images:
#     img = cv2.imread(fname)
#     gray = cv2.cvtColor(img,  cv2.COLOR_BGR2GRAY)
#     ret, corners = cv2.findChessboardCorners(gray, (10,7),None)

#     if ret == True:
#         corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
 
#         # Find the rotation and translation vectors.
#         _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
 
#         # project 3D points to image plane
#         imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
 
#         img = drawAxis(img, corners2, imgpts)
#         cv2.imshow('Images with Axis',img)
#         k = cv2.waitKey()




# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
