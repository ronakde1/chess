import opencvrun2
import ArucoDetector
import chessSolver
import classify2

def main():
    while True:
        images = ArucoDetector.GetSquares()

        fen_string = ""
        empty_count = 0
        for row in images:
            for image in row:
                classified = classify2.classify_image(image)
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

        print(fen_string)
        move = chessSolver.BestMove(fen_string)
        fromSquare = (move.from_square//8, move.from_square % 8)
        toSquare = (move.to_square//8, move.to_square % 8)
        ArucoDetector.ProjectBack(fromSquare, toSquare)


if __name__ == "__main__":
    main()
