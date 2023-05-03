from city import VERTICAL, HORIZONTAL

class Roads:
    """
    This class is a container for the roads
    - roads are represented as sets of tuples according to their direction
        - A set of vertical roads and Another for horizontal roads
    - if a road is hovered, self.hoveredRoad is that road and its direction is hoveredDirection
    - if a road is changed, self.changes is set to True
    The Road can be retrieved from a save_source if it's not none
    """
    def __init__(self, save_source=None):

        # roads in sets of tuples divided according to their directions:
        self.verticalRoads = set()
        self.horizontalRoads = set()

        # mouse hovering
        self.hoveredRoad = None
        self.hoveredDirection = VERTICAL
        # Todo Why are you always vertical?

        # Todo how is this needed?
        self.changes = False  # whether roads were recently modified (for rebuilding the graph)

        # reading from save file
        if save_source is not None:
            for road in save_source['vertical']:
                self.verticalRoads.add(tuple(road))
            for road in save_source['horizontal']:
                self.horizontalRoads.add(tuple(road))


    def removeRoad(self, direction, pos):
        """
        - removeRoad(direction, pos):
            - direction is the set from which to delete the road (self.vertical or self.horizontal)
            - pos is the index of the road in the set
        """
        self.changes = True
        if direction == VERTICAL:
            self.verticalRoads.remove(pos)
        elif direction == HORIZONTAL:
            self.horizontalRoads.remove(pos)

    def addRoad(self, direction, pos):
        """
        - addRoad(direction, pos):
            - direction is the set from which to add the road (self.vertical or self.horizontal)
            - pos is the index of the road in the set
        """
        self.changes = True
        if direction == VERTICAL:
            self.verticalRoads.add(pos)
        elif direction == HORIZONTAL:
            self.horizontalRoads.add(pos)


    def hasRoad(self, x, y, direction):
        """
        - hasRoad(x, y , direction):
            - x, y are the position of the road in the set
            - direction is the set from which to check (self.vertical or self.horizontal)
        """
        if direction == VERTICAL:
            return (x, y) in self.verticalRoads
        elif direction == HORIZONTAL:
            return (x, y) in self.horizontalRoads


    def getRoadsCount(self):
        """
        - getRoadsCount(direction, pos):
            - pos is the index of the road in the set
        """
        return len(self.verticalRoads) + len(self.horizontalRoads)

    def handleRoadClicked(self):
        """
        - handleRoadClicked(direction, pos):
            Event handler when a road is clicked.
            it adds the hovered road, when you click on it
        """
        if self.hoveredRoad is None:
            return
        if self.hoveredDirection == VERTICAL and self.hoveredRoad in self.verticalRoads:
            self.removeRoad(VERTICAL, self.hoveredRoad)
        elif self.hoveredDirection == HORIZONTAL and self.hoveredRoad in self.horizontalRoads:
            self.removeRoad(HORIZONTAL, self.hoveredRoad)
        else:
            self.addRoad(self.hoveredDirection, self.hoveredRoad)

    def handleRoadHovered(self, road):
        """
        - handleRoadHovered(road):
            - updates the hovered road position when the mouse is moved
        """
        if self.hoveredDirection == VERTICAL:
            round_x, round_y = round, int
        else:
            round_x, round_y = int, round
        if road is not None:
            x, y = road
            self.hoveredRoad = round_x(x), round_y(y)
        else:
            self.hoveredRoad = None

    def getRoads(self):
        return {
            'vertical': list(self.verticalRoads),
            'horizontal': list(self.horizontalRoads)
        }
