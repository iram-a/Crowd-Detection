##Project Title:
Crowd Detection 

##Project Description:
Detect and count people in train crowd images using YOLOv8 tiny model. Crowd levels: Green (0-6), Yellow (7-16), Red (17+).

##Folder Structure
crowd_images/: Input images

annotated_images/: Output images with annotations

detect_and_count.py: Detection script

##Setup Instructions
Install required Python packages:
pip install -r requirements.txt

##Run the script:
python detect_and_count.py