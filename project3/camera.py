import cv2
import time
import os

# Initialize the webcam
print("Attempting to open webcam (device index 0)...")

# Behind the scenes:
# - cv2.VideoCapture(0) attempts to open the default video capture device.
# - On Linux, this corresponds to the device file /dev/video0.
# - The OpenCV library uses V4L2 (Video4Linux2) APIs to interact with the webcam.
# - The OS checks permissions and handles device file interactions.
cap = cv2.VideoCapture(0)

# Retrieve webcam properties
print("Retrieving webcam properties...")
# The following calls query properties from the video capture device.
# This involves sending IOCTL (Input/Output Control) system calls to the driver.
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Width: {width}")
print(f"Height: {height}")
print(f"FPS: {fps}")
input("Press Enter to continue...")

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    # System background:
    # - The device file may not exist or be busy.
    # - The OS returns an error code which OpenCV interprets.
    exit(1)

print("Webcam opened successfully.")

frame_count = 0
start_time = time.time()

while cap.isOpened():
    # Read a frame from the webcam
    print("Attempting to read a frame from the webcam...")
    ret, frame = cap.read()

    if ret:
        frame_count += 1
        # Display the frame in a window
        cv2.imshow('Webcam', frame)

        # Log frame read
        print(f"Frame {frame_count} captured successfully.")
        # Simulate background operations
        # - Data is being transferred from the webcam hardware to system memory.
        # - The driver manages buffering and data format conversions if necessary.

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Detected 'q' key press. Exiting loop.")
            break
    else:
        print("Failed to read frame from webcam.")
        # Possible reasons:
        # - The webcam was disconnected.
        # - An error occurred in the driver.
        break

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Captured {frame_count} frames in {elapsed_time:.2f} seconds.")
if elapsed_time > 0:
    print(f"Average FPS: {frame_count / elapsed_time:.2f}")

# Release the video capture object and close all OpenCV windows
print("Releasing webcam and closing windows...")
# Behind the scenes:
# - cap.release() closes the device file /dev/video0.
# - This signals the driver to release the webcam hardware.
# - cv2.destroyAllWindows() closes all OpenCV windows and cleans up GUI resources.
cap.release()
cv2.destroyAllWindows()
print("Webcam released and all windows closed.")
