import pygame as p
import ChessEngine
from aibot import get_best_move

# ================= CONFIG =================
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 300
WIDTH = BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH
HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

AI_ENABLED = True


def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"),
            (SQ_SIZE, SQ_SIZE)
        )


def main():
    global AI_ENABLED

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    loadImages()

    font = p.font.SysFont("Arial", 18)
    bigFont = p.font.SysFont("Arial", 36)

    state = "MENU"
    selected_time = 300
    selected_diff = "Medium"

    gs = None
    validMoves = []

    sqSelected = ()
    playerClicks = []
    moveMade = False
    gameOver = False

    whiteTime = 300
    blackTime = 300

    running = True

    # 🔥 AI BUTTON (GAME SCREEN)
    ai_btn = p.Rect(BOARD_WIDTH + 20, 380, 240, 45)

    while running:
        dt = clock.tick(MAX_FPS) / 1000

        # ================= MENU =================
        if state == "MENU":
            screen.fill((20, 20, 20))

            title = bigFont.render("CHESS GAME", True, p.Color("white"))
            screen.blit(title, (WIDTH//2 - 130, 40))

            # Timer buttons
            times = [60, 300, 600]
            labels = ["1 min", "5 min", "10 min"]

            for i, t in enumerate(times):
                rect = p.Rect(200 + i*120, 150, 100, 50)
                color = p.Color("gold") if selected_time == t else p.Color("gray")
                p.draw.rect(screen, color, rect, border_radius=8)
                txt = font.render(labels[i], True, p.Color("black"))
                screen.blit(txt, (rect.x + 10, rect.y + 12))

                if p.mouse.get_pressed()[0] and rect.collidepoint(p.mouse.get_pos()):
                    selected_time = t

            # Difficulty
            diffs = ["Easy", "Medium", "Hard"]
            for i, d in enumerate(diffs):
                rect = p.Rect(200 + i*120, 250, 100, 50)
                color = p.Color("green") if selected_diff == d else p.Color("gray")
                p.draw.rect(screen, color, rect, border_radius=8)
                txt = font.render(d, True, p.Color("black"))
                screen.blit(txt, (rect.x + 10, rect.y + 12))

                if p.mouse.get_pressed()[0] and rect.collidepoint(p.mouse.get_pos()):
                    selected_diff = d

            # Start button
            start_btn = p.Rect(WIDTH//2 - 100, 350, 200, 60)
            p.draw.rect(screen, p.Color("#2962ff"), start_btn, border_radius=10)
            txt = font.render("START GAME", True, p.Color("white"))
            screen.blit(txt, (start_btn.x + 35, start_btn.y + 18))

            if p.mouse.get_pressed()[0] and start_btn.collidepoint(p.mouse.get_pos()):
                gs = ChessEngine.GameState()
                validMoves = gs.getValidMove()
                whiteTime = selected_time
                blackTime = selected_time
                state = "GAME"

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

        # ================= GAME =================
        elif state == "GAME":

            # Timer logic
            if not gameOver:
                if gs.whiteToMove:
                    whiteTime -= dt
                else:
                    blackTime -= dt

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()

                    # 🔥 AI TOGGLE CLICK
                    if ai_btn.collidepoint(location):
                        AI_ENABLED = not AI_ENABLED

                    if location[0] <= BOARD_WIDTH:
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE

                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                            for validMove in validMoves:
                                if move == validMove:
                                    gs.makeMove(validMove)
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                                    break

                            if not moveMade:
                                playerClicks = [sqSelected]

            # After player move
            if moveMade:
                validMoves = gs.getValidMove()
                moveMade = False

            # 🤖 AI (UNCHANGED)
            if AI_ENABLED and not gameOver:
                if not gs.whiteToMove:
                    p.time.delay(300)

                    fen = gs.getFEN()
                    ai_move = get_best_move(fen)

                    if ai_move:
                        startCol = ord(ai_move[0]) - ord('a')
                        startRow = 8 - int(ai_move[1])
                        endCol = ord(ai_move[2]) - ord('a')
                        endRow = 8 - int(ai_move[3])

                        validMoves = gs.getValidMove()

                        for move in validMoves:
                            if (move.startRow == startRow and
                                move.startCol == startCol and
                                move.endRow == endRow and
                                move.endCol == endCol):

                                gs.makeMove(move)
                                validMoves = gs.getValidMove()
                                break

            # ================= UI =================
            screen.fill(p.Color(18,18,18))

            drawBoard(screen)
            drawPieces(screen, gs.board)

            # Panel
            p.draw.rect(screen, p.Color(24,24,24),
                        (BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, HEIGHT))

            titleFont = p.font.SysFont("Arial", 22, True)
            textFont = p.font.SysFont("Consolas", 18)

            def formatTime(t):
                return f"{int(t//60):02}:{int(t%60):02}"

            # Black
            screen.blit(titleFont.render("Black", True, p.Color("white")),
                        (BOARD_WIDTH+20, 20))
            screen.blit(textFont.render(formatTime(blackTime), True, p.Color("gold")),
                        (BOARD_WIDTH+150, 20))

            # White
            screen.blit(titleFont.render("White", True, p.Color("white")),
                        (BOARD_WIDTH+20, HEIGHT-50))
            screen.blit(textFont.render(formatTime(whiteTime), True, p.Color("gold")),
                        (BOARD_WIDTH+150, HEIGHT-50))

            # Moves
            screen.blit(titleFont.render("Moves", True, p.Color("white")),
                        (BOARD_WIDTH+20, 80))

            y = 110
            for i in range(0, len(gs.moveLog), 2):
                text = f"{i//2+1}. {gs.moveLog[i].getChessNotation()}"
                if i+1 < len(gs.moveLog):
                    text += f" {gs.moveLog[i+1].getChessNotation()}"

                screen.blit(textFont.render(text, True, p.Color("lightgray")),
                            (BOARD_WIDTH+20, y))
                y += 20

            # 🔥 CONTROLS SECTION
            screen.blit(titleFont.render("Controls", True, p.Color("white")),
                        (BOARD_WIDTH+20, 340))

            color = p.Color("#00c853") if AI_ENABLED else p.Color("#d50000")
            p.draw.rect(screen, color, ai_btn, border_radius=8)

            screen.blit(textFont.render(
                "AI: ON" if AI_ENABLED else "AI: OFF",
                True, p.Color("white")),
                (ai_btn.x + 80, ai_btn.y + 12)
            )

        p.display.flip()


def drawBoard(screen):
    colors = [p.Color(235,235,208), p.Color(181,136,99)]
    for r in range(8):
        for c in range(8):
            p.draw.rect(screen, colors[(r+c)%2],
                        p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(8):
        for c in range(8):
            if board[r][c] != "--":
                screen.blit(IMAGES[board[r][c]],
                            p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()