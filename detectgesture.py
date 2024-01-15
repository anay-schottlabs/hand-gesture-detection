import cv2
import threading
import time
import json
import training
import handtracking
import gesturerecognition

TRAINING_DATA_FILE_PATH = "trainingdata.json"
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
LOOP_DELAY = 2
MIN_MATCH_THRESHOLD = 500
GESTURE_PREP_DELAY = 2
capture = cv2.VideoCapture(0)
handDetector = handtracking.HandDetector(1, 0.5, 0.5)
gestureDetector = gesturerecognition.GestureDetector(1, 0.5, 0.5)
getNameEvent = threading.Event()
imageEvent = threading.Event()
exitEvent = threading.Event()

def getNameOfGesture(image):
    print(f"You have {GESTURE_PREP_DELAY} seconds to prepare your gesture.")
    time.sleep(GESTURE_PREP_DELAY)
    print("Your gesture was captured.")
    capturedGesture = handDetector.centerHandPositions(image, 0, 0)
    with open(TRAINING_DATA_FILE_PATH, "r") as trainingDataFile:
        if len(capturedGesture) > 0:
            gestureCosts = gestureDetector.getGestureCosts(capturedGesture, json.load(trainingDataFile))
            minGestureCost = gestureCosts[0]
            for gestureCost in gestureCosts:
                if gestureCost["cost"] < minGestureCost["cost"]:
                    minGestureCost = gestureCost
            if minGestureCost["cost"] <= MIN_MATCH_THRESHOLD and minGestureCost["name"] != "none":
                print(f"Your gesture was identified as '{minGestureCost['name']}'")
            else:
                print("Your gesture did not match any other gesture.")
                minGestureCost["name"] = "none"
            gestureName = input("Enter to register the gesture, type 'NONE' to cancel, or type a different name: ")
            if gestureName != "NONE":
                if gestureName == "":
                    training.addGestureToFile(minGestureCost["name"], capturedGesture, TRAINING_DATA_FILE_PATH)
                else:
                    training.addGestureToFile(gestureName, capturedGesture, TRAINING_DATA_FILE_PATH)
        else:
            print("The camera failed to capture your gesture.")
        getNameEvent.set()

def showCameraFeed():
    global image
    while True:
        capturedImage = capture.read()[1]
        image = capturedImage.copy()
        image = cv2.resize(image, (CAMERA_WIDTH, CAMERA_HEIGHT))
        imageEvent.set()
        cv2.imshow("Image", image)
        key = cv2.waitKey(LOOP_DELAY)
        if key == 27:
            exitEvent.set()
            break
    cv2.destroyAllWindows()

def detectPalm():
    didHandReset = True
    while not exitEvent.is_set():
        imageEvent.wait()
        imageEvent.clear()
        if handDetector.getHandCountInImage(image) == 0:
            didHandReset = True
        elif gestureDetector.detectOpenPalm(image) and didHandReset:
            didHandReset = False
            getGestureNameThread = threading.Thread(target=getNameOfGesture, args=(image,))
            getGestureNameThread.start()
            getNameEvent.wait()
            getNameEvent.clear()
        cv2.waitKey(LOOP_DELAY)

with open(TRAINING_DATA_FILE_PATH, "r") as trainingDataFile:
    if (trainingDataFile.read() == ""):
        with open(TRAINING_DATA_FILE_PATH, "w") as trainingDataFile:
            json.dump([], trainingDataFile)

showCameraThread = threading.Thread(target=showCameraFeed)
detectPalmThread = threading.Thread(target=detectPalm)
showCameraThread.start()
detectPalmThread.start()
