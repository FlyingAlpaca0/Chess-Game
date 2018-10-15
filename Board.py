class Board:
    def __init__(self, sidelength):
        self.sidelength = sidelength
        self.matrix = [['0'] * sidelength for i in range(sidelength)]

    def display(self):
        for i in reversed(range(self.sidelength)):
            for j in range(self.sidelength):
                print(self.matrix[j][i], end=' ')
            print()
                
