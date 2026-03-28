import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2.exe")

def get_best_move(fen):
    board = chess.Board(fen)
    result = engine.play(board, chess.engine.Limit(time=0.2))
    return result.move.uci()
import atexit
atexit.register(engine.quit)