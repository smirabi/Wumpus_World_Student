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

class MyAI ( Agent ):

    def __init__ ( self ):
        self._count = 0
        self._cord = (0,0)
        self._dir = "right"
        self._state = [[self._count, self._dir, self._cord]]


    def getAction( self, stench, breeze, glitter, bump, scream ):
        if glitter:
            return Agent.Action.GRAB
        if stench:
            return Agent.Action.TURN_LEFT
        if breeze:
            return Agent.Action.CLIMB
        if bump:
            return Agent.Action.TURN_RIGHT
        if scream:
            return Agent.Action.FORWARD


    