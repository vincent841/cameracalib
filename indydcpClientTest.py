
import indydcp_client as indycli
import numpy as np 
import sys

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
    print ("Task Pos: ")
    print (task_pos)    

def indyMoveToTask(t_pos):
    print('### Test: MoveToT() ###')
    indy.task_move_to(t_pos)    
    
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

    _server_ip = "192.168.207.2"
    _name = "Indy5"

    indy = indyConnect(_server_ip, indycli.ROBOT_INDYRP2)

    indy.go_home()

    while(True):

        indyPrintJointPosition()
        indyPrintTaskPosition()
        
        pressedKey = (cv2.waitKey(250) & 0xFF)
        # handle key inputs
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('1'):
            t_pos1 = [0.5, -0.2, 0.3, 180, -10, 180]
            indyMoveToTask()
        elif pressedKey == ord('2'):
            t_pos1 = [2.0, -0.2, 0.3, 180, -10, 180]
            indyMoveToTask()


    # Disconnect
    indy.disconnect()
    print("Test finished")
    