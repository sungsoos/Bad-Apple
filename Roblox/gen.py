import os, sys, subprocess, argparse, tempfile
from PIL import Image
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input video file")
parser.add_argument("out_dir", help="output folder for Lua files")
parser.add_argument("--width", type=int, default=64)
parser.add_argument("--height", type=int, default=36)
parser.add_argument("--fps", type=int, default=30)
parser.add_argument("--threshold", type=int, default=128)
parser.add_argument("--rle", action="store_true")
parser.add_argument("--chunk", type=int, default=1000, help="frames per Lua file")
args = parser.parse_args()

W,H,FPS,TH,USE_RLE = args.width,args.height,args.fps,args.threshold,args.rle
os.makedirs(args.out_dir, exist_ok=True)

tmpdir = tempfile.mkdtemp(prefix="badapple_frames_")
cmd = [
    "ffmpeg","-y","-i",args.input,
    "-vf", f"scale={W}:{H},format=gray",
    "-r", str(FPS),
    os.path.join(tmpdir,"frame_%05d.png")
]
print("Extracting frames...")
subprocess.check_call(cmd)

frames_files = sorted([os.path.join(tmpdir,f) for f in os.listdir(tmpdir) if f.endswith(".png")])
print(f"{len(frames_files)} frames extracted.")

def frame_to_bits(path):
    im = Image.open(path).convert("L").resize((W,H))
    return ''.join('1' if p < TH else '0' for p in im.getdata())

def rle_encode(bits):
    out=[]
    last=bits[0]
    cnt=1
    for ch in bits[1:]:
        if ch==last: cnt+=1
        else: out.append(("B" if last=='1' else "W")+str(cnt)); last,ch=ch,ch; cnt=1
    out.append(("B" if last=='1' else "W")+str(cnt))
    return ','.join(out)

# split into chunks
chunks = [frames_files[i:i+args.chunk] for i in range(0,len(frames_files),args.chunk)]
for i, chunk in enumerate(chunks,1):
    out_path = os.path.join(args.out_dir, f"BadAppleFrames_Part{i}.lua")
    lua_lines = [
        f"return {{",
        f"  width = {W},",
        f"  height = {H},",
        f"  fps = {FPS},",
        f"  rle = {str(USE_RLE).lower()},",
        f"  frames = {{"
    ]
    for f in tqdm(chunk, leave=False):
        bits = frame_to_bits(f)
        if USE_RLE: bits = rle_encode(bits)
        bits = bits.replace("\\","\\\\").replace('"','\\"')
        lua_lines.append(f'    "{bits}",')
    lua_lines.append("  }\n}")
    with open(out_path,"w",encoding="utf-8") as fo:
        fo.write("\n".join(lua_lines))
    print(f"Wrote {out_path} ({len(chunk)} frames)")
