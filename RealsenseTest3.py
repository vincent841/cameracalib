import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipe_profile = pipeline.start(config)

curr_frame = 0

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Intrinsics & Extrinsics
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
        depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(
            color_frame.profile)

        print(color_intrin)

        # print(depth_intrin.ppx, depth_intrin.ppy)

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # focusing on a (320, 120) pixel
        depth = depth_frame.get_distance(320, 120)
        depth_point = rs.rs2_deproject_pixel_to_point(depth_intrin, [320, 120], depth)
        text = "%.5lf, %.5lf, %.5lf\n" % (depth_point[0], depth_point[1], depth_point[2])
        #print(text)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(color_image, "[0] 3D Coord:" + text, (0,64), font, 1, (0,255,0),1,cv2.LINE_AA)
        cv2.rectangle(color_image, (319, 119), (321, 121), (255, 0, 0), 2)      

        # focusing on a (320, 240) pixel
        depth = depth_frame.get_distance(320, 239)
        depth_point = rs.rs2_deproject_pixel_to_point(depth_intrin, [320, 239], depth)
        text = "%.5lf, %.5lf, %.5lf\n" % (depth_point[0], depth_point[1], depth_point[2])
        #print(text)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(color_image, "[1] 3D Coord:" + text, (0,96), font, 1, (0,255,0),1,cv2.LINE_AA)
        cv2.rectangle(color_image, (319, 238), (321, 240), (255, 0, 0), 2)

        # focusing on a (320, 360) pixel
        depth = depth_frame.get_distance(320, 360)
        depth_point = rs.rs2_deproject_pixel_to_point(depth_intrin, [320, 360], depth)
        text = "%.5lf, %.5lf, %.5lf\n" % (depth_point[0], depth_point[1], depth_point[2])
        #print(text)
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(color_image, "[2] 3D Coord:" + text, (0,128), font, 1, (0,255,0),1,cv2.LINE_AA)
        cv2.rectangle(color_image, (319, 359), (321, 361), (255, 0, 0), 2)            

         # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

        curr_frame += 1
finally:
    # Stop streaming
    pipeline.stop()

cv2.destroyAllWindows()    