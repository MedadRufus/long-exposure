import cv2

video_name = "C:/Users/medad/Documents/University storage/High Altitude Ballooning/Gimbal construction/Youtube videos/gimbal footage stabilised.avi"
vidcap = cv2.VideoCapture(video_name)

success, image = vidcap.read()
count = 0
output_folder = "C:/Users/medad/PycharmProjects/HAB/LongExposureSimulation/single frames/gimbal footage stabilised"
while success:
    cv2.imwrite(output_folder+"/frame%d.jpg" % count, image)  # save frame as JPEG file
    success, image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1
