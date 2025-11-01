import time
from operator import truediv

import pygame
import numpy as np
import random

from cluster_finder import ClusterFinder
from consts import HEX_COLORS, BACKGROUND_COLOR, HEX_COUNT, HEIGHT, BASE_HEX_COLOR, MIN_NUM_STAR_POINTS, \
    MAX_NUM_STAR_POINTS, BETA, TEAM_BASE_COEFF, NUM_STAR, TIME_PER_ATTACK
from hexagon import Hexagon, hex_pixel_distance
from saver_loader import SaverLoader


class Field:
    def __init__(self, side_size, screen):
        self.side_size = side_size
        self.num_iter = 0
        self.color_hex = 0
        self.radius = self.side_size - 1
        self.save_loader = SaverLoader(self)
        self.screen = screen
        self.regime = "Нападение"
        self.generate_field()
        self.update()

    def load(self):
        self.reset()
        field_dict = self.save_loader.load()
        self.hexagons = []
        self.cubic_hexagons = []
        for i in range(2 * self.radius + 1):
            self.cubic_hexagons.append([False] * (2 * self.radius + 1))
        self.IDs = []
        for i in range(len(field_dict["id"])):
            curr_id, r, q = int(field_dict["id"][i]), int(field_dict["r"][i]), int(field_dict["q"][i])
            size, color_id, is_team_base = (int(field_dict["size"][i]), int(field_dict["color_id"][i]),
                                            bool(field_dict["is_team_base"][i]))
            is_star = bool(field_dict["is_star"][i])
            hex = Hexagon(q, r, curr_id, size=size)
            hex.color_id, hex.is_team_base, hex.is_star = color_id, is_team_base, is_star
            self.hexagons.append(hex)
            self.cubic_hexagons[q + self.radius][r + self.radius] = hex
            self.IDs.append(curr_id)
        self.update()




    def generate_field(self):
        self.hexagons = []
        self.cubic_hexagons = []
        self.hexes_of_forse = []
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
                self.hexes_of_forse.append(self.hexagons[id])
        for _ in range(NUM_STAR):
            self.find_new_start_hex()

    def count_energy(self, curr_hex):
        value = 0
        for hex in self.hexes_of_forse:
            curr_dist = hex_pixel_distance(hex, curr_hex)+0.001
            if hex.is_team_base:
                curr_dist*=1.0/TEAM_BASE_COEFF
            value+=1.0/(1.0*curr_dist)
        value = value/(1.0*len(self.hexes_of_forse))
        return value

    def find_new_start_hex(self):
        energies = []
        for i in range(len(self.hexagons)):
            energies.append(self.count_energy(self.hexagons[i]))
        id = boltzmann_selection(energies, BETA)
        self.hexagons[id].is_star = True
        self.hexes_of_forse.append(self.hexagons[id])


    def get_hex_from_cubic(self,q,r):
        return self.cubic_hexagons[q+self.radius][r+self.radius]

    def reset(self):
        for i in range(len(self.hexagons)):
            self.hexagons[i].reset_color()
        #self.update_all()

    def change_color(self, id, color_id):
        if not self.hexagons[id].is_team_base:
            nearest_hexes = self.get_adjacent_hexagons(id)
            found_same_color = False
            for nearest in nearest_hexes:
                if nearest.color_id==color_id:
                    found_same_color = True
            if color_id == -1:
                found_same_color = True

            if found_same_color:

                if self.hexagons[id].is_star:
                    nearest_hexes = self.get_adjacent_hexagons(id)
                    random.shuffle(nearest_hexes)
                    num_points = np.random.randint(MIN_NUM_STAR_POINTS,MAX_NUM_STAR_POINTS+1)
                    for i in range(len(nearest_hexes)):
                        if nearest_hexes[i].color_id!=color_id and num_points>0:
                            self.simple_change_color(nearest_hexes[i].id, color_id)
                            num_points-=1
                    self.hexagons[id].is_star=False
                self.simple_change_color(id, color_id)

        self.update()
        self.save_loader.save()
        self.draw_status()

    def simple_change_color(self, id, color_id):
        if color_id!=-1:
            self.color_hex += color_id
        self.hexagons[id].change_color(color_id)
        self.hexagons[id].draw(self.screen)

    def contains_point(self, mouse_pos):
        for hexagon in self.hexagons:
            if hexagon.contains_point(mouse_pos):
                return hexagon.id
        return -1

    def update(self):
        self.num_iter+=1
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

    def attack(self, attack_color_id, defend_color_id):
        cluster_finder = ClusterFinder(self)
        attack_cluster, defend_cluster = None, None
        found = False
        for cluster in cluster_finder.clusters:
            border_types = cluster.find_border_types()
            self_type = cluster.cluster_type
            if self_type == attack_color_id:
                if defend_color_id in border_types:
                    found = True
                    attack_cluster = cluster
            elif self_type == defend_color_id:
                if attack_color_id in border_types:
                    found = True
                    defend_cluster = cluster
        if found:
            if self.regime == "Нападение":
                size = 0.25
            elif self.regime == "Война":
                size = 0.5

            num = int(size*len(defend_cluster.cluster_elements))
            print(self.regime, num)
            print("Attack: ", attack_color_id, len(attack_cluster.cluster_elements))
            print("Defend: ", defend_color_id, len(defend_cluster.cluster_elements))

            distes = []
            for i in range(len(defend_cluster.cluster_elements)):
                curr_hex = self.hexagons[defend_cluster.cluster_elements[i]]
                distes.append(attack_cluster.count_mean_dist(curr_hex))
            sorted_cluster_elements = [a for a, b in sorted(zip(defend_cluster.cluster_elements, distes), key=lambda x: x[1])]
            index = 0
            while index<num:
                if self.hexagons[sorted_cluster_elements[index]].is_team_base:
                    num+=1
                else:
                    time.sleep(TIME_PER_ATTACK)
                    self.simple_change_color(sorted_cluster_elements[index], attack_color_id)
                    self.draw()
                    self.count_colors()
                    self.draw_status()
                    pygame.display.flip()
                index+=1
            print(sorted_cluster_elements)
            print("---")

            self.update()



    def draw(self):
        #print("update_all")
        self.screen.fill(BACKGROUND_COLOR)

        # Рисуем все шестиугольники
        for hexagon in self.hexagons:
            hexagon.draw(self.screen)

        self.draw_status()

    def draw_status(self):
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, (0, 0, 100*(len(HEX_COLORS)+2), 80))
        font = pygame.font.SysFont(None, 70)

        for i in range(len(HEX_COLORS)):
            text = str(self.counts[i])
            text_surface = font.render(text, True, HEX_COLORS[i])
            self.screen.blit(text_surface, (60 + 100*i, 10))

    def get_adjacent_hexagons(self, id) -> list[Hexagon]:

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


def boltzmann_selection(energies, beta):
    energies = np.array(energies)
    min_energy = np.min(energies)
    weights = np.exp(-beta * (energies - min_energy))
    probabilities = weights / np.sum(weights)
    selected_index = np.random.choice(len(energies), p=probabilities)

    return selected_index