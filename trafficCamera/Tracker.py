class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.centerPoints = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0