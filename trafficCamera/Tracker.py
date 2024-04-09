import math
class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.centerPoints = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0   
        
    def update(self, objectsRect):
        # Objects boxes and ids
        objectsBoxesIds = []

        # Get center point of new object
        for rect in objectsRect:
            x1, y1, x2, y2 = rect
            centerX = (x1 + x1 + x2) // 2
            centerY = (y1 + y1 + y2) // 2

            # Find out if that object was detected already
            sameObjectDetected = False
            for id, pt in self.centerPoints.items():
                distance = math.hypot(centerX - pt[0], centerY - pt[1])

                if distance < 35:
                    self.centerPoints[id] = (centerX, centerY)
                    objectsBoxesIds.append([x1, y1, x2, y2, id])
                    sameObjectDetected = True
                    break

            # New object is detected we assign the ID to that object
            if sameObjectDetected is False:
                self.centerPoints[self.id_count] = (centerX, centerY)
                objectsBoxesIds.append([x1, y1, x2, y2, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        newCenterPoints = {}
        for objectsBoxesId in objectsBoxesIds:
            _, _, _, _, objectId = objectsBoxesId
            center = self.centerPoints[objectId]
            newCenterPoints[objectId] = center

        # Update dictionary with IDs not used removed
        self.centerPoints = newCenterPoints.copy()
        
        return objectsBoxesIds