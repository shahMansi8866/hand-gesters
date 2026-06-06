import cv2
import mediapipe as mp
import pyautogui
import math

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

mp_draw = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
smooth = 6

click_cooldown = 0
dragging = False
prev_hand_y = 0


while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            # -----------------------------
            # FINGER LANDMARKS
            # -----------------------------
            index_tip = lm[8]
            middle_tip = lm[12]
            thumb_tip = lm[4]

            index_pip = lm[6]
            middle_pip = lm[10]
            ring_pip = lm[14]
            pinky_pip = lm[18]

            # -----------------------------
            # STABLE FINGER CHECK
            # -----------------------------
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = lm[16].y < ring_pip.y
            pinky_up = lm[20].y < pinky_pip.y

            finger_count = sum([index_up, middle_up, ring_up, pinky_up])

            # -----------------------------
            # CURSOR CONTROL (1 FINGER)
            # -----------------------------
            if finger_count == 1:

                x = int(index_tip.x * screen_w)
                y = int(index_tip.y * screen_h)

                curr_x = prev_x + (x - prev_x) / smooth
                curr_y = prev_y + (y - prev_y) / smooth

                pyautogui.moveTo(curr_x, curr_y)

                prev_x, prev_y = curr_x, curr_y
                dragging = False

            # -----------------------------
            # PINCH DRAG (THUMB + INDEX)
            # -----------------------------
            thumb_index_dist = math.hypot(
                thumb_tip.x - index_tip.x,
                thumb_tip.y - index_tip.y
            )

            if thumb_index_dist < 0.035 and click_cooldown == 0:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True

            elif thumb_index_dist > 0.05 and dragging:
                pyautogui.mouseUp()
                dragging = False
                click_cooldown = 10

            # -----------------------------
            # CLICK (2 FINGERS)
            # -----------------------------
            if finger_count == 2 and click_cooldown == 0:
                pyautogui.click()
                click_cooldown = 12

            # -----------------------------
            # SCROLL DOWN (3 FINGERS)
            # -----------------------------
            if finger_count == 3:
                pyautogui.scroll(-10)

            # -----------------------------
            # SCROLL (4 FINGERS UP/DOWN FIXED)
            # -----------------------------
            if finger_count == 4:

                current_hand_y = lm[0].y

                if prev_hand_y != 0:
                    movement = current_hand_y - prev_hand_y

                    # Hand UP → scroll UP
                    if movement < -0.01:
                        pyautogui.scroll(15)

                    # Hand DOWN → scroll DOWN
                    elif movement > 0.01:
                        pyautogui.scroll(-15)

                prev_hand_y = current_hand_y

            else:
                prev_hand_y = 0  # reset when not 4 fingers

            # -----------------------------
            # COOLDOWN UPDATE
            # -----------------------------
            if click_cooldown > 0:
                click_cooldown -= 1

    cv2.imshow("PRO Gesture Control System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()