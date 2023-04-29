import cv2
from hand_utilities import Hand
from arduino_connect import ArduinoConnection
import math
import time
import random

# connect to Arduino
ard_device = ArduinoConnection("COM3", 9600)
# connect to camera
cap = cv2.VideoCapture(0)
hand = Hand()
while True:
    ret, frame = cap.read()

    frame1 = cv2.resize(frame, (320, 240))
    states_fingers = hand.get_fingers_state(frame1)
    if states_fingers:
        values = list()
        for id_finger in hand.fingers_ids:
            values.append(states_fingers[id_finger])
        # send finger states to Arduino
        if values == [True, False, False, False, False]:
            rock_paper_scissors = random.choice(
                [[False, False, False, False, False], [True, False, False, True, True], [True, True, True, True, True]])
            print(rock_paper_scissors)  # бумага/ножницы/камень
            values = rock_paper_scissors
            print('У вас есть три секунды, чтобы показать жест!')
            for i in range(3):
                print(i + 1)
                time.sleep(1)
            bot = values[:]
            ard_device.write_array([3, *values])
            frame2 = cv2.resize(frame, (320, 240))
            states_fingers = hand.get_fingers_state(frame2)
            if states_fingers:
                values = list()
                for id_finger in hand.fingers_ids:
                    values.append(states_fingers[id_finger])
            if values == [False, False, False, False, False]:
                if bot == [False, False, False, False, False]:
                    print('Ничья!')
                elif bot == [True, True, True, True, True]:
                    print('Вы выиграли!')
                elif bot == [True, False, False, True, True]:
                    print('Вы проиграли!')
                else:
                    print('Неверный жест!')
            elif values == [True, True, True, True, True]:
                if bot == [False, False, False, False, False]:
                    print('Вы проиграли!')
                elif bot == [True, True, True, True, True]:
                    print('Ничья!')
                elif bot == [True, False, False, True, True]:
                    print('Вы выиграли!')
                else:
                    print('Неверный жест!')
            elif values == [True, False, False, True, True]:
                if bot == [False, False, False, False, False]:
                    print('Вы выиграли!')
                elif bot == [True, True, True, True, True]:
                    print('Вы проиграли!')
                elif bot == [True, False, False, True, True]:
                    print('Ничья!')
                else:
                    print('Неверный жест!')
    cv2.imshow("Frame", frame1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
