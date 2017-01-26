class Grid:

    y_coords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    x_coords = ["", " 1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    def __init__(self, width=10, height=10, cell_fill="0"):
        self.grid = [self.x_coords]
        for y in range(height):
            row = []
            for x in range(width):
                row.append(cell_fill)
            self.grid.append(row)
        for i, l in enumerate(self.y_coords):
            self.grid[i+1].insert(0, l)

    def __str__(self):
        result = ""
        for y in self.grid:
            row = "   ".join(y)
            result += row + "\n\n"
        return result

    def insert(self, ship, pos_x, pos_y):

        if pos_x > len(self.grid)-1 or pos_x < 1 or pos_y > len(self.grid)-1 or pos_y < 1:
            return False

        self.grid[pos_y][pos_x] = "S"
        for s in range(ship.size):
            if ship.direction == "north":
                if pos_y-s < 1:
                    print("Wrong y buddy.")
                    return False
                self.grid[pos_y-s][pos_x] = "S"
            elif ship.direction == "south":
                if pos_y+s > len(self.grid)-1:
                    print("Wrong y buddy.")
                    return False
                self.grid[pos_y+s][pos_x] = "S"
            elif ship.direction == "east":
                if pos_x+s > len(self.grid[1])-1:
                    print("Wrong x buddy.")
                    return False
                self.grid[pos_y][pos_x+s] = "S"
            else:
                if pos_x-s < 1:
                    print("Wrong x buddy.")
                    return False
                self.grid[pos_y][pos_x-s] = "S"

        return True

class Ship:

    def __init__(self, size=1, dr="north"):
        self.direction = dr
        self.size = size
