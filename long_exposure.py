#!/usr/bin/env python
# Modified by Medad Newman on 24 July 2018
"""
This code take a video and averages the frames of a video to simulate the long exposure. currently, the input and output paths
are hard coded

"""


import argparse
import cv2
import sys
import matplotlib.pyplot as plt
import time

timestamp = time.strftime("%b %d %Y %H %M %S")

class ProgressBar(object):
    def __init__(self, total, prefix='Progress:', suffix='Complete', decimals=2, bar_length=50):
        """
        It is used to show a progress bar.
        :param total: the total value of the progress bar (100%)
        :param prefix: the prefix show before the progress bar (default is 'Progress:')
        :param suffix: the suffix show after the progress bar (default is 'Complete')
        :param decimals: the number of decimal places
        :param bar_length: the length/width of the progress bar
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length

    def update(self, progress):
        """
        Function used to update the progress bar.
        :param progress: the current progress (should be lower than the total)
        """
        str_format = "{0:." + str(self.decimals) + "f}"
        percents = str_format.format(100 * (progress / float(self.total)))
        filled_length = int(round(self.bar_length * progress / float(self.total)))
        bar = '#' * filled_length + '-' * (self.bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.suffix))

        if progress >= self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()


class LongExposure(object):
    @staticmethod
    def run(video, output,n_frames, step=1, start_frame= 0):
        """
        The function used to run the long-exposure effect based on the video.
        :param video: the path to the video file
        :param output: the path to the output image file
        :param n_frames: the number of frames to merge into a single frame
        :param step: the step used to ignore some frames (optional)
        :param start_frame: The initial frame from which merging starts
        """

        # Initialize the RGB channel averages
        (r_avg, g_avg, b_avg) = (None, None, None)

        # Used to count the total number of selected frames
        selected_frames = 0

        print("[INFO] Opening video file pointer...")

        # Open a pointer to the video file
        stream = cv2.VideoCapture(video)

        print("[INFO] Computing frame averages...")

        # Set start frame
        stream.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Get the total number of frames to show the progress bar
        total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))-start_frame
        print("Total frames:",total_frames)

        # Get the frame rate
        fps = stream.get(cv2.CAP_PROP_FPS)

        print("Frame rate:",fps)

        # Single frame exposure time:
        print("Single frame exposure time:",1/fps, 'seconds')

        # Initialize the progress bar
        progress_bar = ProgressBar(total_frames)
        progress_bar.update(0)

        # Used to count the number of frames to update the progress bar
        frame_count = 0

        # Loop over all frames from the video file stream
        while True:
            # Grab the frame from the file stream
            grabbed, frame = stream.read()

            # If the frame was not grabbed, then we have reached the end of the file
            if not grabbed or frame_count > n_frames:
                break

            if frame_count % step == 0:
                # Split the frame into its respective channels
                # We need to convert it to float
                (B, G, R) = cv2.split(frame.astype("float"))

                # If the frame averages are None, initialize them
                if r_avg is None:
                    r_avg = R
                    b_avg = B
                    g_avg = G
                # Otherwise, compute the weighted average between the history
                # of frames and the current frames
                else:
                    r_avg = ((selected_frames * r_avg) + (1 * R)) / (selected_frames + 1.0)
                    g_avg = ((selected_frames * g_avg) + (1 * G)) / (selected_frames + 1.0)
                    b_avg = ((selected_frames * b_avg) + (1 * B)) / (selected_frames + 1.0)

                # Increment the total number of selected frames
                selected_frames += 1

            # Update the progress bar
            frame_count += 1
            progress_bar.update(frame_count)

        # Make sure that the progress bar state is 100%
        progress_bar.update(total_frames)

        # If we got at least one frame
        if selected_frames > 0:
            # Merge the RGB averages together and write the output image to disk
            # Here, we need to convert the value to uint8 to create the new image
            avg = cv2.merge([b_avg, g_avg, r_avg]).astype("uint8")


            cv2.imwrite(output, avg)
            plt.imshow(cv2.cvtColor(avg,cv2.COLOR_RGB2BGR))
            plt.title("Number of frames: "+str(n_frames))
            plt.suptitle("Exposure time:"+str(n_frames*1/fps)+" seconds\n"+"The start frame is frame {0} and end frame is frame {1}".format(start_frame,start_frame+n_frames))
            plt.savefig("Output images with labels/output figure {0}.png".format(timestamp))
            plt.show()


        else:
            print("[ERRO] No frames found...")

        # Release the stream pointer
        stream.release()


if __name__ == "__main__":
    import datetime

    # Construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-v", "--video", required=True, help="Path to input video file")
    # ap.add_argument("-o", "--output", required=True, help="Path to output 'long exposure' image")
    # ap.add_argument("-s", "--step", type=int, default=1, help="Step used to get the frames")
    # args = vars(ap.parse_args())

    # current date time

    # now = datetime.datetime.now()
    # print(now.strftime("%Y-%m-%d %H-%M"))


    #######################################################
    # Temporarily hard code the values to the code itself
    # Path for source video
    video = "E:/DCIM/105___01/MVI_1116.MOV"
    # video = "C:/Users/medad/Documents/University storage/High Altitude Ballooning/Gimbal construction/Youtube videos/gimbal footage.avi"

    # Path for output image
    output = "output_images/output {0}.png".format(timestamp)
    step = 1

    args = {"video": video, "output": output, "step": step}
    #######################################################


    # Run the long exposure algorithm passing the required parameters
    LongExposure.run(args["video"], args["output"],n_frames=24*3, step= args["step"],start_frame=100)
