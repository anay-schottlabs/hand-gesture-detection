import handtracking
import json
import fastdtw

class GestureDetector:
    def __init__(self, maxHands, detectionConfidence, trackingConfidence):
        self.handDetector = handtracking.HandDetector(maxHands, detectionConfidence, trackingConfidence)
    
    def detectOpenPalm(self, image):
        thumbOpen = False
        indexOpen = False
        middleOpen = False
        ringOpen = False
        pinkyOpen = False
        for i in range(self.handDetector.getHandCountInImage(image)):
            hand = self.handDetector.getHandLandmarkPositions(image, i)
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

    def mostSimilarGestureName(self, newGesture, existingGesturesJSON):
        existingGestures = json.loads(existingGesturesJSON)
        gestureCosts = []
        for existingGesture in existingGestures:
            gestureCosts.append(fastdtw.fastdtw(newGesture, existingGesture["gesture"])[0])
        return existingGestures[gestureCosts.index(min(gestureCosts))]["name"]
