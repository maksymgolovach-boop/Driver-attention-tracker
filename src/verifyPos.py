def IsDangerous(headrot, eyes_ear):

    l_eye_ear, r_eye_ear = eyes_ear
    pitch, yaw, _ = headrot

    if abs(yaw) > 10 or abs(pitch) > 4 or (l_eye_ear < 0.10 and r_eye_ear < 0.10):
        return True

    return False