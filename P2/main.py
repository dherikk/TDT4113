import random as r

class Player:

    counter = 0
    move_history = {}

    def __init__(self):
        self.id = counter
        Player.counter += 1
        Player.move_history[self.id] = []
    def select_action(self, action):
        return action

    def set_opponent(self, opponent):
        self.opponentid = opponent

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

    def __str__(self):
        return str(self.value)

    

class Random(Player):
    def __init__(self):
        super().__init__()

    def select_action(self):
        return super().select_action(Action(r.randint(0,2)))

class Sequential(Player):
    def __init__(self):
        super().__init__()
        self.current = 0

    def select_action(self):
        self.counter += 1
        return super().select_action(Action(self.counter % 3))

class MostCommon(Player):
    def __init__(self):
        super().__init__()

    def select_action(self):
        tmp_1 = Player.move_history[self.opponentid]
        return super().select_action(Action(max(set(tmp_1), key = tmp_1.count)))

class Historian(Player):
    def __init__(self, depth):
        self.depth = depth
        super().__init__()

    def select_action(self):
        try:
            tmp_1 = Player.move_history[self.opponentid]
            tmp_2 = tmp_1[self.depth * -1:]
            tmp_3 = [(i+len(tmp_2)) for i in range(len(tmp_1)-self.depth) if tmp_1[i:i+len(tmp_2)] == tmp_2]
            tmp_4 = [tmp_1[i] for i in tmp_3]
            return super().select_action(Action(max(set(tmp_4), key = tmp_4.count)))
        except:
            return super().select_action(Action(r.randint(0,2)))
    
class SingleGame:

    def __init__(self, player1, player2):        
        self.player1.set_opponent(player2.id)
        self.player2.set_opponent(player1.id)
        self.p1_points = 0
        self.p2_points = 0
    
    def perform_game(self):
        tmp_1 = self.player1.select_action()
        tmp_2 = self.player2.select_action()

        if tmp_1 > tmp_2:
            self.p1_points += 1
        elif tmp_1 == tmp_2:
            self.p1_points += 0.5
            self.p2_points += 0.5
        else:
            self.p2_points += 1

# Husk å endre action-klassen fra value til action
        



def main():
    print('test')
    """main"""
   
if __name__ == "__main__":
    main()