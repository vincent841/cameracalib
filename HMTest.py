import indydcp_client as indycli
import numpy as np 
import sys
from time import sleep
import cv2
import math

# rpw unit: degree
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
        p = math.atan2(-H[2,0],math.sqrt(H[0,0]*H[0,0]+H[1,0]*H[1,0]))
        w = math.atan2(H[1,0],H[0,0])
        r = math.atan2(H[2,1],H[2,2])    
    return [x, y, z, r*180/math.pi, p*180/math.pi, w*180/math.pi]


hm = np.array([[-0.6484945560472715, 0.7588883777053825, -0.05952512881754177, -0.09061736124264554], [0.7611366063389998, 0.6475911239041057, 
-0.03601114732090388, -0.6687733681469619], [0.01121950390181825, -0.06865978753469798, -0.9975770427931304, 0.07609749637689898], [0, 0, 0, 1]])
xyzabc = [-0.09064515960284498, -0.6685702677827611, 0.07567205103501873, -176.08612962588248, -0.6780892276157752, 130.42940636697082]

hmcal = convertXYZABCtoHM(xyzabc)
print(hmcal)

xyzabc_calc = convertHMtoXYZABC(hmcal)
print()
print(xyzabc_calc)

print()
print(np.dot(hm, np.array([0,0,0,1]).T))

hminv = np.linalg.pinv(hm)
print()
print(np.dot(hminv, np.array([-0.09064515960284498, -0.6685702677827611, 0.07567205103501873, 1]).T))