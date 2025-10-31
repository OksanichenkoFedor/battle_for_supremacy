from hexagon import hex_pixel_distance, Hexagon


class ClusterFinder:
    def __init__(self, field):
        self.field = field
        self.find_clusters()

    def find_clusters(self):
        self.main_index = 0
        self.not_in_cluster = [True] * self.field.total_hexagons
        self.clusters = []
        while self.main_index < self.field.total_hexagons:
            if self.not_in_cluster[self.main_index]:
                curr_cluster = Cluster(self.main_index,self, self.field)
                self.clusters.append(curr_cluster)
            self.main_index+=1


class Cluster:
    def __init__(self, start_id, master, field):
        self.start_id = start_id
        self.master = master
        self.field = field
        self.cluster_type = self.field.hexagons[self.start_id].color_id
        self.cluster_elements = []
        self.cluster_borders = []
        self.is_base_inside = False
        self.step_deep(start_id)

    def step_deep(self, curr_id):
        if self.field.hexagons[curr_id].is_team_base:
            self.is_base_inside = True
        self.master.not_in_cluster[curr_id] = False
        self.cluster_elements.append(curr_id)
        nearest_hexes = self.field.get_adjacent_hexagons(curr_id)
        for nearest in nearest_hexes:
            if nearest.color_id == self.cluster_type:
                if not (nearest.id in self.cluster_elements):
                    self.step_deep(nearest.id)
            else:
                if not (nearest.id in self.cluster_borders):
                    self.cluster_borders.append(nearest.id)

    def find_border_types(self):
        types = []
        for border_el_id in self.cluster_borders:
            if not (self.field.hexagons[border_el_id].color_id in types):
                types.append(self.field.hexagons[border_el_id].color_id)
        return types

    def redraw(self, new_color_id):
        #print("redraw",self.cluster_type, new_color_id, self.cluster_elements)
        for hex_id in self.cluster_elements:
            self.field.simple_change_color(hex_id, new_color_id)

    def count_mean_dist(self, hex: Hexagon):
        curr_dist = 0.0
        for curr_hex_id in self.cluster_elements:
            curr_dist += hex_pixel_distance(hex, self.field.hexagons[curr_hex_id])
        curr_dist = curr_dist / (1.0*len(self.cluster_elements))
        return curr_dist