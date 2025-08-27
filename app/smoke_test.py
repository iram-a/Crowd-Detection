# app/smoke_test.py
import pathlib, glob
from counter_adapter import count_people

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "Crowd-Detection" / "crowd_images"
imgs = sorted(glob.glob(str(IMG_DIR / "*.*")))
if not imgs:
    raise SystemExit(f"No images found in: {IMG_DIR}")

test_img = imgs[0]
print("Testing on:", test_img)
people, level, vis = count_people(test_img)
print(f"Result -> people: {people}, level: {level}")
print("Annotated image saved at:", vis)
