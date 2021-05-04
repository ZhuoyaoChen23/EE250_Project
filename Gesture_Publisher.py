import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt

# initialize hand tracking and drawing functions
cap = cv2.VideoCapture(0) # choose 0 for builtin webcam
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

gesture_cache = '' # variable that records the last history gesture

#Default message callback for CONNACK response
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# setup MQTT broker connection
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()

# Note on library's coordinate system: the higher a point locates on a frame means the smaller its y coordinate is
def palm_closed(lm_ls):

    # lm_ls[landmark_id][coordinate_choice]
    # the first index (ranges from 0 to 20) indicates which landmark is it among all 21 landmarks
    # the second index (0 or 1) points to the x or y coordinate of a landmark

    tip_coords = [lm_ls[8][1],lm_ls[12][1],lm_ls[16][1],lm_ls[20][1]] # list of all fingertips' y coordinates
    pip_coords = [lm_ls[6][1],lm_ls[10][1],lm_ls[14][1],lm_ls[18][1]] # list of all pip joints' y coordinates
    if pip_coords < tip_coords: # if every finger's pip joint is higher than fingertip
        return True # all fingers are curled, then palm is closed
    else:
        return False
def palm_open(lm_ls):
    # if every finger's fingertip is higher than pip joint
    if (lm_ls[6][1] > lm_ls[8][1]) and (lm_ls[10][1] > lm_ls[12][1]) and (lm_ls[14][1] > lm_ls[16][1]) and (lm_ls[18][1] > lm_ls[20][1]):
        return True # all fingers are open, then palm is open
    else:
        return False

def gesture_one(lm_ls):
    # if index finger's finger tip (landmark No.8) is higher than pip (landmark No.6)
    # while other fingers' pips are higher than tips
    # it means index finger is open, other fingers are curled
    if (lm_ls[8][1] < lm_ls[6][1]) and (lm_ls[10][1] < lm_ls[12][1]) and (lm_ls[14][1] < lm_ls[16][1]) and (lm_ls[18][1] < lm_ls[20][1]):
        return True # hand gesture number one is detected
    else:
        return False
def gesture_two(lm_ls):
    # if index and middle finger's finger tips (landmark No.8, No.12) are higher than pips (landmark No.6, No.10)
    # while other fingers' pips are higher than tips
    # it means index and middle finger are open, other fingers are curled
    if (lm_ls[8][1] < lm_ls[6][1]) and (lm_ls[12][1] < lm_ls[10][1]) and (lm_ls[14][1] < lm_ls[16][1]) and (lm_ls[18][1] < lm_ls[20][1]):
        return True # hand gesture number two is detected
    else:
        return False

while True:
    # set up webcam
    success, img = cap.read() # read webcam input to image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert image to RGB image
    results = hands.process(imgRGB)

    lm_pos = [] # list used to store coordinates of all landmarks
    if results.multi_hand_landmarks: # if hand is detected
        Tracked_Hand = results.multi_hand_landmarks[0]
        for landmark, landmark_coor in enumerate(Tracked_Hand.landmark):  # loop through all 21 landmarks on the tracked hand
            # refer to figure 2.21 for landmarks meaning (https://google.github.io/mediapipe/solutions/hands.html)
            image_height, image_width, _ = img.shape # extract video frame's pixel height and width
            landmark_x = int(landmark_coor.x*image_width) # convert landmark's raw x coordinate to pixel coordinate
            landmark_y = int(landmark_coor.y*image_height) # convert landmark's raw y coordinate to pixel coordinate
            lm_pos.append([landmark_x, landmark_y]) # store (x,y) of a landmark to the list of all landmarks' position
        mpDraw.draw_landmarks(img, Tracked_Hand, mpHands.HAND_CONNECTIONS)  # draw landmarks on the video frame

        # Hand gesture recognition
        if palm_closed(lm_pos): # when close palm is detected
            if gesture_cache != 'Close': # if this gesture is different from the previous one
                # Note: only update the gesture when a new gesture is detected
                #   this lowers the update frequency to broker and simplifies output
                print('Close Palm')
                gesture_cache = 'Close'
                client.publish("zhuoyaoc/LED_control", gesture_cache)  # publish gesture to broker
        elif palm_open(lm_pos): # when open palm is detected
            if gesture_cache != 'Open': # if this gesture is different from the previous one
                print('Open palm')
                gesture_cache = 'Open'
                client.publish("zhuoyaoc/LED_control", gesture_cache)  # publish gesture to broker
        else: # if palm isn't open nor closed
            if gesture_one(lm_pos): # when number gesture one is detected
                if gesture_cache != 'One': # if this gesture is different from the previous one
                    print('finger pose 1')
                    gesture_cache = 'One'
                    client.publish("zhuoyaoc/LED_control", gesture_cache)  # publish to broker
            elif gesture_two(lm_pos): # when number gesture two is detected
                if gesture_cache != 'Two': # if this gesture is different from the previous one
                    print('finger pose 2')
                    gesture_cache = 'Two'
                    client.publish("zhuoyaoc/LED_control", gesture_cache)  # publish to broker
    cv2.imshow("Image", img) # display the annotated video frame
    cv2.waitKey(1) # 1 ms delay