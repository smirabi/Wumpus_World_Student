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
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.bump = False
        self.scream = False

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
                self._safe_zones.remove(self._coord)   #added
                self._coord = self.left
            elif self._dir == "top":
                x = self._range[-1][0]
                self._range.clear()
                for i in range(x):
                    for j in range(self._coord[1] - 1):
                        self._range.append([i + 1, j + 1])
                self._safe_zones.remove(self._coord)    #added
                self._coord = self.down
            self._state.remove(self._state[-1])

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
            if (self.right in self._range) and (self.right not in self._safe_zones):
                self._potentialdanj.append(self.right)
            if (self.left in self._range) and (self.left not in self._safe_zones):
                self._potentialdanj.append(self.left)
            if (self.top in self._range) and (self.top not in self._safe_zones):
                self._potentialdanj.append(self.top)
            if (self.down in self._range) and (self.down not in self._safe_zones):
                self._potentialdanj.append(self.down)

    def getAction(self, stench, breeze, glitter, bump, scream):
        self.update_dir()
        self.update_senses(stench, breeze, glitter, bump, scream)

        if (breeze or stench) and (self._coord == [1, 1]):
            return Agent.Action.CLIMB
        self._count += 1

        if self._count != 1 and self.gold_grabbed and self._coord == [1, 1]:
            return Agent.Action.CLIMB

        if self.node_dict.count([1,1]) == 3:
            return Agent.Action.CLIMB
        self.calc_safety(stench, breeze, bump)

        if glitter:
            self.gold_grabbed = True
            return Agent.Action.GRAB

        if self.gold_grabbed :
            if self._coord == [1, 1]:
                return Agent.Action.CLIMB
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
        #############################################################################################
        else:
            

            if self._dir == "right":

                if self.right in self._safe_zones:
                    # if self.node_dict.count(self.right) == 3:
                    #     trackAndClimb()
                    # else:
                    self._coord = self.right
                    self.node_dict.append(self.right)
                    self.update_state()
                    return Agent.Action.FORWARD
                if self.top in self._safe_zones:
                    # if self.node_dict.count(self.top) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "top"
                    return Agent.Action.TURN_LEFT
                if self.down in self._safe_zones:
                    # if self.node_dict.count(self.down) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "down"
                  #  self.update_state()  new
                    return Agent.Action.TURN_RIGHT
                else:
                    self._dir = "top"
                    return Agent.Action.TURN_LEFT
            if self._dir == "top":
                if bump:
                    if self._coord[0]-1 >= 3:
                        self._dir = "left"
                     #   self.update_state()  new
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                      #  self.update_state()  new
                        return Agent.Action.TURN_RIGHT
                else:
                    if self.top in self._safe_zones:
                        # if self.node_dict.count(self.top) == 3:
                        #     trackAndClimb()
                        # else:
                        self._coord = self.top
                        self.node_dict.append(self.top)
                        self.update_state()
                        return Agent.Action.FORWARD
                    if self.right in self._safe_zones:
                        # if self.node_dict.count(self.right) == 3:
                        #     trackAndClimb()
                        # else:
                        self._dir = "right"
                    #    self.update_state()  new
                        return Agent.Action.TURN_RIGHT
                    if self.left in self._safe_zones:
                        # if self.node_dict.count(self.left) == 3:
                        #     trackAndClimb()
                        # else:
                        self._dir = "left"
                    #    self.update_state()  new
                        return Agent.Action.TURN_LEFT
                    else:
                        self._dir = "right"
                        return Agent.Action.TURN_RIGHT

            if self._dir == "down":
                if self.down in self._safe_zones:
                    # if self.node_dict.count(self.down) == 3:
                    #     trackAndClimb()
                    # else:
                    self._coord = self.down
                    self.node_dict.append(self.down)
                    self.update_state()
                    return Agent.Action.FORWARD
                if self.left in self._safe_zones:
                    # if self.node_dict.count(self.left) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "left"
                 #   self.update_state()
                    return Agent.Action.TURN_RIGHT
                if self.right in self._safe_zones:
                    # if self.node_dict.count(self.right) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "right"
                 #   self.update_state()
                    return Agent.Action.TURN_LEFT
                else:
                    self._dir = "right"
                    return Agent.Action.TURN_LEFT

            if self._dir == "left":
                if self.left in self._safe_zones:
                    # if self.node_dict.count(self.left) == 3:
                    #     trackAndClimb()
                    # else:
                    self._coord = self.left
                    self.node_dict.append(self.left)
                    self.update_state()
                    return Agent.Action.FORWARD
                if self.top in self._safe_zones:
                    # if self.node_dict.count(self.top) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "top"
                #    self.update_state()
                    return Agent.Action.TURN_RIGHT
                if self.down in self._safe_zones:
                    # if self.node_dict.count(self.down) == 3:
                    #     trackAndClimb()
                    # else:
                    self._dir = "down"
                 #   self.update_state()
                    return Agent.Action.TURN_LEFT
                else:
                    self._dir = "top"
                    return Agent.Action.TURN_RIGHT