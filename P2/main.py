import random as r
from itertools import groupby as group

class Player:

    counter = 0
    move_history = {}

    def __init__(self):
        self.id = counter
        counter += 1
        Player.move_history[self.id] = []
    def select_action(self, action):
        return action

    def set_opponent(self, opponent):
        self.opponent = opponent

    def recieve_result(self):
        return None

    def enter_name(self, name):
        self.playername = name

class Action:
    def __init__(self, value):
        self.value = value
    
    def __gt__(self, value):
        tmp_1 = [2,0,1]
        return value == tmp_1[self.value]
    
    def __eq__(self, value):
        return self.action == value

class Random(Player):
    def __init__(self):
        super().__init__()

    def select_action(self, action):
        return super().select_action(Action(r.randint(0,2)))

class Sequential(Player):
    def __init__(self):
        super().__init__()
        self.current = 0

    def select_action(self, action):
        self.counter += 1
        return super().select_action(Action(self.counter % 3))

class MostCommon(Player):
    def __init__(self):
        super().__init__()

    def select_action(self, action):
        tmp_1 = Player.move_history[self.opponent-1]
        return super().select_action(Action(max(set(tmp_1), key = tmp_1.count)))

class Historian(Player):
    def __init__(self, depth):
        self.depth = depth
        super().__init__()

    def select_action(self, action):
        tmp_1 = []
        try:
            tmp1_1 = Player.move_history[self.opponent-1][-2:]
        except:
            tmp_1 = [r.randint(0,2), r.randint(0,2)]
        return super().select_action(action)


def main():
   """main"""
   
if __name__ == "__main__":
    main()