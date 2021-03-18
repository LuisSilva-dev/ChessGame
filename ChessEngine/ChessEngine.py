class Board:
    def __init__(self, p):
        self.width = 800
        self.sqWidth = 100
        self.height = 600;
        self.sqHeight = 75
        self.board = [
           [Rook(False), Peon(False), "", "", "", "", Peon(True), Rook(True)],
           [Khight(False), Peon(False), "", "", "", "", Peon(True), Khight(True)],
           [Bishop(False), Peon(False), "", "", "", "", Peon(True), Bishop(True)],
           [Queen(False), Peon(False), "", "", "", "", Peon(True), Queen(True)],
           [King(False), Peon(False), "", "", "", "", Peon(True), King(True)],
           [Bishop(False), Peon(False), "", "", "", "", Peon(True), Bishop(True)],
           [Khight(False), Peon(False), "", "", "", "", Peon(True), Khight(True)],
           [Rook(False), Peon(False), "", "", "", "", Peon(True), Rook(True)]
        ]
        self.p = p
        self.screen = p.display.set_mode((self.width, self.height))
        self.whiteTurn = True
    def switchTurn(self):
        self.whiteTurn = not self.whiteTurn
    def drawBoard(self):
        white = (255, 255, 255)
        for i in range(8):
            for j in range(4):
                if i % 2 == 0:
                    rect = self.p.Rect((self.sqWidth * 2 * j, i * self.height / 8), (self.sqWidth, self.sqHeight))
                else:
                    rect = self.p.Rect((self.sqWidth * 2 * (j + (1 / 2)), i * self.sqHeight), (self.sqWidth, self.sqHeight))
                self.p.draw.rect(self.screen, white, rect, 0)
                
    def drawPieces(self):
        majorPieces = ["wR.png", "wC.png", "wB.png", "wQ.png", "wK.png", "wB.png", "wC.png", "wR.png"]
        majorPiecesBlack = ["pR.png", "pC.png", "pB.png", "pQ.png", "pK.png", "pB.png", "pC.png", "pR.png"]
        i = 0
        for piece, blackPiece in zip(majorPieces, majorPiecesBlack):
            self.screen.blit( self.p.image.load(piece), (self.sqWidth * i + 15, self.sqHeight * 7))
            self.screen.blit( self.p.image.load(blackPiece), (self.sqWidth * i + 15, 0))
            i += 1
        for j in range(8):
            self.screen.blit(self.p.image.load("wP.png"), (self.sqWidth * j + 23, self.sqHeight * 6))
            self.screen.blit(self.p.image.load("pP.png"), (self.sqWidth * j + 23, self.sqHeight))

class Piece:
    def __init__(self, isWhite):
        self.isWhite = isWhite
    def checkCollisionsSide(self, originPosX, originPosY, destPosX, destPosY, board):
        if originPosX == destPosX:
            for i in range(1, abs(destPosY - originPosY)):
                if destPosY - originPosY > 0:
                    check = isinstance(board[originPosX][originPosY + i], Piece)
                else:
                    check = isinstance(board[originPosX][originPosY - i], Piece)
                if check:
                    return False
        else:
            for i in range(1, abs(destPosX - originPosX)):
                if destPosX - originPosX > 0:
                    check = isinstance(board[originPosX + i][originPosY], Piece)
                else:
                    check = isinstance(board[originPosX - i][originPosY], Piece)
                if check:
                    return False
        return True
    
    def checkCollisionsDiagonal(self, originPosX, originPosY, destPosX, destPosY, board):
        for i in range(1, abs(originPosX - destPosX)):
            if destPosX - originPosX > 0:
                if destPosY - originPosY > 0:
                    check = isinstance(board[originPosX + i][originPosY + i], Piece)
                else:
                    check = isinstance(board[originPosX + i][originPosY - i], Piece)
            else:
                if destPosY - originPosY > 0:
                    check = isinstance(board[originPosX - i][originPosY + i], Piece)
                else:
                    check = isinstance(board[originPosX - i][originPosY - i], Piece)
            if check:
                return False
        return True
    def move(self):
        return True
    
class Peon(Piece):
    def __init__(self, isWhite):
        self.firstMove = True
        self.isWhite = isWhite
      
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        if originPosY + 1 == len(board):
            return False
        if self.isWhite:
            color = "wP.png"
            check = (isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite and ((originPosX - 1, originPosY - 1) == destPos or (originPosX + 1, originPosY - 1) == destPos)) or (isinstance(board[originPosX][originPosY - 1], Piece) == False and ((destPos == (originPosX, originPosY - 1) or (destPos == (originPosX, originPosY - 2) and isinstance(board[originPosX][originPosY - 2], Piece) == False and self.firstMove))))
        else:
            color = "pP.png"
            check = (isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite and ((originPosX - 1, originPosY + 1) == destPos or (originPosX + 1, originPosY + 1) == destPos)) or (isinstance(board[originPosX][originPosY + 1], Piece) == False and ((destPos == (originPosX, originPosY + 1) or (destPos == (originPosX, originPosY + 2) and isinstance(board[originPosX][originPosY + 2], Piece) == False and self.firstMove))))
        if check:
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 23, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        if self.firstMove:
            self.firstMove = False
        return True
    
