
import indydcp_client as indycli
import numpy as np 
import sys
from time import sleep
import cv2
import math
import keyboard

# todo later..
# class indyDcpClinet:
#     serverIP = ""
#     clientName = ""

#     def __init__(self, servIP, cliName):
#         self.serverIP = servIP
#         self.clientName = cliName



def indyConnect(servIP, connName):
    # Connect
    obj = indycli.IndyDCPClient(servIP, connName)
    conResult = obj.connect()
    if conResult == False:
        print("Connection Failed")
    return obj

def indyPrintJointPosition():
    print('### Test: GetJointPos() ###')
    joint_pos = indy.get_joint_pos()
    print ("Joint Pos: ")
    print (joint_pos)    

def indyPrintTaskPosition():
    print('### Test: GetTaskPos() ###')
    task_pos = indy.get_task_pos()
    task_pos_mm = [task_pos[0]*1000.0, task_pos[1]*1000.0, task_pos[2]*1000.0,task_pos[3], task_pos[4], task_pos[5]]
    print ("Task Pos: ")
    print (task_pos_mm) 
    hm = convertXYZABCtoHM(task_pos)
    print(hm)

def indyMoveToTask(t_pos):
    print('### Test: MoveToT() ###')
    indy.task_move_to(t_pos)    

def convertXYZABCtoHM(xyzrpw):
    [x,y,z,r,p,w] = xyzrpw
    a = r*math.pi/180
    b = p*math.pi/180
    c = w*math.pi/180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)    
    H = np.array([[cb*cc, cc*sa*sb - ca*sc, sa*sc + ca*cc*sb, x],[cb*sc, ca*cc + sa*sb*sc, ca*sb*sc - cc*sa, y],[-sb, cb*sa, ca*cb, z],[0,0,0,1]])
    return H

def convertHMtoXYZABC(H):
    x = H[0,3]
    y = H[1,3]
    z = H[2,3]
    if (H[2,0] > (1.0 - 1e-10)):
        p = -pi/2
        r = 0
        w = math.atan2(-H[1,2],H[1,1])
    elif H[2,0] < -1.0 + 1e-10:
        p = pi/2
        r = 0
        w = math.atan2(H[1,2],H[1,1])
    else:
        p = math.atan2(-H[2,0],sqrt(H[0,0]*H[0,0]+H[1,0]*H[1,0]))
        w = math.atan2(H[1,0],H[0,0])
        r = math.atan2(H[2,1],H[2,2])    
    return [x, y, z, r*180/pi, p*180/pi, w*180/pi]



    
# # Get Task Position
# print('### Test: GetTaskPos() ###')
# task_pos = indy.get_task_pos()
# print ("Task Pos: ")
# print (task_pos)

# # Get Joint Position
# print('### Test: GetJointPos() ###')
# joint_pos = indy.get_joint_pos()
# print ("Joint Pos: ")
# print (joint_pos)

# # Move to Task
# print('### Test: MoveToT() ###')
# indy.task_move_to(task_pos)

# # Move to Joint
# print('### Test: MoveToJ() ###')
# indy.joint_move_to(joint_pos)







###############################################################################
# Test                                                                        #
###############################################################################
if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     print('{0} <Server IP> <Robot Name>'.format(sys.argv[0]))
    #     sys.exit()

    _server_ip = "192.168.1.207"
    _name = "NRMK-Indy7"

    indy = indyConnect(_server_ip, _name)
    indy.connect()
    
    indy.reset_robot()
    status = indy.get_robot_status()
    print("Resetting robot")
    print("is in resetting? ", status['resetting'])
    print("is robot ready? ", status['ready'])

    if( status['emergency'] == True):
        indy.stop_emergency()

    sleep(5)
    status = indy.get_robot_status()
    print("Reset robot done")
    print("is in resetting? ", status['resetting'])
    print("is robot ready? ", status['ready'])


    indy.direct_teaching(True)
    iteration = 0
    while(True):

        indyPrintTaskPosition()

        sleep(1)

        if keyboard.is_pressed("q"):
            print("You pressed q")
            break
        
        #pressedKey = (cv2.waitKey(500) & 0xFF)
        # handle key inputs


        # if pressedKey == ord('q'):
        #     break
        # elif pressedKey == ord('1'):
        #     t_pos1 = [0.5, -0.2, 0.3, 180, -10, 180]
        #     indyMoveToTask()
        # elif pressedKey == ord('2'):
        #     t_pos1 = [2.0, -0.2, 0.3, 180, -10, 180]
        #     indyMoveToTask()
        iteration +=1
        if(iteration > 10):
            break

    indy.direct_teaching(False)

    # Disconnect
    indy.disconnect()
    print("Test finished")
    