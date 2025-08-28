from ultralytics import YOLO
import pathlib, cv2

# ROOT now points to the repo root: .../Crowd-Detection
ROOT = pathlib.Path(__file__).resolve().parents[1]

# Weights in the repo folder
CANDIDATES = [
    ROOT / "best.pt",
    ROOT / "runs" / "detect" / "train" / "weights" / "best.pt",
    ROOT / "yolov8n.pt",
]
for p in CANDIDATES:
    if p.exists():
        WEIGHTS = p
        break
else:
    WEIGHTS = "yolov8n.pt"  # fallback (Ultralytics will download)

_MODEL = YOLO(str(WEIGHTS))

def _level(n: int) -> str:
    if n >= 10:
        return "red"
    if n >= 5:
        return "yellow"
    return "green"

def count_people(image_path: str, conf: float = 0.25):
    res = _MODEL(image_path, conf=conf, classes=[0])
    people = int(sum(len(r.boxes) for r in res))
    lvl = _level(people)

    out_dir = pathlib.Path(__file__).parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    vis = res[0].plot()
    out_path = out_dir / f"vis_{pathlib.Path(image_path).name}"
    cv2.imwrite(str(out_path), vis)

    return people, lvl, str(out_path)
