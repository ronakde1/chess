#import opencvrun2
import ArucoDetector
import chessSolver
import classify2
from chess import Move, square_name
import voice
from time import perf_counter
import logging
import threading

logger = logging.getLogger(__name__)

def main():
    voice.say("Charvis Online")
    while True:
        logger.debug("Looking for board")
        images = ArucoDetector.GetSquares()

        logger.debug(f"Got {len(images)} squares")
        time_start = perf_counter()
        
        # stream the camera feed in a separate thread so it doesn't freeze
        # while we process stuff
        ArucoDetector.stop_stream.clear()
        stream_thread = threading.Thread(target=ArucoDetector.stream)
        stream_thread.start()

        fen_string = ""
        empty_count = 0
        for row in images:
            for image in row:
                classified = classify2.classify_image(image)
                if classified.lower() == "e":
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

        logger.debug(f"Classified squares in {perf_counter()-time_start} s")
        logger.info(f"Classified FEN string: {fen_string}")
        move, isWin = chessSolver.BestMove(fen_string)
        logger.debug(f"Got best move in {perf_counter()-time_start} s")
        if move == Move.null:
            continue
        if isWin:
            break
        voice.saymove(square_name(move.from_square), square_name(move.to_square))
        fromSquare = (move.from_square//8, move.from_square % 8)
        toSquare = (move.to_square//8, move.to_square % 8)

        ArucoDetector.stop_stream.set()
        assert (not stream_thread.is_alive(), "Stream thread didn't die?!")
        ArucoDetector.ProjectBack(fromSquare, toSquare)
    voice.win()


if __name__ == "__main__":
    main()
