# hailo10h/vision.py

from picamera2 import Picamera2
import time
import cv2

#-----------------------
# Resolution presets
#-----------------------
RESOLUTIONS = {
    "full": (4608, 2592), # full res for IMX708 (rpi cam module 3)
    "1080p": (1920, 1080),
    "720p": (1280, 720),
    "480p": (640, 480),
}

#-----------------------
# Initialize camera 
#-----------------------
def init_picam(resolution: str = "full") -> Picamera2:
    if resolution not in RESOLUTIONS:
        raise ValueError(f"Unsupported resolution: {resolution}")
    
    size = RESOLUTIONS[resolution]
    picam2 = Picamera2()
    config = picam2.create_video_configuration(
        sensor={"output_size": size},
        main={"format": "RGB888", "size": size},
        buffer_count=4,
    )
    picam2.configure(config)
    picam2.start()

    # autofocus for 1s at startup and then lock to prevent constant autofocus
    picam2.set_controls({"AfMode": 2})
    time.sleep(1.0)
    picam2.set_controls({"AfMode": 0})

    return picam2

#-----------------------
# Main vision loop
#-----------------------
def vision_loop(picam2: Picamera2):
    # OpenCV window
    window_name = "Picamera2 Vision Loop"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # fps variables
    fps = 0.0
    frame_count = 0
    prev_time = time.time()

    # main camera loop
    while True:
        frame = picam2.capture_array()

        # fps calculation
        frame_count += 1
        now = time.time()
        elapsed = now - prev_time
        
        if elapsed >= 1.0:
            fps = frame_count / elapsed
            frame_count = 0
            prev_time = now

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
        )

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    cv2.destroyAllWindows()
    picam2.stop()




