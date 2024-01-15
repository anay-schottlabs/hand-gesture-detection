import cv2
import json
import threading
import handtracking

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
TRAINING_DATA_FILE_PATH = "trainingdata.json"
LOOP_DELAY = 2
capture = cv2.VideoCapture(0)
handDetector = handtracking.HandDetector(1, 0.5, 0.5)
image = None
imageLock = threading.Lock()
imageEvent = threading.Event()
exitEvent = threading.Event()

def showCameraFeed():
    global image
    while True:
        # Get the current frame in the camera feed
        capturedImage = capture.read()[1]
        if capturedImage is None:
            continue
        # Use the lock for safety
        with imageLock:
            # Resize the image
            image = capturedImage.copy()
            image = cv2.resize(image, (CAMERA_WIDTH, CAMERA_HEIGHT))
            # Set the image event
            imageEvent.set()
        # Show the image
        cv2.imshow("Image", image)
        # Wait for the specified delay
        key = cv2.waitKey(LOOP_DELAY)
        # If escape is pressed, close the window
        if key == 27:
            exitEvent.set()
            break
    cv2.destroyAllWindows()

def addTrainingData():
    while not exitEvent.is_set():
        # Wait for the image event and clear it once it is set
        imageEvent.wait()
        imageEvent.clear()

        # Prompt the user to take a picture
        input("Press enter to take a picture: ")
        # Use the lock for safety
        with imageLock:
            # Make a copy of the current image frame
            recordedImage = image.copy()
        # Prompt the user for a name to label the hand gesture with
        imageName = input("Enter a name for the image: ")
        addGestureToFile(imageName, handDetector.getRelativeHandPositions(recordedImage, 0, 0), TRAINING_DATA_FILE_PATH)
        # Wait for the specified delay
        cv2.waitKey(LOOP_DELAY)

def addGestureToFile(name, gesture, filePath):
    with open(filePath, "r") as trainingDataFile:
        data = json.load(trainingDataFile)
        # Append the new data to the original training data
        newData = {"name": name, "gesture": gesture}
        data.append(newData)
        # Print the information written for clarity
        print(f"Will add training data:\nName: {newData['name']}\nGesture: {newData['gesture']}")
        # Ask the user if they would like to proceed
        shouldAddData = input("Press enter to continue, anything else to cancel: ")
        # If the user proceeds, inform them that the data was added
        if shouldAddData == "":
            # Clear the file and rewrite the new information
            with open(TRAINING_DATA_FILE_PATH, "w") as trainingDataFile:
                json.dump(data, trainingDataFile, indent=2)
            print("Data successfully added.")
        # If the user does not proceed, inform them that the data was not added
        else:
            print("Data was not added due to cancellation.")

with open(TRAINING_DATA_FILE_PATH, "r") as trainingDataFile:
    if (trainingDataFile.read() == ""):
        with open(TRAINING_DATA_FILE_PATH, "w") as trainingDataFile:
            json.dump([], trainingDataFile)

# Run the threads
if __name__ == "__main__":
    cameraThread = threading.Thread(target=showCameraFeed)
    trainingThread = threading.Thread(target=addTrainingData)
    cameraThread.start()
    trainingThread.start()
