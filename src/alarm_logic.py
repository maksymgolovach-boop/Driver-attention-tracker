import time
import pygame
import cv2 as cv

COUNTDOWN_DURATION = 3.0
dangerous_time = None

Alarm_path = "res/alarm.wav"
pygame.mixer.init()

alarm = pygame.mixer.Sound(Alarm_path)

def set_Alarm(frame, DangerousSituation, h):
    global dangerous_time

    curr_time = time.time()

    if DangerousSituation:
        if dangerous_time is None:
            dangerous_time = curr_time
        else:
            elapsed_time = curr_time - dangerous_time
            if elapsed_time >= COUNTDOWN_DURATION:
                cv.putText(frame, "DRIVER LOST ATTENTION!!!", (0, h - 10), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
                alarm.play(-1)
    else:
        dangerous_time = None
        alarm.stop()