
import numpy as np
import cv2
import glob

def saveCalibData(mtx, dist, rvecs, tvecs):
    calibFile = cv2.FileStorage("calibData.xml", cv2.FILE_STORAGE_WRITE)
    calibFile.write("cameraMatrix", mtx)
    calibFile.write("distCoeff", dist)
    
    #rotation_matrix = np.zeros(shape=(3,3))
    iter = 0
    for rvec in rvecs:
        #cv2.Rodrigues(rvec, rotation_matrix)
        #calibFile.write("rvec" + str(iter), rotation_matrix)
        calibFile.write("rvec" + str(iter), rvec)
        iter+=1
    iter = 0
    for tvec in tvecs:
        calibFile.write("tvec" + str(iter), tvec)
        iter+=1
    calibFile.release()

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

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# input directory name 
dirInput = input('Directory Name: ')
#dirInput = 'calibimgs'

# get image file names
images = glob.glob('./' + dirInput + '/*.jpg')

for fname in images:
    print(fname)
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (10,7),None)

    # If found, add object points, image points (after refining them)
    if ret == True:

        # show the original image
        cv2.imshow('Images',img)
        cv2.waitKey(1000)

        # append the set of object points like (0,0,0), (1,0,0), (2,0,0), ...
        objpoints.append(objp)

        # refine corners coordinates
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (10,7), corners2,ret)
        cv2.imshow('Images', img)
        cv2.waitKey()

# start camera calibartion
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# save calibration data to the specific xml file
saveCalibData(mtx, dist, rvecs, tvecs)

# project 3D Axis to each image

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,  cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (10,7),None)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
 
        # Find the rotation and translation vectors.
        _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
 
        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
 
        img = drawAxis(img, corners2, imgpts)
        cv2.imshow('Images with Axis',img)
        k = cv2.waitKey()

cv2.destroyAllWindows()
