from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import random

app = Flask(__name__)

# Configurer Flask Session
app.config["SESSION_TYPE"] = "filesystem"  # Fixed syntax error
app.config["SECRET_KEY"] = "supersecretkey"
Session(app)

# Spillbrettets dimensjoner
ROWS = 5
COLS = 5

# Initialiser spillbrettet
def initialize_board():
    board = [[False for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range(random.randint(10, 20)):  # Apply a random number of moves to ensure solvability
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        toggle(board, row, col)
    return board

# Bytt statusen til en celle og dens naboer
def toggle(board, row, col):
    board[row][col] = not board[row][col]
    if row > 0:
        board[row - 1][col] = not board[row - 1][col]
    if row < ROWS - 1:
        board[row + 1][col] = not board[row + 1][col]
    if col > 0:
        board[row][col - 1] = not board[row][col - 1]
    if col < COLS - 1:
        board[row][col + 1] = not board[row][col + 1]

# Sjekk om spilleren har vunnet
def check_victory(board):
    return all(not cell for row in board for cell in row)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'board' not in session:
        session['board'] = initialize_board()

    board = session['board']

    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        toggle(board, row, col)
        session['board'] = board

        if check_victory(board):
            return redirect(url_for('victory'))

    return render_template('index.html', board=board, enumerate=enumerate)  # Pass enumerate to the template

@app.route('/restart')
def restart():
    session['board'] = initialize_board()
    return redirect(url_for('index'))

@app.route('/victory')
def victory():
    return "<h1>Gratulerer! Du har slått av alle lysene!</h1><a href='/'>Spill igjen</a>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Make the app accessible on the local network

