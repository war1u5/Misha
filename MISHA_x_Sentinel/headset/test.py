import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("VR Video Feed", cv2.WINDOW_NORMAL)

# cv2.resizeWindow("VR Video Feed", 1900, 1000)

while True: 
    ret, frame = cap.read()

    if not ret:
        break

    # mask = np.zeros_like(frame)
    # rows, cols, _ = mask.shape
    # mask = cv2.circle(mask, (cols // 2, rows // 2), min(rows, cols) // 2, (255, 255, 255), -1)
    #
    # circular_frame = cv2.bitwise_and(frame, mask)
    #
    # double_frame = cv2.hconcat([circular_frame, circular_frame])

    cv2.imshow('VR Video Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
