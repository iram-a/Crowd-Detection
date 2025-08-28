# app/auto_bucket_images.py
import pathlib, shutil, glob
from counter_adapter import count_people  # uses your working adapter

# ---- settings ----
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC  = ROOT / "Crowd-Detection" / "crowd_images"
DST  = ROOT / "app" / "scenarios"
THRESHOLDS = {"green_max": 15, "yellow_max": 40}  # 0-15 empty, 16-40 moderate, 41+ packed
# ------------------

def bucket_for(n: int) -> str:
    if n <= THRESHOLDS["green_max"]:  return "empty"
    if n <= THRESHOLDS["yellow_max"]: return "moderate"
    return "packed"

def ensure_dirs():
    for d in ["empty","moderate","packed"]:
        (DST / d).mkdir(parents=True, exist_ok=True)

def main():
    ensure_dirs()
    imgs = []
    for ext in ("*.jpg","*.jpeg","*.png","*.bmp"):
        imgs += glob.glob(str(SRC / ext))
    if not imgs:
        raise SystemExit(f"No images found in {SRC}")

    # clear old scenario files (optional)
    for d in (DST/"empty", DST/"moderate", DST/"packed"):
        for f in d.glob("*.*"): f.unlink()

    # count → copy into scenarios as coach_#.jpg
    counters = {"empty":0, "moderate":0, "packed":0}
    for p in sorted(map(pathlib.Path, imgs)):
        n, lvl, _ = count_people(str(p))
        bucket = bucket_for(n)
        counters[bucket] += 1
        out_name = f"coach_{counters[bucket]}.jpg"
        dest = DST / bucket / out_name
        shutil.copy2(p, dest)
        print(f"{p.name:25s} -> {bucket:8s} (people={n})")

    print("\nSummary:", counters)
    print(f"Scenarios created under: {DST}")

if __name__ == "__main__":
    main()
