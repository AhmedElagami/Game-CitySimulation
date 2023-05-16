class RoadNetGraph:
    """ class used as to find connection between fields through road system"""

    def __init__(self, road_system, fields):
        self.road_system = road_system
        self.fields = fields
        self.rebuild_references(force=True)

    def rebuild_references(self, force=False):
        if self.road_system.changes or force:
            self.road_system.changes = False
            fields_with_buildings = self.preprocess_fields()
            for field in fields_with_buildings:
                self.update_field(field)

    def preprocess_fields(self):
        fields_with_buildings = []
        for row in self.fields:
            for field in row:
                field.affected_by = set()
                field.affects = set()
                if not (field.construct is None or field.construct.get('range', 0) == 0):
                    fields_with_buildings.append(field)
        return fields_with_buildings

    def update_field(self, field, remove=False):
        row, col = field.y, field.x
        i, j = row + 1, col
        radius = field.construct.get('range', 0)
        if (j, i) in self.road_system.horizontal:
            visited = dict()
            self.dfs(field, False, i, j, radius, remove, visited)

    def dfs(self, field, vertical, i, j, radius, remove, visited):
        visited[(i, j, vertical)] = radius
        construct = field.construct
        if radius > 0:
            radius -= 1
            hor_neighbors, ver_neighbors = self.edge_neighbors(i, j, vertical)
            field1, field2 = self.road_adjacent_fields(i, j, vertical)

            if remove:
                if construct in field1.affected_by:
                    field1.affected_by.remove(construct)
                if field1 in field.affects:
                    field.affects.remove(field1)

                if field2 is not None:
                    if construct in field2.affected_by:
                        field2.affected_by.remove(construct)
                    if field2 in field.affects:
                        field.affects.remove(field2)
            else:
                field1.affected_by.add(construct)
                field.affects.add(field1)
                if field2 is not None:
                    field2.affected_by.add(construct)
                    field.affects.add(field2)

            for row, col in hor_neighbors:
                if visited.get((row, col, False), 0) <= radius:
                    self.dfs(field, False, row, col, radius, remove, visited)
            for row, col in ver_neighbors:
                if visited.get((row, col, True), 0) <= radius:
                    self.dfs(field, True, row, col, radius, remove, visited)

    def road_adjacent_fields(self, i, j, vertical):
        second_field = None
        if vertical:
            if j - 1 >= 0:
                second_field = self.fields[j - 1][i]
        else:
            if i - 1 >= 0:
                second_field = self.fields[j][i - 1]

        return self.fields[j][i], second_field

    def edge_neighbors(self, i, j, vertical):
        ver, hor = [(i - 1, j)], [(i, j - 1)]
        if vertical:
            ver += [
                (i + 1, j)
            ]
            hor += [
                (i, j),
                (i + 1, j - 1),
                (i + 1, j)
            ]
        else:
            ver += [
                (i - 1, j + 1),
                (i, j),
                (i, j + 1)
            ]
            hor += [
                (i, j + 1)
            ]
        return self.filter_neighbor_roads(hor, ver)

    def filter_neighbor_roads(self, hor=None, ver=None):
        if ver is None:
            ver = []
        if hor is None:
            hor = []

        horizontal = [
            (i, j) for i, j in hor if (j, i) in self.road_system.horizontal
        ]
        vertical = [
            (i, j) for i, j in ver if (j, i) in self.road_system.vertical
        ]
        return horizontal, vertical
