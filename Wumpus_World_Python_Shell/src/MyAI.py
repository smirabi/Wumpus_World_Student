# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
import math

import pdb


class MyAI(Agent):

    def __init__(self):
        self._count = 0
        self._coord = [1, 1]
        self._dir = "right"
        self._senses = []
        # self._potentialdanj = []
        self._safe_zones = [[1, 1]]
        self.node_dict = [[1, 1]]
        self._state = [[self._dir, self._coord]]
        self._range = [
            [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1],
            [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2],
            [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3],
            [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4],
            [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5],
            [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6],
            [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7], [8, 7]]
        self.gold_grabbed = False
        self.shortest_path = []
        #############################
        self.right = [self._coord[0] + 1, self._coord[1]]
        self.left = [self._coord[0] - 1, self._coord[1]]
        self.top = [self._coord[0], self._coord[1] + 1]
        self.down = [self._coord[0], self._coord[1] - 1]
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False
        self.go_to = [[1, 1]]
        self.counter = 0

    def update_senses(self, stench, breeze, glitter, bump, scream):
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

    def update_state(self):
        self._state.append([self._dir, self._coord])

    def update_dir(self):
        self.right = [self._coord[0] + 1, self._coord[1]]
        self.left = [self._coord[0] - 1, self._coord[1]]
        self.top = [self._coord[0], self._coord[1] + 1]
        self.down = [self._coord[0], self._coord[1] - 1]

    def calc_safety(self, stench, breeze, bump):
        if bump:
            if self._dir == "right":
                y = self._range[-1][1]
                self._range.clear()
                for i in range(self._coord[0] - 1):
                    for j in range(y):
                        self._range.append([i + 1, j + 1])
                self._safe_zones.remove(self._coord)
                self.go_to.remove(self._coord)
                self._coord = self.left
            elif self._dir == "top":
                x = self._range[-1][0]
                self._range.clear()
                for i in range(x):
                    for j in range(self._coord[1] - 1):
                        self._range.append([i + 1, j + 1])
                self._safe_zones.remove(self._coord)
                self.go_to.remove(self._coord)
                self._coord = self.down
            self._state.remove(self._state[-1])

        if not stench and not breeze:
            if self.right in self._range and self.right not in self._safe_zones:
                self._safe_zones.append(self.right)
                self.go_to.append(self.right)
            if self.left in self._range and self.left not in self._safe_zones:
                self._safe_zones.append(self.left)
                self.go_to.append(self.left)
            if self.top in self._range and self.top not in self._safe_zones:
                self._safe_zones.append(self.top)
                self.go_to.append(self.top)
            if self.down in self._range and self.down not in self._safe_zones:
                self._safe_zones.append(self.down)
                self.go_to.append(self.down)
        # else:
        #     if (self.right in self._range) and (self.right not in self._safe_zones):
        #         self._potentialdanj.append(self.right)
        #     if (self.left in self._range) and (self.left not in self._safe_zones):
        #         self._potentialdanj.append(self.left)
        #     if (self.top in self._range) and (self.top not in self._safe_zones):
        #         self._potentialdanj.append(self.top)
        #     if (self.down in self._range) and (self.down not in self._safe_zones):
        #         self._potentialdanj.append(self.down)


    def go_to_huristic(self):
        closest_set = []
        for i, c in enumerate(self.go_to):
            closest_set.append( (math.sqrt((self._coord[0] - c[0])**2 + (self._coord[1] - c[1])**2), c) )
        result = []
        if len(closest_set) != 0:
            minimum = min(x[0] for x in closest_set)
            for j in closest_set:
                if j[0] == minimum:
                    result.append(j[1])

            # return result[0]
            return result[-1]
        return []

    def getAction(self, stench, breeze, glitter, bump, scream):
        # print("go to list: ", self.go_to)
        self.counter += 1
        if self.counter == 1000:
            print("----------------------------->>>>>>>>>>>>>>>>>> loop !")
        self.update_dir()
        self.update_senses(stench, breeze, glitter, bump, scream)
        self.update_state()

        if (breeze or stench) and (self._coord == [1, 1]):
            return Agent.Action.CLIMB
        self._count += 1

        if self._count != 1 and self.gold_grabbed and self._coord == [1, 1]:
            return Agent.Action.CLIMB

        # if self.node_dict.count([1,1]) == 3:
        #     return Agent.Action.CLIMB
        self.calc_safety(stench, breeze, bump)
        if self._coord in self.go_to:
            self.go_to.remove(self._coord)
        if glitter:
            self.gold_grabbed = True
            return Agent.Action.GRAB

        dest_node = self.go_to_huristic()
        # print("destination nodes: ", dest_node)

        def trackAndClimb():
            print("TRACING")

            if self._coord == [1, 1]:
                print("RACING ANd 11 ")
                return Agent.Action.CLIMB
            l = len(self.shortest_path)
            if l == 0:
                for s in self._state:
                    if s[1] != self._coord:
                        self.shortest_path.append(s)
                    else:
                        break
                for i in range(len(self.shortest_path) - 1, -1, -1):
                    return go_back(self.shortest_path, i)
            else:
                for i in range(len(self.shortest_path) - 1, -1, -1):
                    return go_back(self.shortest_path, i)

        def go_back(path, i):
            print("this is shortest path: ", path)
            print("GOING BACK")
            if self._coord == [1, 1]:
                return Agent.Action.CLIMB
            if path[i][0] == "right":
                if self._dir == "left":
                    print("check point 1.1")
                    path.pop(i)
                    self._coord = self.left
                    return Agent.Action.FORWARD
                else:
                    print("check point 1.2")
                    self._dir = "top"
                    return Agent.Action.TURN_LEFT
            if path[i][0] == "left":
                if self._dir == "right":
                    print("check point 2.1")
                    path.pop(i)
                    self._coord = self.right
                    return Agent.Action.FORWARD
                else:
                    print("check point 2.2")
                    self._dir = "down"
                    return Agent.Action.TURN_LEFT
            if path[i][0] == "top":
                if self._dir == "down":
                    print("check point 3.1")
                    path.pop(i)
                    self._coord = self.down
                    return Agent.Action.FORWARD
                else:
                    print("check point 3.2")
                    self._dir = "left"
                    return Agent.Action.TURN_LEFT
            if path[i][0] == "down":
                if self._dir == "top":
                    print("check point 4.1")
                    path.pop(i)
                    self._coord = self.top
                    return Agent.Action.FORWARD
                else:
                    print("check point 4.2")
                    self._dir = "right"
                    return Agent.Action.TURN_LEFT
        if self.gold_grabbed or dest_node == []:
            #trackAndClimb()
            if self._coord == [1, 1]:
                return Agent.Action.CLIMB
            dest_node = [1, 1]


        # first try to get the trace and go back to run
        # if it didn't work:
        #   for optimization we can chose a randomize choosing direction
        #   in the last direction choosing
        # at last try to shoot an arrow
        #############################################################################################
        #else:
        if True:
            # pdb.set_trace()
            if dest_node[0]<= self._coord[0] and dest_node[1]<= self._coord[1]:  #in bottom left
                if self._dir == "left":
                    if self.left in self._safe_zones:
                        self._coord = self.left
                        return Agent.Action.FORWARD
                    if self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    if self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                elif self._dir == "down":
                    if self.down in self._safe_zones:
                        self._coord = self.down
                        return Agent.Action.FORWARD
                    if self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    if self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "right":
                    if self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    if self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT

                    if self.right in self._safe_zones:
                        self._coord = self.right
                        return Agent.Action.FORWARD

                    else:
                            self._dir = "down"
                            return Agent.Action.TURN_RIGHT
                elif self._dir == "top":
                    if self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT

                    if self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    if self.top in self._safe_zones:
                        self._coord = self.top
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT

            elif dest_node[0] >= self._coord[0] and dest_node[1] >= self._coord[1]:
                if self._dir == "right":
                    if self.right in self._safe_zones:
                        self._coord = self.right
                        return Agent.Action.FORWARD

                    if self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    if self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "top":
                    if self.top in self._safe_zones:
                        self._coord = self.top
                        return Agent.Action.FORWARD
                    if self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    if self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT

                elif self._dir == "left":
                    if self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    if self.right in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    if self.left in self._safe_zones:
                        self._coord = self.left
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "down":
                    if self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                    if self.top in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                    # in this case where we're facing down and top and right
                    # are not in safe zone we just move forward to save one move
                    # we can also go left
                    # later we can optimize it by choosing between down and left based on
                    # the one that would take us less further than the destination node
                    if self.down in self._safe_zones:
                        self._coord = self.down
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT

            elif dest_node[0] <= self._coord[0] and dest_node[1] >= self._coord[1]:
                if self._dir == "left":
                    if self.left in self._safe_zones:
                        self._coord = self.left
                        return Agent.Action.FORWARD
                    elif self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    elif self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT

                if self._dir == "top":
                    if self.top in self._safe_zones:
                        self._coord = self.top
                        return Agent.Action.FORWARD
                    elif self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    elif self.down in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT

                if self._dir == "down":
                    if self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    elif self.down in self._safe_zones:
                        self._coord = self.down
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                if self._dir == "right":
                    if self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    elif self.right in self._safe_zones:
                        self._coord = self.right
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT

            elif dest_node[0] >= self._coord[0] and dest_node[1] <= self._coord[1]:
                if self._dir == "right":
                    if self.right in self._safe_zones:
                        self._coord= self.right
                        return Agent.Action.FORWARD
                    elif self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                if self._dir == "down":
                    if self.down in self._safe_zones:
                        self._coord = self.down
                        return Agent.Action.FORWARD
                    elif self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                if self._dir == "left":
                    if self.down in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    elif self.right in self._safe_zones:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones:
                        self._coord= self.left
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT

                if self._dir == "top":
                    if self.right in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    elif self.down in self._safe_zones:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones:
                        self._coord = self.top
                        return Agent.Action.FORWARD
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT





























            # if self._dir == "right":
            #
            #     if self.right in self._safe_zones:
            #         # if self.node_dict.count(self.right) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._coord = self.right
            #         self.node_dict.append(self.right)
            #         if self.right in self.go_to:
            #             self.go_to.remove(self.right)
            #         self.update_state()
            #         return Agent.Action.FORWARD
            #     if self.top in self._safe_zones:
            #         # if self.node_dict.count(self.top) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "top"
            #         return Agent.Action.TURN_LEFT
            #     if self.down in self._safe_zones:
            #         # if self.node_dict.count(self.down) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "down"
            #       #  self.update_state()  new
            #         return Agent.Action.TURN_RIGHT
            #     else:
            #         self._dir = "top"
            #         return Agent.Action.TURN_LEFT
            # if self._dir == "top":
            #     if bump:
            #         if self._coord[0]-1 >= 3:
            #             self._dir = "left"
            #          #   self.update_state()  new
            #             return Agent.Action.TURN_LEFT
            #         else:
            #             self._dir = "right"
            #           #  self.update_state()  new
            #             return Agent.Action.TURN_RIGHT
            #     else:
            #         if self.top in self._safe_zones:
            #             # if self.node_dict.count(self.top) == 3:
            #             #     trackAndClimb()
            #             # else:
            #             self._coord = self.top
            #             self.node_dict.append(self.top)
            #             if self.top in self.go_to:
            #                 self.go_to.remove(self.top)
            #             self.update_state()
            #             return Agent.Action.FORWARD
            #         if self.right in self._safe_zones:
            #             # if self.node_dict.count(self.right) == 3:
            #             #     trackAndClimb()
            #             # else:
            #             self._dir = "right"
            #         #    self.update_state()  new
            #             return Agent.Action.TURN_RIGHT
            #         if self.left in self._safe_zones:
            #             # if self.node_dict.count(self.left) == 3:
            #             #     trackAndClimb()
            #             # else:
            #             self._dir = "left"
            #         #    self.update_state()  new
            #             return Agent.Action.TURN_LEFT
            #         else:
            #             self._dir = "right"
            #             return Agent.Action.TURN_RIGHT
            #
            # if self._dir == "down":
            #     if self.down in self._safe_zones:
            #         # if self.node_dict.count(self.down) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._coord = self.down
            #         self.node_dict.append(self.down)
            #         if self.down in self.go_to:
            #             self.go_to.remove(self.down)
            #         self.update_state()
            #         return Agent.Action.FORWARD
            #     if self.left in self._safe_zones:
            #         # if self.node_dict.count(self.left) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "left"
            #      #   self.update_state()
            #         return Agent.Action.TURN_RIGHT
            #     if self.right in self._safe_zones:
            #         # if self.node_dict.count(self.right) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "right"
            #      #   self.update_state()
            #         return Agent.Action.TURN_LEFT
            #     else:
            #         self._dir = "right"
            #         return Agent.Action.TURN_LEFT
            #
            # if self._dir == "left":
            #     if self.left in self._safe_zones:
            #         # if self.node_dict.count(self.left) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._coord = self.left
            #         self.node_dict.append(self.left)
            #         if self.left in self.go_to:
            #             self.go_to.remove(self.left)
            #         self.update_state()
            #         return Agent.Action.FORWARD
            #     if self.top in self._safe_zones:
            #         # if self.node_dict.count(self.top) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "top"
            #     #    self.update_state()
            #         return Agent.Action.TURN_RIGHT
            #     if self.down in self._safe_zones:
            #         # if self.node_dict.count(self.down) == 3:
            #         #     trackAndClimb()
            #         # else:
            #         self._dir = "down"
            #      #   self.update_state()
            #         return Agent.Action.TURN_LEFT
            #     else:
            #         self._dir = "top"
            #         return Agent.Action.TURN_RIGHT