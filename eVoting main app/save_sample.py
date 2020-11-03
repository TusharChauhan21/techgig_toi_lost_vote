import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import pickle
import time
import os
import json
import time
from imutils import paths
import numpy as np
import argparse
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from flask import Flask, render_template, Response, request

###################flask area######################################




def gen(name):
    from imutils.video import VideoStream
    from imutils.video import FPS
    import numpy as np
    import argparse
    import pickle
    import time
    import os
    import json
    import time
    from imutils import paths
    import numpy as np
    import argparse
    from sklearn.preprocessing import LabelEncoder
    from sklearn.svm import SVC
    ############################################################TAKING USER CREDENTIAL####################################################
    # print("enter name")

    x = name

    # Directory
    directory = "{}".format(x)

    user_name = x

    count = 600

    # Parent Directory path
    parent_dir = "dataset"
    try:
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
    except:
        pass

    vs = VideoStream(src=0).start()
    fps = FPS().start()
    img_counter = 0

    while True:
        frame = vs.read()
        img_name = "dataset/{}/0000{}.png".format(x, img_counter)
        cv2.imwrite(img_name, frame)
        # print("{} written!".format(img_name))
        img_counter += 1
        if img_counter == count:
            break

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # if the `q` key was pressed, break from the loop

    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()

    print("Taken ----{}-------images".format(count))
    ###################################################################################DETCTION MODEL#######################################################
    print("done")
    return render_template('audio.html')



















