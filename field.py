import pygame

from cluster_finder import ClusterFinder
from consts import HEX_COLORS, BACKGROUND_COLOR, HEX_COUNT, HEIGHT, BASE_HEX_COLOR
from hexagon import Hexagon


class Field:
    def __init__(self, side_size, screen):
        self.side_size = side_size
        self.radius = self.side_size - 1

        self.screen = screen
        self.generate_field()
        self.update()

    def generate_field(self):
        self.hexagons = []
        self.cubic_hexagons = []
        for i in range(2*self.radius+1):
            self.cubic_hexagons.append([False]*(2*self.radius+1))
        self.IDs = []
        curr_id = 0
        team_id = 0
        for q in range(-self.radius, self.radius + 1):
            for r in range(-self.radius, self.radius + 1):
                s = -q - r
                if abs(s) <= self.radius:
                    hex = Hexagon(q, r, curr_id)
                    self.hexagons.append(hex)
                    if self.cubic_hexagons[q+self.radius][r+self.radius]!=False:
                        print("Error")
                    self.cubic_hexagons[q+self.radius][r+self.radius] = hex
                    self.IDs.append(curr_id)
                    curr_id += 1
        self.total_hexagons = len(self.hexagons)
        for id in range(self.total_hexagons):
            if len(self.get_adjacent_hexagons(id))==3:
                self.hexagons[id].change_color(team_id)
                self.hexagons[id].is_team_base = True
                team_id+=1

    def get_hex_from_cubic(self,q,r):
        return self.cubic_hexagons[q+self.radius][r+self.radius]

    def reset(self):
        for i in range(self.hexagons):
            self.hexagons[i].reset_color()
        #self.update_all()

    def change_color(self, id, color_id):
        if not self.hexagons[id].is_team_base:
            nearest_hexes = self.get_adjacent_hexagons(id)
            found_same_color = False
            for nearest in nearest_hexes:
                if nearest.color_id==color_id:
                    found_same_color = True
            if found_same_color:
                self.simple_change_color(id, color_id)
        self.update()
        self.draw_status()

    def simple_change_color(self, id, color_id):
        self.hexagons[id].change_color(color_id)
        self.hexagons[id].draw(self.screen)

    def contains_point(self, mouse_pos):
        for hexagon in self.hexagons:
            if hexagon.contains_point(mouse_pos):
                return hexagon.id
        return -1

    def update(self):
        continue_clustering = True
        while continue_clustering:
            continue_clustering = False
            cluster_finder = ClusterFinder(self)
            #print("-------", len(cluster_finder.clusters))
            for cluster in cluster_finder.clusters:
                border_types = cluster.find_border_types()
                self_type = cluster.cluster_type
                #print(self_type, border_types, cluster.is_base_inside)
                if self_type == -1:
                    if len(border_types) == 1:
                        cluster.redraw(border_types[0])
                        continue_clustering = True
                else:
                    if not cluster.is_base_inside:
                        if len(border_types) == 1:
                            cluster.redraw(border_types[0])
                            continue_clustering = True
                        else:
                            cluster.redraw(-1)
                            continue_clustering = True
        self.count_colors()

    def count_colors(self):
        self.counts = [0]*len(HEX_COLORS)
        for hex in self.hexagons:
            if hex.color_id!=-1:
                self.counts[hex.color_id]+=1




    def draw(self):
        #print("update_all")
        self.screen.fill(BACKGROUND_COLOR)

        # Рисуем все шестиугольники
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)

        self.draw_status()

    def draw_status(self):
        pygame.draw.rect(self.screen, BASE_HEX_COLOR, (0, 0, 100*(len(HEX_COLORS)+2), 80))
        font = pygame.font.SysFont(None, 70)

        for i in range(len(HEX_COLORS)):
            text = str(self.counts[i])
            text_surface = font.render(text, True, HEX_COLORS[i])
            self.screen.blit(text_surface, (60 + 100*i, 10))

    def get_adjacent_hexagons(self, id):

        q, r = self.hexagons[id].q, self.hexagons[id].r
        # Направления в кубических координатах (q, r, s)
        directions = [
            (1, 0),  # восток
            (1, -1),  # северо-восток
            (0, -1),  # северо-запад
            (-1, 0),  # запад
            (-1, 1),  # юго-запад
            (0, 1)  # юго-восток
        ]

        adjacent = []

        for dq, dr in directions:
            nq = q + dq
            nr = r + dr
            ns = -nq - nr  # s = -q - r (в кубической системе)

            if abs(nq) <= self.radius and abs(nr) <= self.radius and abs(ns) <= self.radius:
                adjacent.append(self.get_hex_from_cubic(nq, nr))
                #print(self.cubic_hexagons[nq][nr].id)
        return adjacent