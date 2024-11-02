import opencvrun2
import ArucoDetector
import chessSolver
from chess import Move

def main():
    while True:
        images = ArucoDetector.GetSquares()

        fen_string = ""
        empty_count = 0
        for row in images:
            for image in row:
                classified = opencvrun2.classify(image)
                if classified is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_string += str(empty_count)
                        empty_count = 0
                    fen_string += classified
            if empty_count > 0:
                fen_string += str(empty_count)
                empty_count = 0
            fen_string += "/"
        fen_string = fen_string[:-1]
    
        move = chessSolver.BestMove(fen_string)
        fromSquare = (move.from_square//8, move.from_square % 8)
        toSquare = (move.to_square//8, move.to_square % 8)


if __name__ == "__main__":
    main()
