"""P2 Assignment, a game of Rock paper scissors with implementation of players with 
choice determination and tournaments."""
import random as r
import matplotlib.pyplot as plt

class Player:
    """Player superclass which has all the methods all players have in common. Also gives each
    player their id and records their moves"""
    counter = 0
    move_history = {}

    def __init__(self):
        self.player_id = Player.counter
        Player.counter += 1
        Player.move_history[self.player_id] = []
        self.name = self.enter_name()
        self.opponentid = None

    def select_action(self, chosen_choice):
        """Returns the action selected by subclasses"""
        return chosen_choice

    def set_opponent(self, opponent):
        """Sets this players opponent with their id to determine which moves to play"""
        self.opponentid = opponent

    def recieve_result(self, value):
        """Player class recieves result which is saved in the move_history dictionary"""
        Player.move_history[self.player_id].append(int(value))

    def enter_name(self):
        """The player enters their name which is saved in this instance of the class"""
        return input('Enter the name of the player:')

class Action:
    """This class contains a move chosen by a player, with also defined greater than or equal
    values"""
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
    """Picks a random move to play"""
    def select_action(self):
        return super().select_action(Action(r.randint(0,2)))

class Sequential(Player):
    """Plays the three moves in sequence no matter the opponents move"""
    def __init__(self):
        super().__init__()
        self.current = 0

    def select_action(self):
        self.counter += 1
        return super().select_action(Action(self.counter % 3))

class MostCommon(Player):
    """This player looks at the opponents most played move and counteracts it"""
    def select_action(self):
        tmp_1 = Player.move_history[self.opponentid]
        tmp_2 = [2, 0, 1]
        if not tmp_1:
            return super().select_action(Action(r.randint(0,2)))
        return super().select_action(Action(tmp_2[max(set(tmp_1), key = tmp_1.count)]))

class Historian(Player):
    """This player looks at the last (chosen amount of) moves and makes a move to
    counteract the historically most chosen moved after this sequence by the opponent"""
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
    """Class which contains the methods to conduct a single game between
    two players."""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1.set_opponent(player2.player_id)
        self.player2.set_opponent(player1.player_id)
        self.won = None
        self.player1_played = None
        self.player2_played = None

    def export_results(self, won):
        """Exports the results to the two players so they can save them to
        the move dictionary within their respected key"""
        self.player1.recieve_result(str(self.player1_played))
        self.player2.recieve_result(str(self.player2_played))
        self.won = won

    def perform_game(self):
        """Performs a single game between chosen players, both report
        a choice to the caller, which calculates who wins"""
        self.won = None
        self.player1_played = self.player1.select_action()
        self.player2_played = self.player2.select_action()

        if self.player1_played == self.player2_played:
            self.export_results(0)

        elif self.player1_played > self.player2_played:
            self.export_results(1)

        else:
            self.export_results(2)

    def show_results(self):
        """Displays the results as a string"""
        tmp_1 = ['Nobody', self.player1.__class__.__name__, self.player2.__class__.__name__]
        tmp_2 = ['Rock', 'Paper', 'Scissors']
        tmp_3 = '{} won. {} played {}, and {} played {}'.format(tmp_1[self.won], tmp_1[1], tmp_2[int(str(self.player1_played))], tmp_1[2], tmp_2[int(str(self.player2_played))])
        print(tmp_3)

class Tournament:
    """Tournament class for conducting games in test environment"""
    def __init__(self, player1, player2, number_of_games):
        self.game = SingleGame(player1, player2)
        self.number_of_games = number_of_games

    def arrange_single_game(self):
        """Calls function from single game class to arrange a single game"""
        self.game.perform_game()
        self.game.show_results()

    def arrange_tournament(self):
        """Arranges tournament with the two chosen players playing
        the set amount of games"""
        xpoints = []
        ypoints = []
        ratio = 0
        for i in range(self.number_of_games):
            xpoints.append(i+1)
            self.game.perform_game()
            if self.game.won == 1:
                ratio += 1
            elif self.game.won == 0:
                ratio += 0.5
            ypoints.append((ratio)/(i+1))
        tmp_1 = ((ratio)/(self.number_of_games))*100
        tmp_2 = 100 - tmp_1
        tmp_3 = 'Tournament has ended. {} has a win rate of {}%, and {} has a win rate of {}%'.format(self.game.player1.name, tmp_1, self.game.player2.name, tmp_2)
        plt.plot(xpoints, ypoints)
        plt.ylim([0,1])
        print(tmp_3)
        plt.show()

def main():
    """Main method"""
    player_1 = MostCommon()
    player_2 = Historian(4)
    stm = Tournament(player_1, player_2, 1000)
    stm.arrange_tournament()

if __name__ == "__main__":
    main()
