import random as r

class Player:

    counter = 0
    move_history = {}

    def __init__(self):
        self.id = Player.counter
        Player.counter += 1
        Player.move_history[self.id] = []
    def select_action(self, action):
        return action

    def set_opponent(self, opponent):
        self.opponentid = opponent

    def recieve_result(self, value):
        Player.move_history[self.id].append(int(value))

    def enter_name(self, name):
        self.playername = name

class Action:
    def __init__(self, value):
        self.value = value
    
    def __gt__(self, action):
        tmp_1 = [2,0,1]
        return action.value != tmp_1[self.value]
    
    def __eq__(self, action):
        return self.value == action.value

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
        if not tmp_1:
            return super().select_action(Action(r.randint(0,2)))
        else:
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
            tmp_5 = [2, 0, 1]
            return super().select_action(Action(tmp_5[max(set(tmp_4), key = tmp_4.count)]))
        except:
            return super().select_action(Action(r.randint(0,2)))
    
class SingleGame:

    def __init__(self, player1, player2):      
        self.player1 = player1
        self.player2 = player2  
        self.player1.set_opponent(player2.id)
        self.player2.set_opponent(player1.id)
        self.p1_points = 0
        self.p2_points = 0
    
    def perform_game(self):
        tmp_1 = self.player1.select_action()
        tmp_2 = self.player2.select_action()


        print('Player 1 plays: ' + str(tmp_1))
        print('Player 2 plays: ' + str(tmp_2))

       
        if tmp_1 == tmp_2:
            self.p1_points += 0.5
            self.p2_points += 0.5
            self.player1.recieve_result(str(tmp_1))
            self.player2.recieve_result(str(tmp_2))
            print('Its a tie')
        elif tmp_1 > tmp_2:
            self.p1_points += 1
            self.player1.recieve_result(str(tmp_1))
            self.player2.recieve_result(str(tmp_2))
            print('Player 1 wins')
        else:
            self.p2_points += 1
            self.player1.recieve_result(str(tmp_1))
            self.player2.recieve_result(str(tmp_2))
            print('Player 2 wins')

def main():
    p1 = MostCommon()
    p2 = Historian(1)
    sg1 = SingleGame(p1, p2)
    i = 0
    while i < 100:
        sg1.perform_game()
        i += 1
    print(Player.move_history)
    print('Player 1 points: '+ str(sg1.p1_points))
    print('Player 2 points: '+ str(sg1.p2_points))

if __name__ == "__main__":
    main()