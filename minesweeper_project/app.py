from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)
SIZE = 10
MINES = 20

game_state = {
    'board': [],
    'flags': [],
    'revealed': [],
    'player': 1,
    'turn': "Lượt của người chơi 1",
    'winner': None      
}


def initialize_game():
    game_state['board'] = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    game_state['flags'] = [[False for _ in range(SIZE)] for _ in range(SIZE)]
    game_state['revealed'] = [[False for _ in range(SIZE)] for _ in range(SIZE)]
    game_state['player'] = 1
    game_state['turn'] = "Lượt của người chơi 1"

    mines_placed = 0
    while mines_placed < MINES:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if game_state['board'][x][y] == 0:
            game_state['board'][x][y] = -1
            mines_placed += 1

    for i in range(SIZE):
        for j in range(SIZE):
            if game_state['board'][i][j] == -1:
                continue
            count = 0
            for ni in range(max(0, i - 1), min(SIZE, i + 2)):
                for nj in range(max(0, j - 1), min(SIZE, j + 2)):
                    if game_state['board'][ni][nj] == -1:
                        count += 1
            game_state['board'][i][j] = count

def reveal_empty_cells(x, y):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if not game_state['revealed'][cx][cy]:
            game_state['revealed'][cx][cy] = True
            if game_state['board'][cx][cy] == 0:
                for nx in range(max(0, cx - 1), min(SIZE, cx + 2)):
                    for ny in range(max(0, cy - 1), min(SIZE, cy + 2)):
                        if not game_state['revealed'][nx][ny] and game_state['board'][nx][ny] != -1:
                            stack.append((nx, ny))

@app.route('/')
def index():
    return render_template('index.html', game_state=game_state)

@app.route('/new_game', methods=['POST'])
def new_game():
    initialize_game()
    return jsonify(game_state)

@app.route('/click_cell', methods=['POST'])
def click_cell():
    data = request.json
    x, y = data['x'], data['y']
    if game_state['board'][x][y] == -1:
        game_state['turn'] = 'Game Over'
        game_state['revealed'] = [[True for _ in range(SIZE)] for _ in range(SIZE)]
        game_state['winner'] = game_state['player']
    else:
        reveal_empty_cells(x, y)
        game_state['turn'] = f"Lượt của người chơi {3 - game_state['player']}"
        game_state['player'] = 3 - game_state['player']
        game_state['winner'] = None
    return jsonify(game_state)


@app.route('/place_flag', methods=['POST'])
def place_flag():
    data = request.json
    x, y = data['x'], data['y']
    game_state['flags'][x][y] = not game_state['flags'][x][y]
    game_state['turn'] = f"Lượt của người chơi {3 - game_state['player']}"
    game_state['player'] = 3 - game_state['player']
    return jsonify(game_state)

if __name__ == '__main__':
    initialize_game()
    app.run(debug=True)
