# Smart Security Camera
Developer - Rohit Dhuri

## Description
A smart security camera with an android application which offers features such as -  
- Instant notifications realted to movement in front of the camera.  
- Intruder detection using face recognition and notification.  
- Activity logs, User login and live streaming (Live streaming feature is incomplete and may not work sometimes).

## Setup
1. Install the apk file found in the AndroidApplication/ in you android device.
2. Put all the files found in RaspberryPi/ into a single folder on your RaspberryPi
3. Change the path for RegisteredFaces according to your system directory in the Draft.py file.
4. Install vlc for streaming on the RaspberryPi using command "sudo apt-get install vlc".
5. Your RaspberryPi must have the PIR motion sensor and a camera module connected(use respective GPIO pins).
6. Ensure that the firebase instance is working. If not create your own realtime firebase database instance and replace the old access link.
7. Run the Draft.py file. 

## Software Stack
- RaspberryPi (Raspian OS).  
- Python3 with Sublime text as the IDE.  
- Android Studio to make the android application using Java.  
- Google Firebase for communication between RaspberryPi and Android device.  
- Firebase Realtime Databse for storing activity logs.  
- VLC for streaming frames.  

## References
1. https://raspberry-projects.com/pi/pi-hardware/raspberry-picamera/streaming-video-using-vlc-player
2. https://pypi.org/project/face-recognition/
3. https://firebase.google.com/docs/database

## Date: 12/06/2020