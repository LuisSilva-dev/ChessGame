import pygame as p
from ChessEngine import ChessEngine
from pygame.constants import MOUSEBUTTONDOWN
p.init()
boardObject = ChessEngine.Board(p)
board = boardObject.board
boardObject.drawBoard()
boardObject.drawPieces()
p.display.update()
running = True
position = (-1, -1)
piece = (-1, -1)
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            position = p.mouse.get_pos()
            piece = board[int(position[0] / boardObject.sqWidth)][int(position[1] / boardObject.sqHeight)]
            if(not boardObject.whiteTurn and piece.isWhite):
                piece = (-1, -1)
            elif(boardObject.whiteTurn and not piece.isWhite):
                piece = (-1, -1)
        if event.type == p.MOUSEBUTTONUP:
            if not piece == (-1, -1):
                nextPos = p.mouse.get_pos()
                if piece.move(position, nextPos, boardObject):
                    boardObject.switchTurn()
                