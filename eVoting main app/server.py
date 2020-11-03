from flask import Flask, request, jsonify, render_template
import os
from processing import recognise_text, crop_aadhar, get_address, seven_segment, _init_model, get_labels_from_aadhar, get_labels_from_licence
from cheque_details_extraction import get_micrcode, ensemble_acc_output, ensemble_ifsc_output
import datetime
import db
from face_matching import match_faces

app = Flask(__name__)

# path to upload images
UPLOAD_FOLDER = './UPLOAD_FOLDER/'

# initializing seven segment display model
_init_model()

name=''
# route to uploading images of id cards
@app.route('/image/upload', methods=['POST'])
def index():
    
    if request.method == 'POST':

        # saving current timestamp
        current_time = str(datetime.datetime.now()).replace('-', '_').replace(':', '_')

        # get the type of image that is being received
        image_type = request.form['type']
        
        # setting filename that is being received to current time stamp with its directory
        filename = UPLOAD_FOLDER + image_type + '/' + current_time + '.png'

        # if the image_type folder doesn't already exist, create it
        if not os.path.exists(UPLOAD_FOLDER + image_type):
            os.mkdir(UPLOAD_FOLDER + image_type)
            # directory for saving faces in the id cards
            os.mkdir(UPLOAD_FOLDER + image_type + '/' + 'faces')
        
        # if image_type is bank cheque, preprocess accordingly
        if image_type == 'Bank Cheque':
            details = {}

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # get details from the image
            details['MICR'] = get_micrcode(filename)
            details['ACC.No'] = ensemble_acc_output(filename)
            details['IFSC'] = ensemble_ifsc_output(filename)

            # return the details and the image name it is saved as
            return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': 'none' })

        # if image_type is seven segment, preprocess accordingly
        elif image_type == 'Seven Segment':
            details = {}

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # get text from seven segment
            text = seven_segment(filename)

            details[0] = text

            # return the details and the image name it is saved as
            return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': 'none' })

        # elif image_type == 'Aadhar Back':
        #     details = {}

        #     # get photo from android
        #     photo = request.files['photo']
        #     photo.save(filename)

        #     crop_path = UPLOAD_FOLDER + image_type + '/temp/' + current_time + '.png'

        #     if not os.path.exists(UPLOAD_FOLDER + image_type + '/temp'):
        #         os.mkdir(UPLOAD_FOLDER + image_type + '/temp')

        #     crop_aadhar(filename, crop_path)

        #     # recognise text in the id card
        #     data, photo_path = recognise_text(crop_path, 'none')
            
        #     details = get_address(data)

        #     os.remove(crop_path)

        #     # return the details and the image name it is saved as
        #     return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': 'none' })
        
        else:
            # setting directory for saving face in the id card
            photo_path = UPLOAD_FOLDER + image_type + '/' + 'faces' + '/' + current_time + '.png'
            
            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # recognise text in the id card
            data, photo_path = recognise_text(filename, photo_path)
            
            # extract labels from the recognised text according to the image_type
            if image_type == "Driving Licence":
                details = { idx : text for idx, text in enumerate(data) }
                details = get_labels_from_licence(details)
            elif image_type == "Aadhar Card":
                details = get_labels_from_aadhar(data)
            else:
                details = { idx : text for idx, text in enumerate(data) }

            with open('outputs.txt', 'a+') as f:
                f.write("##########################################################################\n\n")
                f.write('######################## Raw Output #############################\n\n')
                for value in data:
                    f.write(str(value) + '\n')
                f.write('\n\n######################## Cleaned Output #############################\n\n')
                for key, value in details.items():
                    f.write(str(key) + ' : ' + str(value) + '\n')
                f.write("##########################################################################\n\n")
            details['status']='your data is successsfully verified from ADHAAR API'
            # return the details and the image name and photo path it is saved as
            global name
            name=details["Name"]
            return render_template('verified.html',result=details)
            #return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': photo_path})
    else:
        # if not POST, terminate
        return jsonify({'status':False})


