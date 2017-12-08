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


class MyAI(Agent):

    def __init__(self):
        self._count = 0
        self.shoot = True
        self._coord = [1, 1]
        self._dir = "right"
        self._senses = []
        self._potentialdanj = []
        self._safe_zones = [[1, 1]]
        self.node_dict = [[1, 1]]
        self.go = False
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
        self.path = []
        self.trap = []

    def update_senses(self, stench, breeze, glitter, bump, scream):
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

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

    def func(self,l):
        if len(l) == 1 or len(l) == 0:
            return l
        else:
            for i in range(len(l) - 1, -1, -1):
                if l[i] in l[0:i]:
                    return [l[i]] + self.func(l[0:l.index(l[i])])

                else:
                    return [l[i]] + self.func(l[0:len(l) - 1])

    def getAction(self, stench, breeze, glitter, bump, scream):
        self.path.append(self._coord)
        self.counter += 1
        self.update_dir()
        self.update_senses(stench, breeze, glitter, bump, scream)

        if self.path[-20:].count(self._coord) >= 7 or self.path[-30:].count(self._coord) >= 7:
            self.go = True
            self.trap.append(self._coord)
            k = [self.right, self.left, self.top,self.down]
            if self.go:
                for i in k:
                    if i in self._safe_zones and i not in self.trap:
                        if i == self.top:
                            if self._dir == "top":
                                self._coord = self.top
                                return Agent.Action.FORWARD
                            elif self._dir == "right":
                                self._dir = "top"
                                return Agent.Action.TURN_LEFT
                            elif self._dir == "left":
                                self._dir = "top"
                                return Agent.Action.TURN_RIGHT
                            else:
                                self._dir = "left"
                                return Agent.Action.TURN_RIGHT

                        if i == self.right :
                            if self._dir == "right":
                                self._coord = self.right
                                return Agent.Action.FORWARD
                            elif self._dir == "down":
                                self._dir = "right"
                                return Agent.Action.TURN_LEFT
                            elif self._dir == "top":
                                self._dir = "right"
                                return Agent.Action.TURN_RIGHT
                            else:
                                self._dir = "top"
                                return Agent.Action.TURN_RIGHT

                        if i == self.left:
                            if self._dir == "left":
                                self._coord = self.left
                                return Agent.Action.FORWARD
                            elif self._dir == "down":
                                self._dir = "left"
                                return Agent.Action.TURN_RIGHT
                            elif self._dir == "top":
                                self._dir = "left"
                                return Agent.Action.TURN_LEFT
                            else:
                                self._dir = "top"
                                return Agent.Action.TURN_LEFT

                        if i == self.down:
                            if self._dir == "down":
                                self._coord = self.down
                                #print('UUUUUU')
                                return Agent.Action.FORWARD
                            elif self._dir == "right":
                                self._dir = "down"
                                return Agent.Action.TURN_RIGHT
                            elif self._dir == "left":
                                self._dir = "down"
                                return Agent.Action.TURN_LEFT
                            else:
                                self._dir = "right"
                                return Agent.Action.TURN_RIGHT

        if (breeze or stench) and (self._coord == [1, 1]):
            return Agent.Action.CLIMB
        self._count += 1

        if self._count != 1 and self.gold_grabbed and self._coord == [1, 1]:
            return Agent.Action.CLIMB

        self.calc_safety(stench, breeze, bump)
        if self._coord in self.go_to:
            self.go_to.remove(self._coord)
        if glitter:
            self.gold_grabbed = True
            return Agent.Action.GRAB

        dest_node = self.go_to_huristic()

        if self.gold_grabbed or dest_node == [] :

            if self._coord == [1, 1]:
                return Agent.Action.CLIMB
            if self._dir == "left":
                if self.left in self._safe_zones and self.left not in self.trap:
                    self._coord = self.left
                    return Agent.Action.FORWARD
                if self.down in self._safe_zones and self.down not in self.trap:
                    self._dir = "down"
                    return Agent.Action.TURN_LEFT
                if self.top in self._safe_zones and self.top not in self.trap:
                    self._dir = "top"
                    return Agent.Action.TURN_RIGHT
                else:
                    self._dir = "down"
                    return Agent.Action.TURN_LEFT
            elif self._dir == "down":
                if self.down in self._safe_zones and self.down not in self.trap:
                    self._coord = self.down
                    return Agent.Action.FORWARD
                if self.left in self._safe_zones and self.left not in self.trap:
                    self._dir = "left"
                    return Agent.Action.TURN_RIGHT
                if self.right in self._safe_zones and self.right not in self.trap:
                    self._dir = "right"
                    return Agent.Action.TURN_LEFT
                else:
                    self._dir = "left"
                    return Agent.Action.TURN_RIGHT

            elif self._dir == "right":
                if self.down in self._safe_zones and self.down not in self.trap:
                    self._dir = "down"
                    return Agent.Action.TURN_RIGHT
                if self.left in self._safe_zones and self.left not in self.trap:
                    self._dir = "down"
                    return Agent.Action.TURN_RIGHT

                if self.right in self._safe_zones and self.right not in self.trap:
                    self._coord = self.right
                    return Agent.Action.FORWARD
                else:
                    self._dir = "top"
                    return Agent.Action.TURN_LEFT

            elif self._dir == "top":
                # moving down and left have priority to other moves
                # since we want to go back to [1,1]
                # fix the code accordingly
                if self.left in self._safe_zones and self.left not in self.trap:
                    self._dir = "left"
                    return Agent.Action.TURN_LEFT
                if self.down in self._safe_zones and self.down not in self.trap:
                    self._dir = "left"
                    return Agent.Action.TURN_LEFT
                if self.top in self._safe_zones and self.top not in self.trap:
                    self._coord = self.top

                    return Agent.Action.FORWARD
                else:
                    self._dir = "left"
                    return Agent.Action.TURN_LEFT
        #############################################################################################
        else:
            if dest_node[0]<= self._coord[0] and dest_node[1]<= self._coord[1]:
                if self._dir == "left":
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._coord = self.left

                        return Agent.Action.FORWARD
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                elif self._dir == "down":
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._coord = self.down

                        return Agent.Action.FORWARD
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "right":
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT

                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._coord = self.right

                        return Agent.Action.FORWARD

                    else:
                            self._dir = "down"
                            return Agent.Action.TURN_RIGHT
                elif self._dir == "top":
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT

                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._coord = self.top

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT

            elif dest_node[0] >= self._coord[0] and dest_node[1] >= self._coord[1]:
                if self._dir == "right":
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._coord = self.right

                        return Agent.Action.FORWARD

                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "top":
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._coord = self.top

                        return Agent.Action.FORWARD
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT

                elif self._dir == "left":
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._coord = self.left

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT

                elif self._dir == "down":
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._coord = self.down

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT

            elif dest_node[0] <= self._coord[0] and dest_node[1] >= self._coord[1]:
                if self._dir == "left":

                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._coord = self.left

                        return Agent.Action.FORWARD

                    elif self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT

                    elif self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "top"
                        return Agent.Action.TURN_RIGHT

                if self._dir == "top":
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._coord = self.top

                        return Agent.Action.FORWARD
                    elif self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    elif self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT

                if self._dir == "down":
                    if self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    elif self.down in self._safe_zones and self.down not in self.trap:
                        self._coord = self.down

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                if self._dir == "right":
                    if self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    elif self.right in self._safe_zones and self.right not in self.trap:
                        self._coord = self.right

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT

            elif dest_node[0] >= self._coord[0] and dest_node[1] <= self._coord[1]:
                if self._dir == "right":
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._coord= self.right

                        return Agent.Action.FORWARD
                    elif self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones and self.top not in self.trap:
                        self._dir = "top"
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_RIGHT
                if self._dir == "down":
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._coord = self.down

                        return Agent.Action.FORWARD
                    elif self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones and self.left not in self.trap:
                        self._dir = "left"
                        return Agent.Action.TURN_RIGHT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_LEFT

                if self._dir == "left":
                    if self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    elif self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT
                    elif self.left in self._safe_zones and self.left not in self.trap:
                        self._coord= self.left

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "down"
                        return Agent.Action.TURN_LEFT

                if self._dir == "top":
                    if self.right in self._safe_zones and self.right not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    elif self.down in self._safe_zones and self.down not in self.trap:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT
                    elif self.top in self._safe_zones and self.top not in self.trap:
                        self._coord = self.top

                        return Agent.Action.FORWARD
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT