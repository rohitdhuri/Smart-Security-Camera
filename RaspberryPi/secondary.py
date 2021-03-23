import os
import sys
from firebase import firebase
import signal

firebase = firebase.FirebaseApplication("https://iot-project2-d9b1d.firebaseio.com/", None)

if len(sys.argv) == 2:
    pid = sys.argv[1]
    os.system(f'kill -9 '+str(pid))

#os.system(f'mkdir test'+str(pid))
f = open("stream.sh","r")
str = f.read()
os.system(str)

while firebase.get('/App', 'stream') == "on":
    print("Streaming !!!!")
    if firebase.get('/App', 'stream') == "off":
        os.system(f'python3 Draft.py '+ str(os.getpid()))
    
os.system(f'python3 Draft.py '+ str(os.getpid()))


















#print(f'OldPid killed : '+ str(pid))
#os.system('python3 Draft.py')