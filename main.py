import cv2
import pyfirmata

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 420)

# Connect Arduino board
board = pyfirmata.Arduino('COM3')

# Load Haar Cascade for face detection
faceCascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
    success, img = cap.read()

    # Convert image to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                3
            )
            # Turn LED ON
            board.digital[13].write(1)
    else:
        # Turn LED OFF
        board.digital[13].write(0)

    # Display output
    cv2.imshow('face_detect', img)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
board.digital[13].write(0)
cap.release()
cv2.destroyAllWindows()
