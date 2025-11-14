import cv2
from tqdm import tqdm

# ===== CONFIG =====
VIDEO_PATH = "BadApple.mp4"        # Input video file
OUTPUT_JS = "badapple_frames.js"   # Output JS file
WIDTH = 80                          # ASCII width
HEIGHT = 40                         # ASCII height
FPS = 15                            # Output FPS
ASCII_CHARS = ["█", " "]            # Black -> White (2 levels)
# ==================

def pixel_to_char(v):
    """Convert grayscale pixel to ASCII character (black/white)."""
    return ASCII_CHARS[0] if v < 128 else ASCII_CHARS[1]

def frame_to_ascii(frame):
    """Convert a single frame to ASCII string."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
    ascii_frame = "\n".join(
        "".join(pixel_to_char(px) for px in row)
        for row in resized
    )
    return ascii_frame

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    input_fps = cap.get(cv2.CAP_PROP_FPS)
    step = max(int(input_fps / FPS), 1)

    frames = []
    frame_index = 0

    print("Starting conversion...")

    with tqdm(total=total_frames // step, desc="Converting frames") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_index % step == 0:
                ascii_frame = frame_to_ascii(frame)
                frames.append(ascii_frame)
                pbar.update(1)

            frame_index += 1

    cap.release()

    # Write JS file
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("const FRAMES = [\n")
        for fr in frames:
            escaped = fr.replace("\\", "\\\\").replace("`", "\\`")
            f.write(f"`{escaped}`,\n")
        f.write("];\n")

    print(f"\nConversion completed! Total {len(frames)} frames saved.")
    print(f"Output JS file: {OUTPUT_JS}")

if __name__ == "__main__":
    main()
