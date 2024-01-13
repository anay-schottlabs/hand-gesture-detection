import handtracking
import json
import fastdtw

# A class to detect hand gestures
class GestureDetector:
    def __init__(self, maxHands, detectionConfidence, trackingConfidence):
        self.handDetector = handtracking.HandDetector(maxHands, detectionConfidence, trackingConfidence)
    
    # Check if any of the hands on the screen have their palms open
    def detectOpenPalm(self, image):
        thumbOpen = False
        indexOpen = False
        middleOpen = False
        ringOpen = False
        pinkyOpen = False
        for i in range(self.handDetector.getHandCountInImage(image)):
            hand = self.handDetector.getHandLandmarkPositions(image, i)
            # Check for relative hand landmark positions
            if (hand[2]["y"] > hand[3]["y"] > hand[4]["y"]):
                thumbOpen = True
            if (hand[6]["y"] > hand[7]["y"] > hand[8]["y"]):
                indexOpen = True
            if (hand[10]["y"] > hand[11]["y"] > hand[12]["y"]):
                middleOpen = True
            if (hand[14]["y"] > hand[15]["y"] > hand[16]["y"]):
                ringOpen = True
            if (hand[18]["y"] > hand[19]["y"] > hand[20]["y"]):
                pinkyOpen = True
            if (thumbOpen and indexOpen and middleOpen and ringOpen and pinkyOpen):
                return True
        return False

    # Classify the gesture given based on labeled data from existing gestures
    def mostSimilarGestureName(self, newGesture, existingGesturesJSON):
        existingGestures = json.loads(existingGesturesJSON)
        gestureCosts = []
        # Use dynamic time warping to determine the cost to align the gesture to each gesture
        for existingGesture in existingGestures:
            gestureCosts.append(fastdtw.fastdtw(newGesture, existingGesture["gesture"])[0])
        # Return the gesture name that has the least aligning cost
        return existingGestures[gestureCosts.index(min(gestureCosts))]["name"]
