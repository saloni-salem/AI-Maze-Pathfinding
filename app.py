from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

ROWS = 8
COLS = 8

def h(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):

    open_list = []
    heapq.heappush(open_list, (0, start))

    came = {}
    g = {start: 0}

    while open_list:

        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came:
                path.append(current)
                current = came[current]
            path.reverse()
            return path

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx = current[0] + dx
            ny = current[1] + dy

            if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] == 0:

                new_g = g[current] + 1

                if (nx, ny) not in g or new_g < g[(nx, ny)]:
                    g[(nx, ny)] = new_g
                    f = new_g + h((nx, ny), goal)
                    heapq.heappush(open_list, (f, (nx, ny)))
                    came[(nx, ny)] = current

    return []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/find_path", methods=["POST"])
def find_path():

    data = request.json
    grid = data["grid"]
    start = tuple(data["start"])
    goal = tuple(data["goal"])

    path = astar(grid, start, goal)

    return jsonify({"path": path})


if __name__ == "__main__":
    app.run(debug=True)