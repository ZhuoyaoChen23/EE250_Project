# EE250_Project
README file for Zhuoyao Chen's EE250 End of Course Project - Gesture Control Lighting\
Team Member: Zhuoyao Chen (contact: zhuoyaoc@usc.edu)\
Demo Video:  
 + Google Drive: https://drive.google.com/file/d/1XOnISzc6WQa760zqFQrbMrbSSPDcgP7V/view?usp=sharing

 + YouTube: https://youtu.be/HRH77Hi3Be0

***User Instruction:*** 

1. **On your Laptop/Desktop equiped with a webcam:** 

   + compile and run "Gesture_Publisher.py" code\
      	***Notice:*** depends on the type of webcam, the user may need to change the port number in line 6 
        to either 0 or 1 to have the script be working

   Additional Libraries for Gesture_Publisher.py: 
  
   opencv-python\
   mediapipe\
   paho-mqtt

2. **On your Raspberry Pi:**

   + connect LCD to any I2C port, connect LED1 to port D3 and LED2 to port D4
   + compile and run "subscriber.py" code

   Additional Libraries for subscriber.py:

   ​		paho-mqtt

***Block Diagram:***\
![diagram](diagram/EE250%20Project.png)