class King(Piece):
    def __init__(self, isWhite):
        self.checked = False
        self.isWhite = isWhite
        self.canCastle = True
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        if self.isWhite:
            color = "wK.png"
        else:
            color = "pK.png"
        if self.canCastle and abs(originPosX - destPosX) == 2:
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
        if (isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite or not isinstance(board[destPosX][destPosY], Piece)) and (abs(originPosX - destPosX) <= 1 and abs(originPosY - destPosY) <= 1):
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 15, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        if self.canCastle:
            self.canCastle = False
        return True
    
class Queen(Piece):
    def __init__(self, isWhite):
        self.checked = False
        self.isWhite = isWhite
    
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        print(originPosX - destPosX)
        print(originPosY - destPosY)
        if self.isWhite:
            color = "wQ.png"
        else:
            color = "pQ.png"   
        if ((isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite) or not isinstance(board[destPosX][destPosY], Piece)) and ((abs(originPosX - destPosX) == abs(originPosY - destPosY) and self.checkCollisionsDiagonal(originPosX, originPosY, destPosX, destPosY, board)) or (((destPosY == originPosY and not destPosX == originPosX) or (not destPosY == originPosY and destPosX == originPosX)) and self.checkCollisionsSide(originPosX, originPosY, destPosX, destPosY, board))):
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 15, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        return True
class Khight(Piece):
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        if self.isWhite:
            color = "wC.png"
        else:
            color = "pC.png"
        if ((isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite) or not isinstance(board[destPosX][destPosY], Piece)) and ((abs(originPosX - destPosX) == 1 and abs(originPosY - destPosY) == 2) or (abs(originPosX - destPosX) == 2 and abs(originPosY - destPosY) == 1)):
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 15, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        return True
class Bishop(Piece):
    def __init__(self, isWhite):
        self.checked = False
        self.isWhite = isWhite
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        print(originPosX - destPosX)
        print(originPosY - destPosY)
        if self.isWhite:
            color = "wB.png"
        else:
            color = "pB.png"
        if ((isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite) or not isinstance(board[destPosX][destPosY], Piece)) and (abs(originPosX - destPosX) == abs(originPosY - destPosY) and self.checkCollisionsDiagonal(originPosX, originPosY, destPosX, destPosY, board)):
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 15, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        return True
class Rook(Piece):
    def __init__(self, isWhite):
        self.canCastle = True
        self.isWhite = isWhite
    def move(self, originPos, destPos, boardObject):
        destPosX = int(destPos[0] / boardObject.sqWidth)
        destPosY = int(destPos[1] / boardObject.sqHeight)
        originPosX = int(originPos[0] / boardObject.sqWidth)
        originPosY = int(originPos[1] / boardObject.sqHeight)
        destPos = (destPosX, destPosY)
        board = boardObject.board
        if self.isWhite:
            color = "wR.png"
        else:
            color = "pR.png"
        if ((isinstance(board[destPosX][destPosY], Piece) and not board[destPosX][destPosY].isWhite == board[originPosX][originPosY].isWhite) or not isinstance(board[destPosX][destPosY], Piece)) and (((destPosY == originPosY and not destPosX == originPosX) or (not destPosY == originPosY and destPosX == originPosX)) and self.checkCollisionsSide(originPosX, originPosY, destPosX, destPosY, board)):
            board[destPosX][destPosY] = self
            board[originPosX][originPosY] = ""
            rect = boardObject.p.Rect((boardObject.sqWidth * destPosX, destPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((destPosX * boardObject.sqWidth, destPosY * boardObject.sqHeight)), rect)
            boardObject.screen.blit(boardObject.p.image.load(color), (boardObject.sqWidth * destPosX + 15, boardObject.sqHeight * destPosY))
            rect = boardObject.p.Rect((boardObject.sqWidth * originPosX, originPosY * boardObject.sqHeight), (boardObject.sqWidth, boardObject.sqHeight))
            boardObject.p.draw.rect(boardObject.screen, boardObject.screen.get_at((originPosX * boardObject.sqWidth, originPosY * boardObject.sqHeight)), rect)
            boardObject.p.display.update()
        else:
            return False
        return True