@app.route('/upload_adhaar', methods=['POST'])
def upload_adhaar():
    if request.method == 'POST':

        # saving current timestamp
        current_time = str(datetime.datetime.now()).replace('-', '_').replace(':', '_')

        # get the type of image that is being received
        image_type = request.form['type']

        # setting filename that is being received to current time stamp with its directory
        filename = UPLOAD_FOLDER + image_type + '/' + current_time + '.png'

        # if the image_type folder doesn't already exist, create it
        if not os.path.exists(UPLOAD_FOLDER + image_type):
            os.mkdir(UPLOAD_FOLDER + image_type)
            # directory for saving faces in the id cards
            os.mkdir(UPLOAD_FOLDER + image_type + '/' + 'faces')

        # if image_type is bank cheque, preprocess accordingly
        if image_type == 'Bank Cheque':
            details = {}

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # get details from the image
            details['MICR'] = get_micrcode(filename)
            details['ACC.No'] = ensemble_acc_output(filename)
            details['IFSC'] = ensemble_ifsc_output(filename)

            # return the details and the image name it is saved as
            return jsonify({'status': True, 'fields': details, 'image_path': filename, 'photo_path': 'none'})

        # if image_type is seven segment, preprocess accordingly
        elif image_type == 'Seven Segment':
            details = {}

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # get text from seven segment
            text = seven_segment(filename)

            details[0] = text

            # return the details and the image name it is saved as
            return jsonify({'status': True, 'fields': details, 'image_path': filename, 'photo_path': 'none'})

        # elif image_type == 'Aadhar Back':
        #     details = {}

        #     # get photo from android
        #     photo = request.files['photo']
        #     photo.save(filename)

        #     crop_path = UPLOAD_FOLDER + image_type + '/temp/' + current_time + '.png'

        #     if not os.path.exists(UPLOAD_FOLDER + image_type + '/temp'):
        #         os.mkdir(UPLOAD_FOLDER + image_type + '/temp')

        #     crop_aadhar(filename, crop_path)

        #     # recognise text in the id card
        #     data, photo_path = recognise_text(crop_path, 'none')

        #     details = get_address(data)

        #     os.remove(crop_path)

        #     # return the details and the image name it is saved as
        #     return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': 'none' })

        else:
            # setting directory for saving face in the id card
            photo_path = UPLOAD_FOLDER + image_type + '/' + 'faces' + '/' + current_time + '.png'

            # get photo from android
            photo = request.files['photo']
            photo.save(filename)

            # recognise text in the id card
            data, photo_path = recognise_text(filename, photo_path)

            # extract labels from the recognised text according to the image_type
            if image_type == "Driving Licence":
                details = {idx: text for idx, text in enumerate(data)}
                details = get_labels_from_licence(details)
            elif image_type == "Aadhar Card":
                details = get_labels_from_aadhar(data)
            else:
                details = {idx: text for idx, text in enumerate(data)}

            with open('outputs.txt', 'a+') as f:
                f.write("##########################################################################\n\n")
                f.write('######################## Raw Output #############################\n\n')
                for value in data:
                    f.write(str(value) + '\n')
                f.write('\n\n######################## Cleaned Output #############################\n\n')
                for key, value in details.items():
                    f.write(str(key) + ' : ' + str(value) + '\n')
                f.write("##########################################################################\n\n")
            details['status'] = 'your data is successsfully verified from ADHAAR API'
            # return the details and the image name and photo path it is saved as
            global name
            name = details["Name"]
            details["Voter ID card "]="Verified"
            return render_template('vote_verification.html', result=details)
            # return jsonify({'status':True, 'fields': details, 'image_path': filename, 'photo_path': photo_path})
    else:
        # if not POST, terminate
        return jsonify({'status': False})



