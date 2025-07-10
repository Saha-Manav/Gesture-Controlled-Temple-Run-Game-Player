from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
import cv2
import time
import math

# Initialize
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2, detectionCon=0.85)

keyboard = KeyboardController()
mouse = MouseController()

cooldown = 1  # seconds between actions
gesture_hold_time = 0.3  # how long a gesture must be held
last_action_time = 0
gesture_start_time = {}

# Helper functions
def calc_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def is_hand_open(lmList):
    return (lmList[8][1] < lmList[6][1] and
            lmList[12][1] < lmList[10][1] and
            lmList[16][1] < lmList[14][1] and
            lmList[20][1] < lmList[18][1])

def is_peace_sign(lmList):
    return (lmList[8][1] < lmList[6][1] and
            lmList[12][1] < lmList[10][1] and
            lmList[16][1] > lmList[14][1] and
            lmList[20][1] > lmList[18][1])

def is_index_up(lmList):
    return (lmList[8][1] < lmList[6][1] and
            lmList[12][1] > lmList[10][1] and
            lmList[16][1] > lmList[14][1] and
            lmList[20][1] > lmList[18][1])

def is_ok_sign(lmList):
    return calc_distance(lmList[4], lmList[8]) < 30

def is_fist(lmList):
    return (lmList[8][1] > lmList[6][1] and
            lmList[12][1] > lmList[10][1] and
            lmList[16][1] > lmList[14][1] and
            lmList[20][1] > lmList[18][1])

# Main loop
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame)  # Detect hands and draw

    current_time = time.time()
    gestures = {}

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            label = hand["type"]  # "Left" or "Right"

            if is_fist(lmList):
                gestures[label] = 'fist'
            elif is_ok_sign(lmList):
                gestures[label] = 'mouse_click'
            elif is_peace_sign(lmList):
                gestures[label] = 'jump'
            elif is_index_up(lmList):
                gestures[label] = 'slide'
            elif is_hand_open(lmList):
                gestures[label] = 'left' if label == "Left" else 'right'

        if gestures.get("Left") == 'fist' and gestures.get("Right") == 'fist':
            cv2.putText(frame, "✊✊ Both fists - No Action", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            for label, gesture in gestures.items():
                if gesture == 'fist':
                    continue

                other_label = "Right" if label == "Left" else "Left"
                if other_label in gestures and gestures[other_label] == 'fist':
                    pass

                if gesture not in gesture_start_time:
                    gesture_start_time[gesture] = current_time
                elif current_time - gesture_start_time[gesture] > gesture_hold_time and current_time - last_action_time > cooldown:
                    if gesture == 'slide':
                        print("☝️ Index finger → Slide")
                        keyboard.press(Key.down)
                        keyboard.release(Key.down)
                    elif gesture == 'jump':
                        print("✌️ Peace sign → Jump")
                        keyboard.press(Key.up)
                        keyboard.release(Key.up)
                    elif gesture == 'left':
                        print("✋ Left palm → Move Left")
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                    elif gesture == 'right':
                        print("🤚 Right palm → Move Right")
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                    elif gesture == 'mouse_click':
                        print("👌 OK sign → Mouse Click")
                        mouse.click(Button.left, 1)

                    last_action_time = current_time
                    gesture_start_time = {}
    else:
        gesture_start_time = {}

    cv2.imshow("Gesture Controller", frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
