
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

R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(R_gripper2base, t_gripper2base, R_target2cam, t_target2cam)

# output results
print(R_cam2gripper)
print("---------------")
print(t_cam2gripper)
    



