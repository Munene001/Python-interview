import zerorpc
import tkinter as tk
from tkinter import messagebox
import sys

PORT = 4011

if len(sys.argv) >=2:
    PORT = int(sys.argv[1])


current_player = 0
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
name = ''


def createGame(con):
    window = tk.Tk()
    window.title("Tic Tac Toe")

    # Create board
    def create_board():
        for i in range(3):
            for j in range(3):
                button = tk.Button(window, text="", font=("Arial", 50), height=2, width=6,
                                   bg="lightblue", command=lambda row=i, col=j: handle_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")

    create_board()

    # Handle button clicks
    def handle_click(row, col):
        global name
        global current_player

        text, winner = con.sendMove(name, row, col)
        print(text, winner)
        if winner:
            declare_winner(winner)

    # Declare the winner and ask to restart the game
    def declare_winner(winner):
        if winner == "tie":
            message = "It's a tie!"
        else:
            message = f"Player {winner} wins!"

        answer = messagebox.askyesno(
            "Game Over", message + " Do you want to restart the game?")

        if answer:
            global board
            con.resetGame()
        else:
            window.quit()

    def update():
        global board
        global current_player
        board = con.getBoard()
        current_player = con.getPlayer()
        winner = con.getGameover()
        if winner:
            declare_winner(winner)

        for i in range(3):
            for j in range(3):
                button = window.grid_slaves(row=i, column=j)[0]
                val = board[i][j]
                val = "" if val == 0 else val
                button.config(text= val)

        window.after(500, update)

    window.after(500, update)
    window.mainloop()

def main():
    global name
    c = zerorpc.Client()
    c.connect(f"tcp://127.0.0.1:{PORT}")
    name = input("Enter player name: ")

    entered = c.enterGame(name)
    if entered == 'yes':
        print("Entry accepted")
    else:
        print(entered)
        return

    createGame(c)


main()
