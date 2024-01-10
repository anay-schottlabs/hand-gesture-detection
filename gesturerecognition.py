import handtracking
import json
import fastdtw

class GestureDetector:
    def __init__(self, maxHands, detectionConfidence, trackingConfidence):
        self.handDetector = handtracking.HandDetector(maxHands, detectionConfidence, trackingConfidence)
    
    def detectOpenPalm(self, image, handLandmarkToCenter):
        thumbOpen = False
        indexOpen = False
        middleOpen = False
        ringOpen = False
        pinkyOpen = False
        hands = self.handDetector.getHandLandmarksFromImage(image)
        if (hands):
            for i in range(len(hands)):
                hand = self.handDetector.findHandLandmarkPositions(image, i)
                try:
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
                        height, width = image.shape
                        centerX = width / 2
                        centerY = height / 2
                        xModifierToCenter = centerX - hand[handLandmarkToCenter]["x"]
                        yModifierToCenter = centerY - hand[handLandmarkToCenter]["y"]
                        return ({"x": xModifierToCenter, "y": yModifierToCenter}, True)
                except:
                    break
            return (None, False)

    def mostSimilarGestureName(self, newGesture, existingGesturesJSON, xModifierToCenter, yModifierToCenter):
        existingGestures = json.loads(existingGesturesJSON)
        gestureCosts = []
        for existingGesture in existingGestures:
            centeredNewGesture = newGesture.copy()
            centeredExistingGesture = existingGesture.copy()
            for hand in centeredNewGesture:
                for handLandmarks in hand:
                    for handLandmark in handLandmarks:
                        handLandmark[1] += xModifierToCenter
                        handLandmark[2] += yModifierToCenter
            for hand in centeredExistingGesture:
                for handLandmarks in hand:
                    for handLandmark in handLandmarks:
                        handLandmark[0] += xModifierToCenter
                        handLandmark[1] += yModifierToCenter
            gestureCosts.append(fastdtw.fastdtw(newGesture, existingGesture))
        return existingGestures[gestureCosts.index(min(gestureCosts))]["name"]
