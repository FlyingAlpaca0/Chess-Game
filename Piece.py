

class Piece:

    def __init__(self, color):
        self.color = color
        self.char = None
        self.first = True

    def move(self, target):
        self.x = target[0]
        self.y = target[1]

    def isValid(self, target, occupied):
        reachableSquares = self.reachable(occupied)
        if target in path:
            return True
        return False

class Pawn(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'p'
        self.first = True

    def pathGen(self, target, pos, kill):
        path = []
        if self.color:
            i = 1
        else:
            i = -1
        if kill:
            if 0 <= pos[0] + 1 < 8 and 0 <= pos[1] + i < 8:
                if (pos[0] + 1, pos[1] + i) == target:
                    path.append((pos[0] + 1, pos[1] + i))
                    return path
            if 0 <= pos[0] - 1 < 8 and 0 <= pos[1] + i < 8:
                if (pos[0] - 1, pos[1] + i) == target:
                    path.append((pos[0] - 1, pos[1] + i))
                    return path
        else:
            if 0 <= pos[1] + i < 8:
                path.append((pos[0], pos[1] + i))
                if path[-1] == target:
                    return path            
                if self.first:
                    path.append((pos[0], pos[1] + 2*i))
                    if path[-1] == target:
                        self.justDoublePushed = True
                        return path
        return []
        

class King(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'K'

    def pathGen(self, target, pos, kill):
        path = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if  (0 <= pos[0] + i < 8 and
                    0 <= pos[1] + j < 8 and
                    (pos[0] + i, pos[1] + j) == target):
                    path.append((pos[0] + i, pos[1] + j))
        return path
        

class Queen(Piece):

    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'Q'

    def pathGen(self, target, pos, kill):
        return (Bishop.pathGen(self, target, pos, kill) +
                Rook.pathGen(self, target, pos, kill))

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'B'

    def pathGen(self, target, pos, kill):
        path = []
        k = 1
        while(pos[0] + k < 8 and pos[1] + k < 8):
            path.append((pos[0] + k, pos[1] + k))
            if (pos[0] + k, pos[1] + k) == target:
                return path
            k += 1
        path = []
        k = 1
        while(pos[0] - k >= 0 and pos[1] - k >= 0):
            path.append((pos[0] - k, pos[1] - k))
            if (pos[0] - k, pos[1] - k) == target:
                return path
            k += 1
        path = []
        k = 1
        while(pos[0] + k < 8 and pos[1] - k >= 0):
            path.append((pos[0] + k, pos[1] - k))
            if (pos[0] + k, pos[1] - k) == target:
                return path
            k += 1
        path = []
        k = 1
        while(pos[0] - k >= 0 and pos[1] + k < 8):
            path.append((pos[0] - k, pos[1] + k))
            if (pos[0] - k, pos[1] + k) == target:
                return path
            k += 1

        return []

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'R'

    def pathGen(self, target, pos, kill):
        path = []
        k = 1
        while(pos[0] + k < 8):
            path.append((pos[0] + k, pos[1]))
            if (pos[0] + k, pos[1]) == target:
                return path
            k += 1
        k = 1
        path = []
        while(pos[0] - k >= 0):
            path.append((pos[0] - k, pos[1]))
            if (pos[0] - k, pos[1]) == target:
                return path
            k += 1
        k = 1
        path = []
        while(pos[1] + k < 8):
            path.append((pos[0], pos[1] + k))
            if (pos[0], pos[1] + k) == target:
                return path
            k += 1
        k = 1
        path = []
        while(pos[1] - k >= 0):
            path.append((pos[0], pos[1] - k))
            if (pos[0], pos[1] - k) == target:
                return path
            k += 1
        return []

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
        self.char = 'N'

    def pathGen(self, target, pos, kill):
        path = []
        for i in [-2, 2]:
            for j in [-1, 1]:
                if ((pos[0] + i, pos[1] + j) == target and
                    0 <= pos[0] + i < 8 and
                    0 <= pos[1] + j < 8):
                    path.append((pos[0] + i, pos[1] + j))
                    return path
        for j in [-2, 2]:
            for i in [-1, 1]:
                if ((pos[0] + i, pos[1] + j) == target and
                    0 <= pos[0] + i < 8 and
                    0 <= pos[1] + j < 8):
                    path.append((pos[0] + i, pos[1] + j))
                    return path
                    
        return []
                    
            
            
            
            
        

    
