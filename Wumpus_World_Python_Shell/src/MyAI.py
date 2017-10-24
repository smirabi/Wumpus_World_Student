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


class MyAI ( Agent ):

    def __init__(self):
        self._count = 0
        self._coord = [1, 1]
        self._dir = "right"
        self._senses = []
        self._potentialdanj = []
        self._safe_zones = [[1, 1]]
        self.node_dict = defaultdict(lambda: 0)
        # self.node_dict[[1, 1]] = 1
        self._state = [[self._dir, self._coord]]
        self._range =[]
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
        if bump:
            if self._dir == "right":
                for i in range(len(self._range)):
                    if self._range[i][0]== self._coord[0]+1:
                        self._range.remove(self._range[i])
            elif self._dir == "top":
                for i in range(len(self._range)):
                    if self._range[i][1]== self._coord[1]+1:
                        self._range.remove(self._range[i])
        if not stench and not breeze:
            if self.right in self._range:
                self._safe_zones.append(self.right)
            if self.left in self._range:
                self._safe_zone.append(self.left)
            if self.top in self._range:
                self._safe_zones.append(self.top)
            if self.down in self._range:
                self._safe_zones.append(self.down)
        else:
            if (self.right in self._range) and (self.right not in self._safe_zones):
                self._potentialdanj.append(self.right)
            if (self.left in self._range) and (self.left not in self._safe_zones):
                self._potentialdanj.append(self.left)
            if (self.top in self._range) and (self.top not in self._safe_zones):
                self._potentialdanj.append(self.top)
            if (self.down in self._range) and (self.down not in self._safe_zones):
                self._potentialdanj.append(self.down)

    def trackAndClimb(self):
        if self._coord == [1, 1]:
            return Agent.Action.CLIMB
        l = len(self.shortest_path)
        if l == 0:
            for s in self._state:
                if s[1] != self._coord:
                    self.shortest_path.append(s)
                else:
                    break
        else:
            for i in range(l +1 , 0, -1):
                self.go_back(self.shortest_path, i)

    def go_back(self, path, i):
        if self._coord == [1,1]:
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
            if self._dir== "down":
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
        self._count += 1
        self.calc_safety(stench, breeze, bump)
        if self.gold_grabbed:
            self.trackAndClimb()

        if glitter:
            self.gold_grabbed = True
            return Agent.Action.GRAB

        if self._dir == "right":
            if self.right in self._safe_zones:
                if self.node_dict[self.right] == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.right
                    self.node_dict[self.right] += 1
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.top in self._safe_zones:
                if self.node_dict[self.top] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "top"
                    self.update_state()
                    return Agent.Action.TURN_LEFT
            if self.down in self._safe_zones:
                if self.node_dict[self.down] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "down"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT

        if self._dir == "top":
            if self.top in self._safe_zones:
                if self.node_dict[self.top] == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.top
                    self.node_dict[self.top] += 1
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.right in self._safe_zones:
                if self.node_dict[self.right] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "right"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            if self.left in self._safe_zones:
                if self.node_dict[self.left] ==3:
                    self.trackAndClimb()
                else:
                    self._dir = "left"
                    self.update_state()
                    return Agent.Action.TURN_LEFT

        if self._dir == "down":
            if self.down in self._safe_zones:
                if self.node_dict[self.down] == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.down
                    self.node_dict[self.down] += 1
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.left in self._safe_zones:
                if self.node_dict[self.left] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "right"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            if self.right in self._safe_zones:
                if self.node_dict[self.right] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "left"
                    self.update_state()
                    return Agent.Action.TURN_LEFT

        if self._dir == "left":
            if self.left in self._safe_zones:
                if self.node_dict[self.left] == 3:
                    self.trackAndClimb()
                else:
                    self._coord = self.left
                    self.node_dict[self.left] += 1
                    self.update_state()
                    return Agent.Action.FORWARD
            if self.top in self._safe_zones:
                if self.node_dict[self.top] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "top"
                    self.update_state()
                    return Agent.Action.TURN_RIGHT
            if self.down in self._safe_zones:
                if self.node_dict[self.down] == 3:
                    self.trackAndClimb()
                else:
                    self._dir = "down"
                    self.update_state()
                    return Agent.Action.TURN_LEFT
