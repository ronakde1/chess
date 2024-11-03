#import opencvrun2
import ArucoDetector
import chessSolver
from chess import Move, square_name
import voice
from time import perf_counter
import asyncio

def main():
    voice.say("Charvis Online")
    while True:
        print("Looking for board")
        images = ArucoDetector.GetSquares()

        print(f"Found board. Classifying...")
        time_start = perf_counter()

        fen_string = asyncio.run(ArucoDetector.classifyBoardWhileStream(images))
        print(f"Classified squares in {perf_counter()-time_start} s")
        print(f"Classified FEN string: {fen_string}")
        move, isWin = chessSolver.BestMove(fen_string)
        print(f"Got best move in {perf_counter()-time_start} s")
        if move == Move.null:
            continue
        if isWin:
            break
        voice.saymove(square_name(move.from_square), square_name(move.to_square))
        fromSquare = (move.from_square//8, move.from_square % 8)
        toSquare = (move.to_square//8, move.to_square % 8)
        ArucoDetector.ProjectBack(fromSquare, toSquare)
    voice.win()


if __name__ == "__main__":
    main()
