import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-macos-m1-apple-silicon")
def BestMove(fenString):
    board = chess.Board(fen=fenString)
    move = engine.play(board, chess.engine.Limit(time=0.5)).move
    print(board)
    return move
