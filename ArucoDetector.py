import cv2
import numpy as np
from cv2 import aruco
from PIL import Image

dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)
cap = cv2.VideoCapture(1)

def FindBoard(blueOverlay = True):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            continue
        
        parameters =  aruco.DetectorParameters()
        corners, ids, rejectedImgPoints = detector.detectMarkers(frame)
        dist_coeffs = np.zeros((4, 1))
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        if len(corners) == 4:
            id_corner_pairs = list(zip(ids.flatten(), corners))

            id_corner_pairs.sort(key=lambda x: x[0])
            sorted_corners = [corner for _, corner in id_corner_pairs]
            pts_src = np.array([corner[0][0] for corner in sorted_corners], dtype="float32")

            side_length = 300 
            pts_dst = np.array([
                [0, 0],
                [side_length - 1, 0],
                [0, side_length - 1],
                [side_length - 1, side_length - 1],
            ], dtype="float32")

            h, _ = cv2.findHomography(pts_src, pts_dst)

            warped_frame = cv2.warpPerspective(frame, h, (side_length, side_length))
            cv2.imshow('Frame', addHud(warped_frame))
            return warped_frame
            

        else:
            cv2.imshow('Frame', addHud(frame_markers))
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def ProjectBack(startSquare, endSquare):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        parameters =  aruco.DetectorParameters()
        corners, ids, rejectedImgPoints = detector.detectMarkers(frame)
        dist_coeffs = np.zeros((4, 1))
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        if len(corners) == 4:
            id_corner_pairs = list(zip(ids.flatten(), corners))

            id_corner_pairs.sort(key=lambda x: x[0])
            sorted_corners = [corner for _, corner in id_corner_pairs]
            pts_src = np.array([corner[0][0] for corner in sorted_corners], dtype="float32")

            side_length = 300 
            pts_dst = np.array([
                [0, 0],
                [side_length - 1, 0],
                [0, side_length - 1],
                [side_length - 1, side_length - 1],
            ], dtype="float32")

            h, _ = cv2.findHomography(pts_src, pts_dst)

            warped_frame = cv2.warpPerspective(frame, h, (side_length, side_length))

            warped_frame = DrawArrow(warped_frame, startSquare, endSquare)
            h_inv, _ = cv2.findHomography(pts_dst, pts_src)

            warped_back = cv2.warpPerspective(warped_frame, h_inv, (frame.shape[1], frame.shape[0]))

            ordered_pts_src = np.array([
                pts_src[0],
                pts_src[1],
                pts_src[3],
                pts_src[2]
            ], dtype=np.int32)

            mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)

            cv2.fillPoly(mask, [ordered_pts_src], 255)

            element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            mask = cv2.erode(mask, element, iterations=3)

            frame_masked = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
            warped_back_masked = cv2.bitwise_and(warped_back, warped_back, mask=mask)
            im_out = cv2.add(frame_masked, warped_back_masked)

            cv2.imshow('Frame', addHud(im_out))
        else:
            cv2.imshow('Frame', addHud(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def CropBoard(img, padding):
    croppedImg = img.crop((
        padding,
        padding, 
        img.width - padding,
        img.height - padding
    ))
    return croppedImg

def ToPIL(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def DrawArrow(img, startSquare, endSquare):
    grid_size = 8
    width, height, _ = img.shape
    square_width = width // grid_size
    square_height = height // grid_size

    startx, starty = startSquare
    endx, endy = endSquare

    xs = int((startx+0.5) * square_width)
    ys = int((starty+0.5) * square_height)

    xe = int((endx+0.5) * square_width)
    ye = int((endy+0.5) * square_height)

    arrowColour = (219, 175, 31)
    arrowWidth = 4
    imgWithArrow = cv2.arrowedLine(img, (ys,xs), (ye, xe), arrowColour, arrowWidth)

    text_x = int((xs + xe) / 2)
    text_y = height - int((ys + ye) / 2)

    if ys > ye:
        text_y += 4  
    else:
        text_y -= 4 

    # text = str(evaluation)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # fontScale = 1
    # textColor = (0, 255, 0) 
    # textThickness = 2

    # imgWithArrow = cv2.flip(imgWithArrow, 0)
    # cv2.putText(imgWithArrow, text, (text_x, text_y), font, fontScale, textColor, textThickness, cv2.LINE_AA)
    # imgWithArrow = cv2.flip(imgWithArrow, 0)

    return imgWithArrow

def GetSquares():
    board = FindBoard()

    grid_size = 8
    width, height, _ = board.shape
    square_width = width // grid_size
    square_height = height // grid_size

    squares = [[] for _ in range(8)]

    for row in range(grid_size):
        for col in range(grid_size):
            left = col * square_width
            top = row * square_height
            right = left + square_width
            bottom = top + square_height

            square = board[top:bottom, left:right]
            square = cv2.flip(square, 0)
            squares[7-row].append(square)
        
    # for row in squares:
    #     for square in row:
    #         cv2.imshow("SquaraddHud       ClassifySquare(square)
    #         cv2.waitKey(0)
    return squares

def addHud(baseImg, position=(0, 0)):
    overlayImg = cv2.imread("assets/hud.png", cv2.IMREAD_UNCHANGED)
    x, y = position
    overlayHeight, overlayWidth = overlayImg.shape[:2]
    baseImg = baseImg.copy()

    if x + overlayWidth > baseImg.shape[1] or y + overlayHeight > baseImg.shape[0]:
        overlayWidth = min(overlayWidth, baseImg.shape[1] - x)
        overlayHeight = min(overlayHeight, baseImg.shape[0] - y)
        overlayImg = overlayImg[:overlayHeight, :overlayWidth]

    if overlayImg.shape[2] == 4:
        overlayColor = overlayImg[:, :, :3]
        alphaOverlay = overlayImg[:, :, 3] / 255.0
        alphaBase = 1 - alphaOverlay

        for c in range(3):
            baseImg[y:y + overlayHeight, x:x + overlayWidth, c] = (
                alphaOverlay * overlayColor[:, :, c] +
                alphaBase * baseImg[y:y + overlayHeight, x:x + overlayWidth, c]
            )
    else:
        baseImg[y:y + overlayHeight, x:x + overlayWidth] = overlayImg

    return baseImg




def ClassifySquare(img):
    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    average = np.average(rgbImg, axis = (0,1))
    print(average)


if __name__ == "__main__":
    seed = 0
    squares = GetSquares()
    for row in squares:
        for square in row:
            square = ToPIL(square)
            square.save(f"Raw Data 2/{seed}.png")
            seed += 1
        # if seed >= 16:
        #     break
        
        
# # board = None
# # while board == None:
# #     board = FindBoard()
# board = FindBoard(projectBack=False)


# # while True:
# #     cv2.imshow("square",addHudif cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
# #board.show()

# grid_size = 8
# width, height, _ = board.shape
# square_width = width // grid_size
# square_height = height // grid_size

# squares = []
# # Loop through each square position
# for row in range(grid_size):
#     for col in range(grid_size):
#         # Calculate the coordinates of the current square
#         left = col * square_width
#         top = row * square_height
#         right = left + square_width
#         bottom = top + square_height
        
#         # Crop the square and add it to the list
#         square = board[top:bottom, left:right]
#         squares.append(square)
    
# iterable = iter(squares)
# while True:
#     cv2.imshow("sqaure",addHud
#     cv2.waitKey(0)

