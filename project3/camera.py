import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

while cap.isOpened():
    # Read a frame from the webcam
    ret, frame = cap.read()


    if ret:
        # Display the frame in a window
        cv2.imshow('Webcam', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
