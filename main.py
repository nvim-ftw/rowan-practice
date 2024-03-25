def index_grid(xy, grid):
    x, y = xy
    return grid[y][x]

def index_alter_grid(xy, grid, new_value):
    x, y = xy
    grid[y][x] = new_value
    return grid

def within_grid(xy, wh):
    x, y = xy
    w, h = wh
    return 0 <= x < w and 0 <= y < h


def move(xy, direction):
    x, y = xy
    dx, dy = direction_dict[direction]
    return (x + dx, y + dy)


direction_dict = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
        }

"""
Fields of the data:

int width
int height
int[][] grid
(int, int) start
int strength
int agility
int steps_to_perform
char[] directions
"""
class Dataset:
    def __init__(self, width, height, grid, start, strength, agility, steps_to_perform, directions):
        self.width = width
        self.height = height
        self.grid = grid
        self.start = start
        self.strength = strength
        self.agility = agility
        self.steps_to_perform = steps_to_perform
        self.directions = directions

    def simulate(self):
        if not within_grid(self.start, (self.width, self.height)):
            print("Robot is off the grid.")
            return

        if index_grid(self.start, self.grid) == 0:
            print("Robot is in a hole")
            return

        for i in range(self.steps_to_perform):
            direction = self.directions[i]
            try:
                value = index_grid(move(self.start, direction), self.grid)
            except IndexError:
                print("Instruction {} unsafe: {} at {} {}", i + 1, direction, self.start)
                return
            if value > 0:
                if self.strength > value:
                    self.start = move(self.start, direction)
                elif self.strength == value:
                    self.grid = index_alter_grid(move(self.start, direction), self.grid, 0)
                    self.start = move(self.start, direction)
                else:
                    # do nothing
                    pass
            elif value == 0:
                self.start = move(self.start, direction)
            else:
                if self.agility >= abs(value):
                    self.start = move(self.start, direction)
                else:
                    # do nothing
                    pass

        print("{} Instructions processed; robot at {} {}", self.steps_to_perform, self.start[0], self.start[1])


# returns a list of `Dataset` objects
def parse_data(filepath):
    with open(filepath, "r") as file:
        data = file.readlines()
    dataset_count = int(data.pop(0).strip())
    datasets = []

    for i in range(dataset_count):
        width, height = map(int, data.pop(0).strip().split())
        grid = []
        for j in range(height):
            line_list = [int(x) for x in data.pop(0).strip().split()]
            grid.append(line_list)

        start_pos_list = [int(x) for x in data.pop(0).strip().split()]
        start_pos = (start_pos_list[0], start_pos_list[1])
        strength, agility = map(int, data.pop(0).strip().split())
        steps_to_perform = int(data.pop(0).strip())
        directions = data.pop(0).strip().split()
        dataset = Dataset(width, height, grid, start_pos, strength, agility, steps_to_perform, directions)
        datasets.append(dataset)

    return datasets

filepath = input("What is the file path? ").strip()
data = parse_data(filepath)
for i, dataset in enumerate(data):
    print("Data Set {}", i + 1)
    print("Robot Start: {} {}", dataset.start[0], dataset.start[1])
    print("Robot Strength and Agility: {} {}", dataset.strength, dataset.agility)
    print("Instructions: {}", dataset.steps_to_perform)
    dataset.simulate()

    print("Table configuration:")


def print_grid(grid):
    for row in grid:
        print(" ".join([str(x) for x in row]))

    print("\n\n")



