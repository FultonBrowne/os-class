# https://pygame-gui.readthedocs.io/en/latest/quick_start.html
# https://www.tutorialspoint.com/pygame/pygame_using_camera_module.htm
# https://pygame-gui.readthedocs.io/en/latest/quick_start.html

import pygame  # Pygame is a set of Python modules designed for writing games.
import pygame.camera  # Provides access to camera hardware via Pygame.
import pygame_gui  # A GUI module for Pygame applications.
import sys  # Provides access to system-specific parameters and functions.
import os  # Provides functions for interacting with the operating system.
import logging  # Used for logging debug and operational messages.

# Configure logging to output messages to a file with a specific format.
logging.basicConfig(
    filename='camera_app.log',  # Log file name.
    level=logging.DEBUG,  # Log level to capture all levels of log messages.
    format='%(asctime)s %(levelname)s:%(message)s'  # Log message format.
)

def main():
    # Initialize all imported Pygame modules.
    pygame.init()
    logging.debug("Pygame initialized successfully.")

    # Initialize the camera module to enable webcam functionality.
    pygame.camera.init()
    logging.debug("Pygame camera module initialized.")

    # Define the size of the application window (width x height).
    window_size = (800, 600)

    # Create the main display surface (the window where everything is drawn).
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Camera App")
    logging.debug(f"Application window created with size: {window_size}.")

    # Create a UIManager instance to manage GUI elements.
    manager = pygame_gui.UIManager(window_size)
    logging.debug("UIManager for GUI elements created.")

    # Obtain a list of available camera devices on the system.
    cams = pygame.camera.list_cameras()
    logging.debug(f"Available cameras: {cams}")

    # Check if any cameras are found; if not, exit the application.
    if not cams:
        logging.error("No camera found on the system.")
        print("No camera found")
        pygame.quit()
        sys.exit()

    # Initialize the camera using the first camera in the list.
    # On Linux, this typically corresponds to /dev/video0.
    cam = pygame.camera.Camera(cams[0], (640, 480))
    cam.start()
    logging.debug(f"Camera {cams[0]} started with resolution 640x480.")

    # Initialize a list to keep track of snapshot filenames.
    snapshots = []

    # Scan the current directory for existing image files to include in the gallery.
    files = os.listdir()
    logging.debug(f"Files in current directory: {files}")
    image_files = [file for file in files if file.endswith('.jpg')]
    logging.debug(f"Image files found: {image_files}")
    snapshots.extend(image_files)
    current_photo_index = 0
    logging.debug(f"Total snapshots available: {len(snapshots)}")

    # Define the initial mode of the application ('camera' or 'gallery').
    mode = 'camera'
    logging.debug(f"Application started in '{mode}' mode.")

    # Set up GUI elements.
    # Define a common 'Exit' button.
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 10), (140, 50)),
        text='Exit',
        manager=manager
    )
    logging.debug("Exit button created.")

    # Define buttons specific to 'Camera' mode.
    take_snapshot_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 70), (140, 50)),
        text='Take Snapshot',
        manager=manager
    )
    logging.debug("Take Snapshot button created.")

    go_to_gallery_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 130), (140, 50)),
        text='Gallery',
        manager=manager
    )
    logging.debug("Go to Gallery button created.")

    # Define buttons specific to 'Gallery' mode.
    previous_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 70), (140, 50)),
        text='Previous Photo',
        manager=manager
    )
    logging.debug("Previous Photo button created (hidden by default).")

    next_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 130), (140, 50)),
        text='Next Photo',
        manager=manager
    )
    logging.debug("Next Photo button created (hidden by default).")

    back_to_camera_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((650, 190), (140, 50)),
        text='Camera',
        manager=manager
    )
    logging.debug("Back to Camera button created (hidden by default).")

    # Initially hide buttons that are only used in 'Gallery' mode.
    previous_button.hide()
    next_button.hide()
    back_to_camera_button.hide()

    # Create a clock object to manage the application's frame rate.
    clock = pygame.time.Clock()
    is_running = True
    logging.debug("Entering the main application loop.")

    while is_running:
        # Control the frame rate and get the time delta.
        time_delta = clock.tick(30) / 1000.0  # Convert milliseconds to seconds.
        logging.debug(f"Frame time delta: {time_delta} seconds.")

        # Process events generated by user actions and the system.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Handle the window close event.
                logging.info("QUIT event detected. Exiting the application.")
                is_running = False

            # Pass the event to the GUI manager for processing.
            manager.process_events(event)

            # Check for user interactions with GUI elements.
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Handle 'Exit' button click.
                    if event.ui_element == exit_button:
                        logging.info("Exit button clicked. Exiting the application.")
                        is_running = False

                    # Handle events depending on the current mode.
                    if mode == 'camera':
                        # User is in 'Camera' mode.
                        if event.ui_element == take_snapshot_button:
                            # Capture the current frame from the camera.
                            snapshot = cam.get_image()
                            # Generate a unique filename using the current time.
                            now = pygame.time.get_ticks()
                            file_name = f"snapshot{now}.jpg"
                            # Save the snapshot image to the filesystem.
                            pygame.image.save(snapshot, file_name)
                            logging.info(f"Snapshot saved as {file_name}.")
                            # Add the new snapshot to the list.
                            snapshots.append(file_name)
                        elif event.ui_element == go_to_gallery_button:
                            if snapshots:
                                # Switch to 'Gallery' mode if snapshots are available.
                                mode = 'gallery'
                                current_photo_index = 0
                                logging.info("Switching to 'Gallery' mode.")
                                # Hide 'Camera' mode buttons.
                                take_snapshot_button.hide()
                                go_to_gallery_button.hide()
                                # Show 'Gallery' mode buttons.
                                previous_button.show()
                                next_button.show()
                                back_to_camera_button.show()
                            else:
                                logging.warning("No snapshots to display.")
                                print("No snapshots to display.")
                    elif mode == 'gallery':
                        # User is in 'Gallery' mode.
                        if event.ui_element == previous_button:
                            if current_photo_index > 0:
                                # Move to the previous photo.
                                current_photo_index -= 1
                                logging.debug(f"Moved to previous photo: index {current_photo_index}.")
                        elif event.ui_element == next_button:
                            if current_photo_index < len(snapshots) - 1:
                                # Move to the next photo.
                                current_photo_index += 1
                                logging.debug(f"Moved to next photo: index {current_photo_index}.")
                        elif event.ui_element == back_to_camera_button:
                            # Switch back to 'Camera' mode.
                            mode = 'camera'
                            logging.info("Switching back to 'Camera' mode.")
                            # Show 'Camera' mode buttons.
                            take_snapshot_button.show()
                            go_to_gallery_button.show()
                            # Hide 'Gallery' mode buttons.
                            previous_button.hide()
                            next_button.hide()
                            back_to_camera_button.hide()

        # Clear the screen to prevent drawing artifacts.
        screen.fill((0, 0, 0))

        if mode == 'camera':
            # In 'Camera' mode, capture the current frame from the webcam.
            image = cam.get_image()
            # Display the camera image on the screen at position (0, 0).
            screen.blit(image, (0, 0))
            logging.debug("Camera image captured and displayed.")
        elif mode == 'gallery':
            # In 'Gallery' mode, display the current snapshot.
            if os.path.exists(snapshots[current_photo_index]):
                # Load the image from the filesystem.
                snapshot_image = pygame.image.load(snapshots[current_photo_index])
                # Resize the image to fit the display window.
                snapshot_image = pygame.transform.scale(snapshot_image, (640, 480))
                # Display the snapshot image on the screen.
                screen.blit(snapshot_image, (0, 0))
                logging.debug(f"Displayed snapshot: {snapshots[current_photo_index]}")
            else:
                # If the snapshot file doesn't exist, remove it from the list.
                logging.error(f"Snapshot file {snapshots[current_photo_index]} not found. Removing from list.")
                print("Snapshot file not found, removing from list.")
                del snapshots[current_photo_index]
                if not snapshots:
                    # If no snapshots remain, switch back to 'Camera' mode.
                    mode = 'camera'
                    logging.info("No snapshots left. Switching back to 'Camera' mode.")
                    # Show 'Camera' mode buttons.
                    take_snapshot_button.show()
                    go_to_gallery_button.show()
                    # Hide 'Gallery' mode buttons.
                    previous_button.hide()
                    next_button.hide()
                    back_to_camera_button.hide()
                else:
                    # Adjust the current photo index if necessary.
                    if current_photo_index >= len(snapshots):
                        current_photo_index = len(snapshots) - 1
                        logging.debug(f"Adjusted current photo index to {current_photo_index}.")

        # Update the GUI elements based on user interaction and time.
        manager.update(time_delta)
        # Draw the GUI elements onto the screen.
        manager.draw_ui(screen)

        # Update the display to reflect any changes made during this frame.
        pygame.display.update()
        logging.debug("Display updated.")

    # Clean up resources before exiting.
    cam.stop()
    logging.debug("Camera stopped.")
    pygame.quit()
    logging.debug("Pygame terminated. Application closed.")

if __name__ == "__main__":
    # Entry point of the application.
    main()
