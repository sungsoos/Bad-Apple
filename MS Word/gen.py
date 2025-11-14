import cv2

# === CONFIGURATION ===
VIDEO_PATH = "bad_apple_gray.mp4"      # Path to your Bad Apple video
OUTPUT_FILE = "bad_apple_frames.txt"
WIDTH = 40                             # ASCII width (increase for better resolution)
HEIGHT = 20                            # ASCII height
FPS = 60                               # Reduce fps to make text file smaller

# More ASCII characters from dark to light
ASCII_CHARS = ["@ ", "% ", "# ", "* ", "+ ", "= ", "- ", ": ", ". ", "  "]  

# === FUNCTION TO CONVERT GRAYSCALE TO ASCII ===
def pixel_to_ascii(pixel_value):
    # Map 0-255 to index in ASCII_CHARS
    num_chars = len(ASCII_CHARS)
    index = int(pixel_value / 255 * (num_chars - 1))
    return ASCII_CHARS[index]

# === OPEN VIDEO ===
cap = cv2.VideoCapture(VIDEO_PATH)
video_fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = max(int(video_fps / FPS), 1)

frames = []
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % frame_interval == 0:
        # Resize frame
        frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
        # Convert to grayscale
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        # Convert to ASCII
        ascii_frame = "\n".join(
            "".join(pixel_to_ascii(pixel) for pixel in row) for row in gray
        )
        frames.append(ascii_frame)
    frame_count += 1

cap.release()

# === WRITE FRAMES TO TEXT FILE ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("===FRAME===\n".join(frames))

print(f"Done! {len(frames)} frames saved to {OUTPUT_FILE}")
