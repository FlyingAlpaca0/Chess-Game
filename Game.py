#Type the chess notation for the location of the piece you want to move followed by the destination with no spaces
#For example to start with King's pawn to e4, give your input as e2e4
#The reason for this is that regular chess notation is insufficient here as it requires some level of human judgement
#The type of inout notation used here can be expanded to a drag and drop type of input if a GUI is added to this game

import Piece

class Game:
    def __init__(self):
        self.board = [[None]*8 for i in range(8)]
        for i in range(8):
            self.board[i][1] = Piece.Pawn(True)
            self.board[i][6] = Piece.Pawn(False)
        self.board[4][0] = Piece.King(True)
        self.board[0][0] = Piece.Rook(True)
        self.board[7][0] = Piece.Rook(True)
        self.board[2][0] = Piece.Bishop(True)
        self.board[5][0] = Piece.Bishop(True)
        self.board[1][0] = Piece.Knight(True)
        self.board[6][0] = Piece.Knight(True)
        self.board[3][0] = Piece.Queen(True)
        self.board[4][7] = Piece.King(False)
        self.board[0][7] = Piece.Rook(False)
        self.board[7][7] = Piece.Rook(False)
        self.board[2][7] = Piece.Bishop(False)
        self.board[5][7] = Piece.Bishop(False)
        self.board[1][7] = Piece.Knight(False)
        self.board[6][7] = Piece.Knight(False)
        self.board[3][7] = Piece.Queen(False)
        
        self.king_pos = {}
        self.king_pos[True] = (4, 0)
        self.king_pos[False] = (4, 7)

        self.checkmate = False
 

    def display(self):
        for i in reversed(range(8)):
            for j in range(8):
                if self.board[j][i] == None:
                    print('0' , end=' ')
                else:
                    print(self.board[j][i].char , end=' ')
            print()

    def threatened(self, position, side):
        for i in reversed(range(8)):
            for j in range(8):
                if self.board[j][i] == None or self.board[j][i].color == side:
                    continue
                threatPath = self.board[j][i].pathGen(
                    position, (j, i), True)
                if len(threatPath) == 0:
                    continue
                for k in range(len(threatPath) - 1):
                    if self.board[threatPath[k][0]][threatPath[k][1]] != None:
                        return False
                return True

    def parse(self, move_string):
        target = (ord(move_string[-2]) - ord('a'), int(move_string[-1]) - 1)
        pos = (ord(move_string[0]) - ord('a'), int(move_string[1]) - 1)
        return [target, pos]

    def validate(self, pos, target, turn):
        if (self.board[pos[0]][pos[1]] == None or
            self.board[pos[0]][pos[1]].color != turn):
            return False
        if self.board[target[0]][target[1]] != None:
            if self.board[target[0]][target[1]].color == turn:
                return False           
            kill = (self.board[target[0]][target[1]].color != turn)
        else:
            kill = False
        
        path = self.board[pos[0]][pos[1]].pathGen(target, pos, kill)
        if len(path) == 0:
            return False
        for i in range(len(path) - 1):
            if self.board[path[i][0]][path[i][1]] != None:
                return False
        return True

    def move(self, pos, target):
        self.board[target[0]][target[1]] = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = None

    def checkcheck(self, turn):
        if self.threatened(self.king_pos[not turn], not turn):
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    if  (0 <= self.king_pos[not turn][0] + i < 8 and
                        0 <= self.king_pos[not turn][1] + j < 8):
                        isKingMoveValid = self.validate(self.king_pos[not turn],
                            (self.king_pos[not turn][0] + i,self.king_pos[not turn][1] + j),
                             not turn)
                        if isKingMoveValid:
                            if not self.threatened(
                            (self.king_pos[not turn][0] + i,
                             self.king_pos[not turn][1] + j), not turn):
                                print("Check!!!")
                                return
            self.checkmate = True
            return

    def checkcastle(self, turn, target):
        if target[1]!= self.king_pos[turn][1]:
            return False
        for i in [-2, 2]:
            if target[0] != self.king_pos[turn][0] + i:
                break
        else:
            return False
        if target[0] < self.king_pos[turn][0]:
            if self.board[0][target[1]].char != 'R':
                return False
            for i in range(self.king_pos[turn][0], -1):
                if self.threatened((i, target[1]), turn):
                    return False
            self.move(self.king_pos[turn], target)
            self.move((0, target[1]), (target[0] + 1, target[1]))
            self.board[target[0]][target[1]].first = False
            self.board[target[0] + 1][target[1]].first = False
            return True
        else:
            if self.board[7][target[1]].char != 'R':
                return False
            for i in range(self.king_pos[turn][0], -1):
                if self.threatened((i, target[1]), turn):
                    return False
            self.move(self.king_pos[turn], target)
            self.move((7, target[1]), (target[0] - 1, target[1]))
            self.board[target[0]][target[1]].first = False
            self.board[target[0] - 1][target[1]].first = False
            return True
        return False
        
    def enPassant(self, pos, target, side):
        enPassantPath = self.board[pos[0]][pos[1]].pathGen(target, pos, True)
        if len(enPassantPath) == 0:
            return False
        if (self.board[target[0]][pos[1]] != None and
            self.board[target[0]][pos[1]].char == 'p' and
            self.board[target[0]][pos[1]].justDoublePushed and
            not self.board[target[0]][pos[1]]. first):
            self.board[target[0]][pos[1]].justDoublePushed = False
            self.board[target[0]][pos[1]] = None
            self.move(pos, target)
            return True
        return False

    def playOneTurn(self, move_string, turn):
        parsedString = self.parse(move_string)
        target = parsedString[0]
        pos = parsedString[1]
        if (pos == self.king_pos[turn] and self.board[pos[0]][pos[1]].first):
            if self.checkcastle(turn, target):
                self.king_pos[turn] = target
                return True
            print('invalid move!!!')
            return False
        for i in range(8):
            for j in range(8):
                if (self.board[i][j] != None and
                    self.board[i][j].char == 'p' and
                    self.board[i][j].color == turn):
                    self.board[i][j].justDoublePushed = False
        if not self.validate(pos, target, turn):
            if (self.board[pos[0]][pos[1]] != None and
                self.board[pos[0]][pos[1]].char == 'p'):
                if self.enPassant(pos, target, turn):
                    return True
            print('invalid move!!!')
            return False
        self.move(pos, target)
        if self.board[target[0]][target[1]].char == 'K':
            self.king_pos[turn] = target
        if self.threatened(self.king_pos[turn], turn):
            print("illegal move!!!")
            self.move(target, pos)
            return False
        if self.board[target[0]][target[1]].char == 'p' and (target[1] == 0 or target[1] == 7):
            self.board[target[0]][target[1]] = Piece.Queen(turn)
        self.checkcheck(turn)
        if self.board[target[0]][target[1]].first:
            self.board[target[0]][target[1]].first = False
        return True

    def play(self):
        self.display()
        turn = True
        while(True):
            move_string = input()
            if move_string == 'q':
                return
            if not self.playOneTurn(move_string, turn):
                continue
            if self.checkmate:
                self.display()
                print("Checkmate!", 'White' if turn else 'Black', "Wins!!")
                return
            turn = not turn
            print()
            self.display()

if __name__ == "__main__":
    g = Game()
    g.play()
        
