import cv2
from imutils.video import VideoStream
from imutils.video import FPS
# importing os module 
import os


print('Enter your name:')
x = input()
# Directory 
directory = "{}".format(x)

# Parent Directory path 
parent_dir = "C:/Users/rdhen/OneDrive/Desktop/perspectico/opencv-face-recognition/dataset"
path = os.path.join(parent_dir, directory) 
os.mkdir(path) 
print("Directory '% s' created" % directory) 


vs = VideoStream(src=0).start()
fps = FPS().start()
img_counter = 0

while True:
    frame = vs.read()
    cv2.imshow("making dataset", frame)
    img_name = "dataset/{}/0000{}.png".format(x,img_counter)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))
    img_counter += 1
    if img_counter == 400:
        break
    
    key = cv2.waitKey(1) & 0xFF

# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    
fps.stop()        
cv2.destroyAllWindows()
vs.stop()