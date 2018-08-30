import random
import matplotlib.pyplot as plt

class Board:
    def __init__(self):
        self.board=[0]*9

    def place(self, mark, position):
        if self.board[position] != 0:
            raise ValueError('Tried to play at an already taken position')
        self.board[position] = mark

    def isWinner(self, player):
        # Horizontal
        if all(i==player for i in self.board[0:3]):
            return True
        if all(i==player for i in self.board[3:6]):
            return True
        if all(i==player for i in self.board[6:9]):
            return True

        # Vertical
        if all([self.board[i]==player for i in (0, 3, 6)]):
            return True
        if all([self.board[i]==player for i in (1, 4, 7)]):
            return True
        if all([self.board[i]==player for i in (2, 5, 8)]):
            return True
        # Diagonal
        if all([self.board[i]==player for i in (0, 4, 8)]):
            return True
        if all([self.board[i]==player for i in (2, 4, 6)]):
            return True
        return False

    def boardFull(self):
        return not any([i==0 for i in self.board])

    def getPossibleActions(self):
        return([i for i in range(9) if self.board[i]==0])

    def __str__(self):
        return( str(self.board[0]) + '\t|\t' + str(self.board[1]) + '\t|\t' +str(self.board[2]) +'\n' +
                '-------------------------------------\n' +
                str(self.board[3]) + '\t|\t' + str(self.board[4]) + '\t|\t' +str(self.board[5]) +'\n' +
                '-------------------------------------\n' +
                str(self.board[6]) + '\t|\t' + str(self.board[7]) + '\t|\t' +str(self.board[8]) + '\n' )



class Player:

    def action(self, board):
        raise NotImplementedError(self + ' has not implemented an action-method.')

    def gameOver(self, points):
        for board_map, action in self.history:
            if board_map in self.Q:
                self.Q[board_map][action] += points
            else:
                self.Q[board_map] = [0]*9
                self.Q[board_map][action] += points
        self.history = []

    def __str__(self):
        return type(self).__name__ + '' + str(self.mark)

class RandomPlayer(Player):

    def __init__(self, mark):
        self.mark = mark
        self.history = []

    def action(self, board):
        possible_actions = board.getPossibleActions()
        choice =  random.choice(possible_actions)
        board.place(self.mark, choice)
        return choice

class QPlayer(Player):
    def __init__(self, mark):
        self.mark = mark
        self.Q = {}
        self.history = []

    def action(self,board):
        def l(x):
            if x == self.mark:
                return 'x'
            elif x == 0:
                return '0'
            else:
                return 'o'

        possible_actions = board.getPossibleActions()
        board_map = ''.join(map(l, board.board))

        if board_map in self.Q:
            rewards = [self.Q[board_map][i] for i in range(9) if i in possible_actions]
            choice =  possible_actions[rewards.index(max(rewards))]
        else:
            choice = random.choice(possible_actions)

        self.history.append((board_map, choice))
        board.place(self.mark, choice)
        return choice


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
        self.result = -1

    def play(self):
        result = 0
        while(True):
            self.player1.action(self.board)
            if self.board.isWinner(self.player1.mark):
                result = self.player1.mark
                self.notifyGameOver(self.player1.mark)
                break
            if self.board.boardFull():
                result = self.player2.mark
                self.notifyGameOver(0)
                break
            self.player2.action(self.board)
            if self.board.isWinner( self.player2.mark):
                self.notifyGameOver(self.player2.mark)
                break
        self.result = result

    def notifyGameOver(self, winner):
        if winner==self.player1.mark:
            self.player1.gameOver(10)
            self.player2.gameOver(-10)
        elif winner == self.player2.mark:
            self.player2.gameOver(10)
            self.player1.gameOver(-10)
        else:
            self.player1.gameOver(2)
            self.player2.gameOver(2)



class Tournament:
    def __init__(self, player1, player2, n_games = 100):
        self.player1 = player1
        self.player2 = player2
        self.n_games = n_games
        self.history = []

    def play(self):
        for i in range(self.n_games):
            game = Game(self.player1, self.player2)
            game.play()
            self.history.append(game.result)
    def getScore(self):
        p1 = self.history.count(self.player1.mark)
        p2 = self.history.count(self.player2.mark)
        draw = self.history.count(0)
        return (p1, p2, draw)
    def plotProgress(self):
        p1 = [self.history[0:(i+1)].count(self.player1.mark) for i in range(self.n_games)]
        p2 = [self.history[0:(i+1)].count(self.player2.mark)for i in range(self.n_games)]
        draw = [self.history[0:(i+1)].count(0) for i in range(self.n_games)]
        plt.plot(p1, 'r')
        plt.plot(p2, 'b')
        plt.plot(draw, 'y')
        plt.show()


p1 = QPlayer(1)
p2 = RandomPlayer(2)

t = Tournament(p1, p2, 100)
t.play()
print(t.getScore())
t.plotProgress()
