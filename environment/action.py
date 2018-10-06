from enum import IntEnum

class ActionType(IntEnum):
    HINT = 0
    PLAY = 1
    DISCARD = 2

class Action(object):
    def __init__(self, action_type, target, index, color, value):
        self.action_type = action_type
        self.target = target
        self.index = index
        self.color = color
        self.value = value
