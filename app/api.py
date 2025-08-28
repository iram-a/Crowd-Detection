from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Dict
import pathlib, glob
from app.counter_adapter import count_people

APP = FastAPI(title="Coach Crowd API", version="0.1")
APP.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

APP_DIR = pathlib.Path(__file__).parent
SCENARIOS_DIR = APP_DIR / "scenarios"

@APP.get("/health")
def health(): return {"status": "ok"}

@APP.get("/scenarios")
def scenarios():
    if not SCENARIOS_DIR.exists(): return {"scenarios": []}
    return {"scenarios": sorted([p.name for p in SCENARIOS_DIR.iterdir() if p.is_dir()])}

def _images_for(scenario: str):
    folder = SCENARIOS_DIR / scenario
    if not folder.exists(): raise HTTPException(404, f"Scenario '{scenario}' not found")
    imgs = []
    for ext in ("*.jpg","*.jpeg","*.png","*.bmp"): imgs += glob.glob(str(folder / ext))
    if not imgs: raise HTTPException(400, f"No images in scenario '{scenario}'")
    return sorted(imgs, key=lambda p: pathlib.Path(p).stem)

@APP.get("/crowd_status")
def crowd_status(scenario: str):
    report: Dict[str, dict] = {}
    for p in _images_for(scenario):
        coach_id = pathlib.Path(p).stem
        people, lvl, vis = count_people(p)
        report[coach_id] = {"people": people, "level": lvl, "image": f"/image?name={pathlib.Path(vis).name}"}
    return {"scenario": scenario, "coaches": report}

@APP.get("/image")
def image(name: str):
    p = APP_DIR / "outputs" / name
    if not p.exists(): raise HTTPException(404, "Image not found")
    return FileResponse(str(p))
