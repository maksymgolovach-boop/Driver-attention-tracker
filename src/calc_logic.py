import cv2 as cv
import numpy as np

#Face 3d model
model_points = np.array([
    (0.0, 0.0, 0.0),             # Nose tip (Landmark 1)
    (0.0, 330.0, 65.0),        # Chin (Landmark 152)
    (-225.0, -170.0, 135.0),     # Left eye outer corner (Landmark 33)
    (225.0, -170.0, 135.0),      # Right eye outer corner (Landmark 263)
    (-150.0, 150.0, -115.0),    # Left mouth corner (Landmark 61)
    (150.0, 150.0, -115.0)      # Right mouth corner (Landmark 291)
], dtype=np.float32)

# Landmark indices: Nose(1), Chin(152), L-Eye(33), R-Eye(263), L-Mouth(61), R-Mouth(291)
key_indices = [1, 152, 33, 263, 61, 291]

# Eyes indicies for eyes state detection
LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]

#calculating Drivers face
def select_driver_face(face_list, frame_width, frame_height):
    largest_face = None
    max_area = 0

    for face in face_list:
        x = [lm.x * frame_width for lm in face]
        y = [lm.y * frame_height for lm in face]

        box_width = max(x) - min(x)
        box_heigth = max(y) - min(y)

        area = box_heigth * box_width

        if area > max_area:
            max_area = area
            largest_face = face

    return largest_face


def calc_EAR(landmarks, indicies):

    pts = np.array([
        [(landmarks[idx].x, landmarks[idx].y)] for idx in indicies]
    )

    v1 = np.linalg.norm(pts[1] - pts[5])
    v2 = np.linalg.norm(pts[2] - pts[4])

    h = np.linalg.norm(pts[0] - pts[3])

    ear = (v1+v2)/(2*h)

    return ear

def get_head_pos(faceLandmarks, img_w, img_h):

    image_points = np.array([
        (faceLandmarks[idx].x * img_w, faceLandmarks[idx].y * img_h) for idx in key_indices],
        dtype=np.float32
    )

    focal_length = img_w
    center = (img_w//2, img_h//2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0,0,1]
    ], dtype=np.float32)

    dist_coeff = np.zeros((4,1))

    succes, rvec, tvec = cv.solvePnP(
        model_points, image_points, camera_matrix, dist_coeff, flags=cv.SOLVEPNP_SQPNP
    )

    rmat, _ = cv.Rodrigues(rvec)
    angles, _, _, _, _, _ = cv.RQDecomp3x3(rmat)

    pitch = angles[0]  # Up / Down
    yaw = angles[1]  # Left / Right
    roll = angles[2]  # Tilt

    return (pitch, yaw, roll)