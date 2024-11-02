import opencvrun2
import ArucoDetector

def main():
    while True:
        images, img_data = ArucoDetector.GetSquares()

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

        print(fen_string)


if __name__ == "__main__":
    main()
