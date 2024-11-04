
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0] # [AI, Player]

while True:
    imgBG = cv2.imread("C:/Users/The Computer World/Desktop/Rock Paper Scissor/resourses/BG.png")
    # we have put this inside while loop because we want to keep update the complete image on every single frame
    # if we keep it outside the while loop it will not be updated and it will contain the previous image during the start of new round
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875) # to resize the image to desirable size
    imgScaled=imgScaled[:, 80:480] # to fit the image in the BG from the centre of the image

    # find hands
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), ( 605,435), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,0), 4)
            
            if timer>3:
                stateResult = True #stops the timer at 3 
                timer = 0

                if hands:
                    playerMove = None
                    hand=hands[0]
                    fingers = detector.fingersUp(hand)# tells how many fringers are up and stores data in form of 0 and1 in an array of size 5
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3    

                    randomNumber = random.randint(1,3) # gives a random no. between 1-3
                    imgAI = cv2.imread(f'C:/Users/The Computer World/Desktop/Rock Paper Scissor/resourses/{randomNumber}.png', cv2.IMREAD_UNCHANGED )
                    # cv2.IMREAD_UNCHANGED has to be used while using cvzone.overlayPNG as without it will remove the alpha channel and we can't use the PNG image
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

                    # Player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                    (playerMove == 2 and randomNumber == 1) or \
                    (playerMove == 3 and randomNumber == 2):
                        scores[1] +=1

                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                    (playerMove == 1 and randomNumber == 2) or \
                    (playerMove == 2 and randomNumber == 3):
                        scores[0] +=1    




    imgBG[234:654, 795:1195] = imgScaled #adds the image into BG frame as per its size

    # here it will happen again and again while inside the above condition it will happens only once
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

    cv2.putText(imgBG, str(scores[0]), ( 410,215), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 6)
    cv2.putText(imgBG, str(scores[1]), ( 1112,215), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 6)

    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("Scaled", imgScaled)
    key = cv2.waitKey(1)
    if key == ord('s'): # adds a key for starting the game
        startGame = True
        initialTime = time.time()
        stateResult = False