// main.js

const SIZE = 10;

function renderBoard(board, flags, revealed, gameOver) {
    const boardDiv = document.getElementById('board');
    boardDiv.innerHTML = '';
    for (let i = 0; i < SIZE; i++) {
        for (let j = 0; j < SIZE; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.x = i;
            cell.dataset.y = j;

            if (revealed[i][j] || gameOver) {
                if (board[i][j] === -1) {
                    cell.classList.add(gameOver ? 'mine-clicked' : 'mine');
                    cell.innerText = gameOver ? '💣' : '';
                } else {
                    cell.classList.add('revealed');
                    cell.innerText = board[i][j] === 0 ? '' : board[i][j];
                }
            } else {
                if (flags[i][j]) {
                    cell.classList.add('flag');
                    cell.innerText = 'F';
                }
            }

            cell.addEventListener('click', () => clickCell(i, j));
            cell.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                placeFlag(i, j);
            });
            boardDiv.appendChild(cell);
        }
    }
}

function reveal_empty_cells(x, y) {
    let stack = [{x: x, y: y}];
    while (stack.length > 0) {
        let cell = stack.pop();
        let cx = cell.x;
        let cy = cell.y;
        if (!revealed[cx][cy]) {
            revealed[cx][cy] = true;
            if (board[cx][cy] === 0) {
                for (let nx = Math.max(0, cx - 1); nx <= Math.min(SIZE - 1, cx + 1); nx++) {
                    for (let ny = Math.max(0, cy - 1); ny <= Math.min(SIZE - 1, cy + 1); ny++) {
                        stack.push({x: nx, y: ny});
                    }
                }
            }
        }
    }
}

function newGame() {
    $.post('/new_game', (data) => {
        renderBoard(data.board, data.flags, data.revealed, false);
        document.getElementById('turn').innerText = data.turn;
    });
}

function clickCell(x, y) {
    $.ajax({
        url: '/click_cell',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ x, y }),
        success: (data) => {
            renderBoard(data.board, data.flags, data.revealed, data.turn === 'Game Over');
            document.getElementById('turn').innerText = data.turn;
            if (data.winner) {
                alert(`Người chơi ${data.winner} đã dẫm phải mìn!`);
            }
        }
    });
}


function placeFlag(x, y) {
    $.ajax({
        url: '/place_flag',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ x, y }),
        success: (data) => {
            renderBoard(data.board, data.flags, data.revealed, false);
            document.getElementById('turn').innerText = data.turn;
        }
    });
}

$(document).ready(() => {
    newGame();
});
