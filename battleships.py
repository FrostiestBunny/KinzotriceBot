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

    def insert(self, ship, pos_x, pos_y, dr, ch="S"):

        pos_y = self.y_coords.index(pos_y.upper())+1

        if pos_x > len(self.grid)-1 or pos_x < 1 or pos_y > len(self.grid)-1 or pos_y < 1:
            return False

        for s in range(ship.size):
            if dr == "north":
                if pos_y-s < 1 or self.grid[pos_y-s][pos_x] == "S":
                    return False
                self.grid[pos_y-s][pos_x] = ch
            elif dr == "south":
                if pos_y+s > len(self.grid)-1 or self.grid[pos_y+s][pos_x] == "S":
                    return False
                self.grid[pos_y+s][pos_x] = ch
            elif dr == "east":
                if pos_x+s > len(self.grid[1])-1 or self.grid[pos_y][pos_x+s] == "S":
                    return False
                self.grid[pos_y][pos_x+s] = ch
            else:
                if pos_x-s < 1 or self.grid[pos_y][pos_x-s] == "S":
                    return False
                self.grid[pos_y][pos_x-s] = ch

        return True

    def hit(self, x, y):

        if self.grid[y][x] == "S":
            self.grid[y][x] = "X"
            return True

        return False

class Ship:

    def __init__(self, name, size=1):
        self.name = name
        self.size = size

    def __str__(self):
        return self.name
