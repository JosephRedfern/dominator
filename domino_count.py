import numpy as np
import cv2

from multiprocessing.pool import ThreadPool
from collections import deque

def video_parse(input_video = None, output_video = None, display = False):
    #Get capture object and read frame
    if input_video is not None:
        cap = cv2.VideoCapture(input_video)
    else:
        cap = cv2.VideoCapture(0)

    # Space for opencv setup

    #Generate output objects if is required
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out_v = None
    if output_video is not None:
        out_v = cv2.VideoWriter(output_video,fourcc, 20.0, (int(previous_frame.shape[1]),int(previous_frame.shape[0])))

    ## Generate a queue for the processes
    n_threads = cv2.getNumberOfCPUs()
    pool = ThreadPool(processes = n_threads)

    pending_frames = deque()

    ## While the video is running
    while(cap.isOpened()):
        # Unload the ready frames
        while len(pending_frames) > 0 and pending_frames[0].ready():
            #Get the completed job
            res = pending_frames.popleft().get()

            #Write out the file to video if requested
            if out_va is not None:
                out_va.write(res)

            #Display ready frame
            if display:
                cv2.imshow(' Frame ', res)

        #If there are approx threads free, get more jobs
        if len(pending_frames) < n_threads:
            ## Generate the new job
            ret, frame = cap.read()
            if ret == False:
                break

            # drawing componenet to the fraem - only the compoenents not culled
            task = pool.apply_async(process_frame, (frame.copy()))
            pending_frames.append(task)

    # Clean up the used elements
    if out_v is not None:
        out_v.release()

    cap.release()
    cv2.destroyAllWindows()


def process_frame(frame):
    ### Just convert to grey for now
    cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    return img



if __name__ == "__main__":
    video_parse(input_video = './test_video.mp4', display=True)

