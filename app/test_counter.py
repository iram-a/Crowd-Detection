from app.counter_adapter import count_people
import pathlib, glob

# pick one of Person-A's crowd images
imgs = glob.glob("Crowd-Detection/crowd_images/*.jpg")
if not imgs:
    raise SystemExit("No images in Crowd-Detection/crowd_images")

test_img = imgs[0]
print("Testing on:", test_img)
people, level, vis = count_people(test_img)
print("People:", people, "Level:", level)
print("Annotated image saved at:", vis)
