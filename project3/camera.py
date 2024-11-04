# Description: This script captures frames from the webcam and displays them in a window using PySDL2.
# Note: PySDL2 does not provide direct webcam capture functionality. Therefore, we use 'imageio' to capture frames.
# Sources:
# - https://pysdl2.readthedocs.io/
# - https://imageio.readthedocs.io/en/stable/examples.html#reading-from-the-webcam
import sdl2
import sdl2.ext
import imageio
import numpy as np
import time
import os

# Initialize SDL2
sdl2.ext.init()

# Initialize the webcam
print("Attempting to open webcam (device index 0)...")
try:
    reader = imageio.get_reader('<video0>')
except Exception as e:
    print("Error opening video stream or file")
    print(e)
    exit(1)

# Retrieve webcam properties
print("Retrieving webcam properties...")
meta_data = reader.get_meta_data()
width, height = meta_data['size']
fps = meta_data.get('fps', 30)  # Default to 30 FPS if not available
print(f"Width: {width}")
print(f"Height: {height}")
print(f"FPS: {fps}")
input("Press Enter to continue...")

# Create an SDL2 window and renderer
window = sdl2.ext.Window("Webcam", size=(width, height))
window.show()
renderer = sdl2.ext.Renderer(window)

# Create a SpriteFactory for texture sprites
factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

print("Webcam opened successfully.")

frame_count = 0
start_time = time.time()
running = True

while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        elif event.type == sdl2.SDL_KEYDOWN:
            key = event.key.keysym.sym
            if key == sdl2.SDLK_q:
                print("Detected 'q' key press. Exiting loop.")
                running = False
                break
            elif key == sdl2.SDLK_s:
                print("Detected 's' key press. Saving frame to disk.")
                filename = f"frame_{frame_count}.png"
                imageio.imwrite(filename, frame)
                print(f"Frame saved to {filename}.")
                time.sleep(2)
            elif key == sdl2.SDLK_w:
                print("Detected 'w' key press. Displaying recent photos.")
                files = [f for f in os.listdir() if f.endswith('.png')]
                files.sort()
                for f in files:
                    print(f)
                    img = imageio.imread(f)

                    # Create a texture sprite from the image
                    img_surface = sdl2.ext.pixels3d(factory.create_texture_sprite((img.shape[1], img.shape[0])).texture)
                    img_surface[:, :, :] = img.swapaxes(0, 1)

                    # Create a texture sprite
                    sprite = factory.from_surface(img_surface)
                    renderer.clear()
                    renderer.copy(sprite)
                    renderer.present()

                    # Wait for key press to proceed to the next image
                    while True:
                        events = sdl2.ext.get_events()
                        key_pressed = False
                        for event in events:
                            if event.type == sdl2.SDL_QUIT:
                                running = False
                                key_pressed = True
                                break
                            elif event.type == sdl2.SDL_KEYDOWN:
                                key_pressed = True
                                break
                        if key_pressed or not running:
                            break
                    if not running:
                        break
    if not running:
        break

    # Read a frame from the webcam
    print("Attempting to read a frame from the webcam...")
    try:
        frame = reader.get_next_data()
    except Exception as e:
        print("Failed to read frame from webcam.")
        print(e)
        break

    frame_count += 1

    # Create a texture sprite from the image


    # Log frame read
    print(f"Frame {frame_count} captured successfully.")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Captured {frame_count} frames in {elapsed_time:.2f} seconds.")
if elapsed_time > 0:
    print(f"Average FPS: {frame_count / elapsed_time:.2f}")

# Release resources
print("Releasing webcam and closing windows...")
reader.close()
sdl2.ext.quit()
print("Webcam released and all windows closed.")
