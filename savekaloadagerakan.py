import cv2, time
import os
import numpy as np
from datetime import datetime

FILE_OUTPUT = "video_" + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
sdThresh = 10
cv2.namedWindow('frame')
cv2.namedWindow('dist')
i = 0

# Cek dan menghapus file video
# You cant have the duplicate of an already-existed file or it will go through an error
# if os.path.isfile(FILE_OUTPUT + ".mp4"):
#     os.remove(FILE_OUTPUT + ".mp4")

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter(FILE_OUTPUT + ".mp4", fourcc, 10.0, (640,480))


t0 = time.time()

def distMap(frame1, frame2):
    # outputs pythagorean distance between two frames
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

# source kamera nya
# camera = cv2.VideoCapture('rtsp://admin:@192.168.1.6:554')
camera = cv2.VideoCapture(0)

check1, frame1 = camera.read()
check2, frame2 = camera.read()

# Looping untuk mengambil gambar

while True:
    # frame object
    check3, frame3 = camera.read()
    gerakan = False
    if check3 == True:
        # mirroring kamera biar gak kebalik
        frame3 = cv2.flip(frame3,1)

        rows, cols, _ = np.shape(frame3)
        dist = distMap(frame1, frame3)

        frame1 = frame2
        frame2 = frame3
    
        # Gaussian smoothing
        mod = cv2.GaussianBlur(dist, (9,9), 0)
    
        # Thresholding
        _, thresh = cv2.threshold(mod, 100, 255, 0)
    
        # menghitung std dev test
        _, stDev = cv2.meanStdDev(mod)

        # menampilkan frame saat merekam
        cv2.imshow("Merekam", frame2)
       # cv2.imshow("Frame 1", frame1)
       # cv2.imshow("Frame 2", frame2)
        # cv2.imshow("Frame 3", frame3)
    else:
        break

    if stDev > sdThresh:
        # save video
        image = cv2.resize(frame2, (640, 480))
        output.write(image)
        gerakan = True


        # print("Ada pergerakan");


    # For playing
    # key = cv2.waitKey(1)
    # if key == 27 : # esc
    #    break

    t1 = time.time()  # current time
    durasi = t1 - t0  # diff
    if durasi > 60:
        break
    elif cv2.waitKey(25) and 0xFF == ord('q'):
        break
    # else:
    #    objek2.append(print())

# mematikan kamera
camera.release()

output.release()

cv2.destroyAllWindows()