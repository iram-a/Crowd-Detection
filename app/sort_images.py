# app/sort_images.py
import pathlib, shutil, glob
from app.counter_adapter import count_people   # uses YOUR working adapter

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC  = ROOT / "crowd_images"
DST  = ROOT / "app" / "scenarios"

# thresholds: 0–15 -> empty, 16–40 -> moderate, 41+ -> packed
def bucket(n: int) -> str:
    if n <= 15: return "empty"
    if n <= 40: return "moderate"
    return "packed"

def main():
    # make folders
    for d in ("empty","moderate","packed"):
        (DST / d).mkdir(parents=True, exist_ok=True)
        # OPTIONAL: clear old files for a clean re-run
        for f in (DST / d).glob("*.*"): f.unlink()

    # collect source images
    imgs = []
    for ext in ("*.jpg","*.jpeg","*.png","*.bmp"):
        imgs += glob.glob(str(SRC / ext))
    if not imgs:
        raise SystemExit(f"No images found in {SRC}")

    counters = {"empty":0,"moderate":0,"packed":0}

    for img in sorted(map(pathlib.Path, imgs)):
        n, lvl, _ = count_people(str(img))
        group = bucket(n)
        counters[group] += 1
        out = DST / group / f"coach_{counters[group]}.jpg"
        shutil.copy2(img, out)
        print(f"{img.name:25s} -> {group:8s} (people={n})")

    print("\nSummary:", counters)
    print(f"Scenarios created in: {DST}")

if __name__ == "__main__":
    main()
