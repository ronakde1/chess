import chess
import chess.engine


def BestMove(fenString):
    board = chess.Board(fen=fenString)
    engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-macos-m1-apple-silicon")
    try:
        isWin = board.is_checkmate()
        move = engine.play(board, chess.engine.Limit(time=0.5)).move
    except:
        move = chess.Move.null
        isWin = False
        print('invalid FEN')
    print(board)
    return (move, isWin)
