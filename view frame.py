# Created by Medad Newman on 25 july 2018

import numpy as np
import matplotlib.pyplot as plt
import cv2

video_name = "C:/Users/medad/Documents/University storage/High Altitude Ballooning/Gimbal construction/Youtube videos/gimbal footage stabilised.avi"

video = cv2.VideoCapture(video_name) #video_name is the video being called

fps = video.get(cv2.CAP_PROP_FPS)
print(fps)

frame_no = 344
video.set(1, frame_no) # Where frame_no is the frame you want
ret, frame = video.read() # Read the frame
frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

plt.imshow(frame)
plt.show()