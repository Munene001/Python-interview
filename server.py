import zerorpc
import sys

PORT = 4011

playersTurn = 1
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

current_player = 1
gamever = False

class HelloRPC(object):

    def __init__(self) -> None:
        self.players = []

    def enterGame(self, name):
        if len(self.players) > 2:
            mes = "Game full"
            print(mes)
            return mes
        if name in self.players:
            print("name taken")
            return "Name taken"
        self.players += [name]
        print("new client", name)
        return "yes"

    def isGameReady(self):
        return len(self.players) >= 2

    def playerPos(self, name):
        if name not in self.players:
            return -1
        return self.players.index(name)+1

    def sendMove(self, name, row, col):
        if not self.isGameReady():
            return ["Not playing", ""]
        pos = self.playerPos(name)
        if pos == -1 or current_player != pos:
            return ["Not a player now", ""]
        res = self.addMove(row, col)
        return res

    def addMove(self, row, col):
        global current_player
        global board
        print("Made move", row, col)
        if board[row][col] == 0:
            if current_player == 1:
                board[row][col] = "X"
                current_player = 2
            else:
                board[row][col] = "O"
                current_player = 1

            text = board[row][col]
            winner = self.check_for_winner()
            return [text, winner]
        else:
            ["", None]

    def check_for_winner(self):
        global board, gamever
        winner = None
        for row in board:
            if row.count(row[0]) == len(row) and row[0] != 0:
                winner = row[0]
                break
        for col in range(len(board)):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
                winner = board[0][col]
                break
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            winner = board[0][0]
        elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            winner = board[0][2]
        if all([all(row) for row in board]) and winner is None:
            winner = "tie"
        if winner:
            gamever = winner
        return winner

    def getBoard(self):
        global board
        return board

    def getPlayer(self):
        return playersTurn

    def getGameover(self):
        return gamever
    
    def resetGame(self):
        global playersTurn, board, current_player, gamever
        playersTurn = 1
        board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        current_player = 1
        gamever = False


if len(sys.argv) >= 2:
    PORT = int(sys.argv[1])

s = zerorpc.Server(HelloRPC())
s.bind(f"tcp://0.0.0.0:{PORT}")
print("Server running on port ", PORT)
s.run()
