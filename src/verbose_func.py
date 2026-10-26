import cv2 as cv


def verbose_func(frame, headpos, eyes,faceLandmarks, w, h, DangerousSituation):
    pitch, yaw, roll =  headpos
    l_eye_ear, r_eye_ear = eyes

    cv.putText(frame, f"Yaw:{yaw:.2f}, Pitch: {pitch:.2f}, roll: {roll:.2f},Danger: {DangerousSituation}", (20, 50),
               cv.FONT_HERSHEY_PLAIN, 1.4,
               (0, 0, 255), 1)
    cv.putText(frame, f"Left EAR: {l_eye_ear:.2f} | Right EAR: {r_eye_ear:.2f}", (w // 4, 100),
               cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    x = [lm.x * w for lm in faceLandmarks]
    y = [lm.y * h for lm in faceLandmarks]
    startpoint = (int(min(x)), int(min(y)))
    endpoint = (int(max(x)), int(max(y)))

    cv.rectangle(frame, startpoint, endpoint, (255, 0, 255), 2)