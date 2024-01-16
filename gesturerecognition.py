import handtracking
import fastdtw
import numpy as np

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
            if hand:
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

    # Get the cost to align each existing gesture to a new gesture
    def getGestureCosts(self, newGesture, existingGestures, newGestureIdentifier):
        gestureCosts = []
        mostSimilarGestures = self.getSimilarGestures(existingGestures, newGestureIdentifier)
        for existingGesture in mostSimilarGestures:
            # Convert the gestures into points
            newGesturePoints = self.convertGestureToPoints(newGesture)
            existingGesturePoints = self.convertGestureToPoints(existingGesture)
            # Use dynamic time warping to determine the cost to align the new gesture to each existing gesture
            cost = fastdtw.fastdtw(newGesturePoints, existingGesturePoints)[0]
            gestureCosts.append({"name": existingGesture["name"], "cost": cost})
        # Return all of the gesture costs
        return gestureCosts

    # Use a binary search to get similar gestures to a new gesture using their identifiers
    def getSimilarGestures(self, gestures, identifier):
        # Set the low and high variables
        low = 0
        high = len(gestures) - 1
        while low <= high:
            # Calculate the middle of the gestures
            middle = (high + low) // 2
            # If we are on the last gesture and can't find anything, exit the loop
            if middle == len(gestures) - 1:
                break
            # Return the gestures if we found the two closest ones
            elif gestures[middle] < identifier and gestures[middle + 1] > identifier:
                return (gestures[middle], gestures[middle + 1])
            # If we found the same gesture, return it
            elif gestures[middle] == identifier:
                return (gestures[middle],)
            # If the gesture's identifier is less than the new identifier, change the low to the middle
            elif gestures[middle] < identifier:
                low = middle + 1
            # If the gesture's identifier is higher than the new identifier, change the high to the middle
            elif gestures[middle] > identifier:
                high = middle - 1
        # If we couldn't find anything, return an empty tuple
        return ()

    # Convert each hand landmark to a list of coordinates rather than a dictionary
    def convertGestureToPoints(self, gesture):
        # Copy the original gesture
        gesturePoints = gesture.copy()
        for handMovement in gesturePoints:
            for hand in handMovement:
                for point in hand:
                    # Convert each dictionary to a list of the x and y coordinates
                    point = [point["x"], point["y"]]

    # Get the distance between the given gesture and a standard comparison gesture
    def getGestureIdentifier(self, gesture, comparisonGesture):
        return np.linalg.norm(gesture - comparisonGesture)
