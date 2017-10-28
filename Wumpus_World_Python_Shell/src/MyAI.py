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
from collections import defaultdict


class MyAI(Agent):
    def __init__(self):
        self._count = 0
        self._coord = [1, 1]
        self._dir = "right"
        self._senses = []
        self._potentialdanj = []
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

    def update_state(self):
        self._state.append([self._count, self._dir, self._coord])

    def calc_safety(self, stench, breeze, bump):
        print("BUMP", bump)
        if bump:
            print("got into bump!!!!!")
            if self._dir == "right":
                print("right")
                y = self._range[-1][1]
                self._range.clear()
                for i in range(self._coord[0] - 1):
                    for j in range(y):
                        self._range.append([i + 1, j + 1])
                self._safe_zones.remove(self._coord)   #added
                self._coord = self.left
                print(self._range)


            elif self._dir == "top":
                x = self._range[-1][0]
                self._range.clear()
                for i in range(x):
                    for j in range(self._coord[1] - 1):
                        self._range.append([i + 1, j + 1])
                self._safe_zones.remove(self._coord)    #added
                self._coord = self.down
                print(self._range)


        if not stench and not breeze:
            if self.right in self._range and self.right not in self._safe_zones:
                self._safe_zones.append(self.right)
            if self.left in self._range and self.left not in self._safe_zones:
                self._safe_zones.append(self.left)
            if self.top in self._range and self.top not in self._safe_zones:
                self._safe_zones.append(self.top)
            if self.down in self._range and self.down not in self._safe_zones:
                self._safe_zones.append(self.down)
        else:
            print("breeze or stench")
            if (self.right in self._range) and (self.right not in self._safe_zones):
                self._potentialdanj.append(self.right)
            if (self.left in self._range) and (self.left not in self._safe_zones):
                self._potentialdanj.append(self.left)
            if (self.top in self._range) and (self.top not in self._safe_zones):
                self._potentialdanj.append(self.top)
            if (self.down in self._range) and (self.down not in self._safe_zones):
                self._potentialdanj.append(self.down)

    def trackAndClimb(self):
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
        else:
            for i in range(len(self.shortest_path) - 1, -1, -1):
                self.go_back(self.shortest_path, i)

    def go_back(self, path, i):
        print("GOING BACK")
        if self._coord == [1, 1]:
            return Agent.Action.CLIMB
        if path[i][0] == "right":
            if self._dir == "left":
                path.pop(i)
                self._coord = self.left
                return Agent.Action.FORWARD
            else:
                return Agent.Action.TURN_LEFT
        if path[i][0] == "left":
            if self._dir == "right":
                path.pop(i)
                self._coord = self.right
                return Agent.Action.FORWARD
            else:
                return Agent.Action.TURN_LEFT
        if path[i][0] == "top":
            if self._dir == "down":
                path.pop(i)
                self._coord = self.down
                return Agent.Action.FORWARD
            else:
                return Agent.Action.TURN_LEFT
        if path[i][0] == "down":
            if self._dir == "top":
                path.pop(i)
                self._coord = self.top
                return Agent.Action.FORWARD
            else:
                return Agent.Action.TURN_LEFT

    def getAction(self, stench, breeze, glitter, bump, scream):
        print(self._coord, "Before")
        self.right = [self._coord[0] + 1, self._coord[1]]
        self.left = [self._coord[0] - 1, self._coord[1]]
        self.top = [self._coord[0], self._coord[1] + 1]
        self.down = [self._coord[0], self._coord[1] - 1]
        if (breeze or stench) and (self._coord == [1, 1]):
            return Agent.Action.CLIMB
        self._count += 1
        if (self._count != 1 and self.gold_grabbed and self._coord == [1, 1]):
             return Agent.Action.CLIMB
        if self.node_dict.count([1,1]) == 3:
            return Agent.Action.CLIMB
        print("bump in getAcytion:", bump)
        self.calc_safety(stench, breeze, bump)
        if self.gold_grabbed:
            print("HERE1")
            self.trackAndClimb()
        if glitter:

            self.gold_grabbed = True
            return Agent.Action.GRAB
        # if self.gold_grabbed and self._coord == [1,1]:
        #     print("HERE2")
        #     return Agent.Action.CLIMB

        if self._dir == "right":
            print(stench, breeze)
            if self.right in self._safe_zones:
                if self.node_dict.count(self.right) == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.right
                    self.node_dict.append(self.right)
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.top in self._safe_zones:
                if self.node_dict.count(self.top) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "top"
                    self.update_state()
                    return Agent.Action.TURN_LEFT
            if self.down in self._safe_zones:
                if self.node_dict.count(self.down) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "down"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            else:
                self._dir = "top"
                return Agent.Action.TURN_LEFT

        if self._dir == "top":
            if bump:
                if self._coord[0]-1 >= 3:
                    self._dir = "left"
                    return Agent.Action.TURN_LEFT
                else:
                    self._dir = "right"
                    return Agent.Action.TURN_RIGHT
            else:
                if self.top in self._safe_zones:
                    if self.node_dict.count(self.top) == 3:
                        self.trackAndClimb()
                    else:
                        self._coord = self.top
                        self.node_dict.append(self.top)
                        self.update_state()
                        return Agent.Action.FORWARD
                if self.right in self._safe_zones:
                    if self.node_dict.count(self.right) == 3:
                        self.trackAndClimb()
                    else:
                        self._dir = "right"
                        self.update_state()
                        return Agent.Action.TURN_RIGHT
                if self.left in self._safe_zones:
                    if self.node_dict.count(self.left) == 3:
                        self.trackAndClimb()
                    else:
                        self._dir = "left"
                        self.update_state()
                        return Agent.Action.TURN_LEFT
                else:
                    self._dir = "right"
                    return Agent.Action.TURN_RIGHT

        if self._dir == "down":
            if self.down in self._safe_zones:
                if self.node_dict.count(self.down) == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.down
                    self.node_dict.append(self.down)
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.left in self._safe_zones:
                if self.node_dict.count(self.left) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "left"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            if self.right in self._safe_zones:
                if self.node_dict.count(self.right) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "right"
                    self.update_state()
                    return Agent.Action.TURN_LEFT
            else:
                self._dir = "right"
                return Agent.Action.TURN_LEFT

        if self._dir == "left":
            if self.left in self._safe_zones:
                if self.node_dict.count(self.left) == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.left
                    self.node_dict.append(self.left)
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.top in self._safe_zones:
                if self.node_dict.count(self.top) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "top"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            if self.down in self._safe_zones:
                if self.node_dict.count(self.down) == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "down"
                    self.update_state()
                    return Agent.Action.TURN_LEFT
            else:
                self._dir = "top"
                return Agent.Action.TURN_RIGHT