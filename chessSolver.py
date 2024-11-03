import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-macos-m1-apple-silicon")
def BestMove(fenString):
    board = chess.Board(fen=fenString)
    try:
        move = engine.play(board, chess.engine.Limit(time=0.5)).move
        info = engine.analyse(board, chess.engine.Limit(depth=20))
        evaluation = info["score"]
    except:
        move = chess.Move.null
        evaluation = 0
        print('invalid FEN')
    print(board)
    return (move, evaluation)
