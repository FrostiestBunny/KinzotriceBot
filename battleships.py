class Grid:

    y_coords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    x_coords = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    def __init__(self, width=10, height=10):
        self.grid = [self.x_coords]
        for y in range(height):
            row = []
            for x in range(width):
                row.append('0')
            self.grid.append(row)
        for i, l in enumerate(self.y_coords):
            self.grid[i+1].insert(0, l)

    def __str__(self):
        result = ""
        for y in self.grid:
            row = "   ".join(y)
            result += row + "\n\n"
        return result
