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

    def __init__ ( self ):
        self._count = 0
        self._coord = [1, 1]
        self._dir = "right"
        self._senses = []
        self._potentialdanj = []
        self._safe_zones = [[1,1]]
        self.node_dict = defaultdict(lambda : 0)
        self.node_dict[[1,1]] = 1
        self._state = [[self._count, self._dir, self._coord, self._senses]]
        self._range =[]

    def update_coord(self):
        if self._dir == "right":
            self._coord[0] += 1
        elif self._dir == "left":
            self.coord[0] -= 1
        elif self._dir == "top":
            self._coord[1] += 1
        else:
            self._coord[1] -= 1
        return self._coord

    def get_coord(self):
        return self._coord

    def update_state(self, count, direction, coord, senses):
        # self._count = count
        # self._dir = dir
        # self._coord = coord
        # self._senses.append(i for i in senses)
        self._state.append([count, direction, coord, senses])

    def calc_safety(self, stench, breeze, bump):

        a = [self._coord[0] + 1, self._coord[1]]
        b = [self._coord[0] - 1, self._coord[1]]
        c = [self._coord[0], self._coord[1] + 1]
        d = [self._coord[0], self._coord[1] - 1]

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
             if a in self._range:
                 self._safe_zones.append(a)
             if b in self._range:
                self._safe_zone.append(b)
             if c in self._range:
                 self._safe_zones.append(c)
             if d in self._range:
                 self._safe_zones.append(d)

        else:
            if (a in self._range) and (a not in self._safe_zones):
                self._potentialdanj.append(a)
            if (b in self._range) and (b not in self._safe_zones):
                self._potentialdanj.append(b)
            if (c in self._range) and (c not in self._safe_zones):
                self._potentialdanj.append(c)
            if (d in self._range) and (d not in self._safe_zones):
                self._potentialdanj.append(d)


    def getAction(self, stench, breeze, glitter, bump, scream):
        self._count += 1
        self.calc_safety(stench, breeze, bump)
        if glitter:
            self.update_state(self._count, self._dir, self.get_coord(), self._senses)
            return Agent.Action.GRAB
        # if stench:
        #     if self._coord == [1, 1]:
        #         return Agent.Action.CLIMB
        #     else:
        #         if [self._coord[0] + 1, self._coord[1]] in self._safe_zones:
        #             self.update_state(self._count, self._dir, self.update_coord(), self._senses)
        #             return Agent.Action.FORWARD
        #         elif [self._coord[0], self._coord[1] +1] in self._safe_zones:
        #             self._dir = "top"
        #             return Agent.Action.TURN_LEFT
        #
        # if breeze:
        #     return Agent.Action.CLIMB
        # if bump:
        #     return Agent.Action.TURN_RIGHT
        # if scream:
        #     return Agent.Action.FORWARD

        right = [self._coord[0] + 1, self._coord[1]]
        left = [self._coord[0] - 1, self._coord[1]]
        top = [self._coord[0], self._coord[1] + 1]
        down = [self._coord[0], self._coord[1] - 1]

        if self._dir == "right":
            if right in self._safe_zones:
                if (self.node_dict[right] ) == 2:
                    #call trace back and climb
                else:
                    self.node_dict[right] += 1
                    return Agent.Action.FORWARD
            if top in self._safe_zones:
                self._dir = "top"
                return Agent.Action.TURN_LEFT
            if down in self._safe_zones:
                self._dir = "down"
                return Agent.Action.TURN_RIGHT

        if self._dir == "top":
            if top in self._safe_zones:
                self.node_dict[top] += 1
                return Agent.Action.FORWARD
            if right in self._safe_zones:
                self._dir = "right"
                return Agent.Action.TURN_RIGHT
            if left in self._safe_zones:
                self._dir = "left"
                return Agent.Action.TURN_LEFT

        if self._dir == "down":
            if down in self._safe_zones:
                self.node_dict[down] += 1
                return Agent.Action.FORWARD
            if left in self._safe_zones:
                self._dir = "right"
                return Agent.Action.TURN_RIGHT
            if right in self._safe_zones:
                self._dir = "left"
                return Agent.Action.TURN_LEFT

        if self._dir == "left":
            if left in self._safe_zones:
                self.node_dict[left] += 1
                return Agent.Action.FORWARD
            if top in self._safe_zones:
                self._dir = "top"
                return Agent.Action.TURN_RIGHT
            if down in self._safe_zones:
                self._dir = "down"
                return Agent.Action.TURN_LEFT





