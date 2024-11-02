import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-macos-m1-apple-silicon")
def BestMove(fenString):
    board = chess.Board(fen=fenString)
    move = engine.play(board, chess.engine.Limit(time=0.5)).move
    return ((move.from_square // 8, move.from_square % 8), (move.to_square // 8, move.to_square % 8))

print(BestMove(chess.STARTING_FEN))
