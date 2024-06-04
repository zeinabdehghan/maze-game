import random
def generate_maze(size,xg, yg, xs, ys ):
    random1 = input("do you want your maze random? (y/n)")
    maze = []

    if random1 == 'n':
        print("Enter the matrix values (each row separated by a space):")
        for _ in range(size):
            row_input = input().strip()
            values = list(map(int, row_input.split()[:size]))
            maze.append(values)

    elif random1 == 'y':
        maze = [[random.choice([0, 1]) for _ in range(size)] for _ in range(size)]

    else:
        print("Invalid input. Exiting.")
        exit(1)

    if 0 <= xs < size and 0 <= ys < size and 0 <= xg < size and 0 <= yg < size:
        maze[xs][ys] = 0  # Start cell
        maze[xg][yg] = 0  # Goal cell
    else:
        print("Invalid start or goal coordinates. Exiting.")
        exit(1)
    return maze

def print_maze(maze,xg,yg):
    visual_maze = [row[:] for row in maze]
    visual_maze[xg][yg] = 'G'

    for row in visual_maze:
        print(" ".join(map(str, row)))

def local_beam_search(maze,xg, yg, xs, ys ,beam_width=2, max_iterations=1000):
    size = len(maze)
    start = (xs, ys)
    goal = (xg, yg)

    def get_neighbors(cell):
        x, y = cell
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0]

    def heuristic(cell):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def evaluate_paths(paths):
        return sorted(paths, key=lambda path: heuristic(path[-1]))

    paths = [[start]]
    for _ in range(max_iterations):
        new_paths = []
        for path in paths:
            current_cell = path[-1]
            neighbors = get_neighbors(current_cell)
            for neighbor in neighbors:
                new_path = path + [neighbor]
                if neighbor == goal:
                    return new_path
                new_paths.append(new_path)

        paths = evaluate_paths(new_paths)[:beam_width]

    return None

def lrta_star(maze, xg, yg, xs, ys, max_iterations=1000):
    size = len(maze)
    start = (xs, ys)
    goal = (xg, yg)

    def get_neighbors(cell):
        x, y = cell
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0]

    def heuristic(cell):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def cost(current, next_cell):
        return 1  # Cost of moving

    def update_cost_to_go(cell):
        return heuristic(cell)

    def lrta_star_iteration(path, h_values):
        current_cell = path[-1]
        neighbors = get_neighbors(current_cell)

        if not neighbors:
            return None

        min_h_value = float('inf')
        best_neighbor = None

        for neighbor in neighbors:
            if h_values[neighbor] < min_h_value:
                min_h_value = h_values[neighbor]
                best_neighbor = neighbor

        return best_neighbor

    h_values = {(i, j): heuristic((i, j)) for i in range(size) for j in range(size)}
    path = [start]

    for _ in range(max_iterations):
        current_cell = path[-1]

        if current_cell == goal:
            return path

        next_cell = lrta_star_iteration(path, h_values)

        if next_cell is None:
            break

        path.append(next_cell)
        h_values[next_cell] = update_cost_to_go(next_cell)

    return None


input_start = input("Enter the row and column of the start cell (x y): ")
xs, ys = map(int, input_start.split())
input_goal = input("Enter the row and column of the goal cell (x y): ")
xg, yg = map(int, input_goal.split())

maze_size = 5
maze = generate_maze(maze_size, xg, yg, xs, ys)

print("Generated Maze:")
print_maze(maze, xg, yg)


path = local_beam_search(maze, xg, yg, xs, ys)

if path:
    print("\nLocal beam: path found:")
    for step, cell in enumerate(path):
        print(f"Step {step + 1}: {cell}")
else:
    print("\nthere is no path with local beam.")



lrta_star_path = lrta_star(maze, xg, yg, xs, ys)

if lrta_star_path:
    print("\nLRTA*: path found:")
    for step, cell in enumerate(lrta_star_path):
        print(f"Step {step + 1}: {cell}")
else:
    print("\nthere is no path with LRTA*.")