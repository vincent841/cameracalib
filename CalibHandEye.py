
import numpy as np
import cv2


R_gripper2base = []
t_gripper2base = []
R_target2cam = []
t_target2cam = []
#R_cam2gripper = []
#t_cam2gripper = []

handEyeInput = cv2.FileStorage("./handEyeSample.yml", cv2.FILE_STORAGE_READ)
fileNode = handEyeInput.root()

for key in fileNode.keys():
    ymlnode = handEyeInput.getNode(key)
    ymlmtx = ymlnode.mat()

    if key.find("target2cam") >= 0:
        rotataion = ymlmtx[0:3, 0:3]
        R_target2cam.append(rotataion)
        translation = ymlmtx[0:3, 3]
        t_target2cam.append(translation)

    if key.find("gripper2base") >= 0:
        rotataion = ymlmtx[0:3, 0:3]
        R_gripper2base.append(rotataion)
        translation = ymlmtx[0:3, 3]
        t_gripper2base.append(translation)        

#test codes 




methodHE = [cv2.CALIB_HAND_EYE_TSAI, cv2.CALIB_HAND_EYE_PARK, cv2.CALIB_HAND_EYE_HORAUD, cv2.CALIB_HAND_EYE_ANDREFF, cv2.CALIB_HAND_EYE_DANIILIDIS]

for mth in methodHE:
    R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(R_gripper2base, t_gripper2base, R_target2cam, t_target2cam, None, None, mth)
    cv2.calibrateHandEye(R_gripper2base, t_gripper2base, R_target2cam, t_target2cam, None, None, mth)
    # output results
    print("--------------------------------------")
    print("Method %d" % mth)
    print(R_cam2gripper)
    print(t_cam2gripper)
    print("--------------------------------------")


    



