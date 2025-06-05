
import cv2
import os

video = cv2.VideoCapture("Oocyte osmotic behavior.mp4")
fps = int(video.get(cv2.CAP_PROP_FPS))

output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

for sec in range(360):
    frame_id = sec * fps
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    success, image = video.read()
    if success:
        cv2.imwrite(f"{output_dir}/frame_{sec}.jpg", image)
video.release()
