from src.calc_logic import *
from src.verbose_func import *
from src.landmarker import *
from src.alarm_logic import *
from src.verifyPos import IsDangerous

verbose = True

DangerousSituation = False

cap = cv.VideoCapture(0)
ret, frame = cap.read()
h,w, _ = frame.shape

if not cap.isOpened():
    print("Couldn't access the camera")
    exit(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Couldn't receive frame")
        break

    rgb_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

    timestamp_ms = int(time.time() * 1000)
    detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

    if detection_result.face_landmarks:
        faceLandmarks = select_driver_face(detection_result.face_landmarks, w, h)

        headrot = get_head_pos(faceLandmarks, w, h)
        l_eye_ear = calc_EAR(landmarks=faceLandmarks, indicies=LEFT_EYE_INDICES)
        r_eye_ear = calc_EAR(landmarks=faceLandmarks, indicies=RIGHT_EYE_INDICES)

        if verbose:
            verbose_func(frame, headrot, (l_eye_ear, r_eye_ear), faceLandmarks, w, h, DangerousSituation)

        DangerousSituation = IsDangerous(headrot, (l_eye_ear, r_eye_ear))
    else:
        cv.putText(frame, "NO FACE DETECTED", (0, h - 10), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
        print("No face detected!!!")

    set_Alarm(frame, DangerousSituation, h)

    cv.imshow("Driver Attention Verifier",frame)
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()