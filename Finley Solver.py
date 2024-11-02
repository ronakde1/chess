import chess
import chess.engine

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("Engine/stockfish-windows-2022-x86-64-modern.exe")