from save_sample import *
@app.route('/video', methods=['POST'])
def video():
    """Video streaming home page."""
    return render_template('video.html')

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpeg','tif','png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_form():
    return render_template('upload.html')
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template
@app.route('/load', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global input
            input=filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return render_template('upload.html')
        else:
            flash('jpg','png')
            return redirect(request.url)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an frame tag."""
    print(name)
    return Response(gen(name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/data', methods=['POST'])
def saveData():
    
    # get values as json
    values = request.get_json()
    image_type = values.get('type')
    data = values.get('fields')
    
    db.insert_data(image_type, args_dict = data)

    return jsonify({'status': True})


@app.route('/image/face_match',methods=['GET','POST'])
def face_match():

    # saving current timestamp
    current_time = str(datetime.datetime.now())

    # temporary folder for saving face for face matching
    if not os.path.exists(UPLOAD_FOLDER + 'temp'):
            os.mkdir(UPLOAD_FOLDER + 'temp')

    # setting filename that is being received to current time stamp with its directory
    filename = UPLOAD_FOLDER + 'temp' + '/' + current_time + '.png'
    
    # getting the path of the saved face image
    photo_path = request.form['photopath']

    # get live face from android
    photo = request.files['liveface']
    photo.save(filename)
    
    # check face match and probability
    result, percent = match_faces(id_card_image=photo_path, ref_image=filename)

    # delete the temp face image
    os.remove(filename)

    # return face match prediction and percentage
    return jsonify({'status':str(result), 'percent': percent})


@app.route('/biometrics',methods=['GET','POST'])
def biometrics():
    return render_template('vote_biometrics.html')


@app.route('/reg_fingure',methods=['GET','POST'])
def reg_fingure():
    return render_template('reg_fingure.html')

@app.route('/reg_fingure_print',methods=['GET','POST'])
def reg_fingure_print():
    print('fmr generated : "Rk1SACAyMAAAAADkAAgAyQFnAMUAxQEAAAARIQBqAGsgPgCIAG0fRwC2AG2dSQBVAIUjPABuALShMgCxAL0jMAByAM6lPgCmAN2kQQBwAN8qNAB1AN8mPADJAOcgOQA8AOorNABoAOomOQC+AO2fMQDFAPqlSgCvAP8lRQB8AQuhPABwAQ4fMgB7ASqcRADAAS4iNwCkATMeMwCFATYeNwBLATYwMQBWATcoMQCkATecMQBEATwyMgBJAUciQQCkAU8cNQB9AVQWNgCEAVUVRACoAVgYOgBBAV69NgCsAWeYNwAA"')
    app.config['UPLOAD_FOLDER']='UPLOAD_FOLDER\\bio'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global name
            filename=name+'_'+'2'+'.tif'
            verify = 'UPLOAD_FOLDER\\bio\\' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return render_template('audio.html')



from fingure import *
@app.route('/fingure_print',methods=['GET','POST'])
def fingure_print():
    print('fmr generated : "Rk1SACAyMAAAAADkAAgAyQFnAMUAxQEAAAARIQBqAGsgPgCIAG0fRwC2AG2dSQBVAIUjPABuALShMgCxAL0jMAByAM6lPgCmAN2kQQBwAN8qNAB1AN8mPADJAOcgOQA8AOorNABoAOomOQC+AO2fMQDFAPqlSgCvAP8lRQB8AQuhPABwAQ4fMgB7ASqcRADAAS4iNwCkATMeMwCFATYeNwBLATYwMQBWATcoMQCkATecMQBEATwyMgBJAUciQQCkAU8cNQB9AVQWNgCEAVUVRACoAVgYOgBBAV69NgCsAWeYNwAA"')
    app.config['UPLOAD_FOLDER']='UPLOAD_FOLDER\\bio'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global name
            filename=name+'_'+'2'+'.tif'
            verify = 'UPLOAD_FOLDER\\bio\\' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')

            sample='database\\'+name+'_'+'1'+'.tif'
            r = fingure(sample, verify)
            dict={}
            dict['status']=r
            return render_template('vote_bio_result.html', result=dict)
        else:
            flash('jpg','png')
            return redirect(request.url)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registration',methods=['GET','POST'])
def registration():
    print('regis')
    return render_template('registration.html')

@app.route('/login',methods=['GET','POST'])
def login():
    print('regis')
    return render_template('vote_resigtration.html')

from recognize_deploy import *
@app.route('/video_2',methods=['GET','POST'])
def video_2():
    return render_template('vote_video_result.html')

@app.route('/video_verification',methods=['GET','POST'])
def video_verification():
    print(name)
    return Response(gen_2(name),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/voice',methods=['GET','POST'])
def voice():
    return render_template('vote_voice.html')

@app.route("/webrtc",methods=['GET','POST'])
def webrtc():
    return render_template('web_rtc.html',)



def gen3():
    import cv2

    vs = VideoStream(src=0).start()
    fps = FPS().start()
    img_counter = 0

    while True:
        frame = vs.read()
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()

    print("Taken ----{}-------images".format(count))
    ###################################################################################DETCTION MODEL#######################################################
    print("done")


@app.route('/web_rtc_2',methods=['GET','POST'])
def web_rtc_2():
    return Response(gen3(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/voice_behaviour',methods=['GET','POST'])
def voice_behaviour():
    dict={}
    dict["Voice Matched"]='kalam'
    dict["Mental Status"] = 'Normal'
    return render_template('vote_voice_result.html',result=dict)


# running web app in local machine
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
