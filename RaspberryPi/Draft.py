import RPi.GPIO as GPIO
import time
import face_recognition
import picamera
import numpy as np
import os
import sys
from firebase import firebase
from time import ctime

if len(sys.argv) ==2:
    pid = sys.argv[1]
    os.system(f'kill -9 '+str(pid))


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(11, GPIO.OUT)         #LED output pin
GPIO.output(11, 0)

#Firebase setup
firebase = firebase.FirebaseApplication("https://iot-project2-d9b1d.firebaseio.com/", None)
#firebase = firebase.FirebaseApplication("https://iotfinal-83f06-default-rtdb.firebaseio.com/", None)
firebase.put('App',"stream", "off");

# Enabling camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
output = np.empty((480, 640, 3), dtype=np.uint8)
scan_time = 3
index = 0
t = 5
stream_once = 1

def init_camera():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)

print("Loading registered face image(s)")
path = '/home/pi/Desktop/face_recog_example/registered_faces'
files = os.listdir(path)
registered_images = []
registered_names = []


for f in files:
    registered_images.append(face_recognition.load_image_file("registered_faces/"+f))
    registered_names.append(f[:-4])


print(registered_names)

# Encoding all the registered faces
registered_face_encodings = []
for image in registered_images:
    registered_face_encodings.append(face_recognition.face_encodings(image)[0])
 
    
# Initialize some variables
face_locations = []
face_encodings = []
print("Starting Detection")
while True:
    
    if firebase.get('/App', 'stream') == "on":
        camera.close()
        os.system(f'python3 secondary.py '+ str(os.getpid()))
        
    i=GPIO.input(7)
    if i==0: #When output from motion sensor is LOW
        #print ("No intruders",i)
        GPIO.output(11, 0) #Turn OFF LED
        time.sleep(0.1)

    elif i==1: #When output from motion sensor is HIGH
        
        if firebase.get('/App', 'stream') == "on":
            camera.close()
            os.system(f'python3 secondary.py '+ str(os.getpid()))
            
        
        print ("Motion detected",i)
        GPIO.output(11, 1) #Turn ON LED
        db_result = firebase.post('App/Movement', {'Index': index , 'time': ctime() })
        index=index+1
        # Start face recognition
        i=0;
        while i < scan_time:
            i=i+1
            print("Capturing image.")
            # Grab a single frame of video from the RPi camera as a numpy array
            camera.capture(output, format="rgb")

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(output)
            print("Found {} faces in image.".format(len(face_locations)))
            face_encodings = face_recognition.face_encodings(output, face_locations)

            # Loop over each face found in the frame to see if it's someone we know.
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                results = face_recognition.compare_faces(registered_face_encodings, face_encoding)
                match = None

                if True in results:
                    match = registered_names[results.index(True)]
                
                if match == None:
                    print("Unknown face found!")
                    db_result = firebase.post('App/Faces',{'Identity': 'Unknown' , 'Time': ctime() })
                else:   
                    print("I see someone named {}!".format(match))
                    db_result = firebase.post('App/Faces',{'Identity':match , 'Time': ctime() })
        print("Cooldown for 5 seconds")
        time.sleep(t)