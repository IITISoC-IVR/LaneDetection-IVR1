from enum import Enum
import cv2
import time
from lstr import LSTR

class ModelType(Enum):
    LSTR_180X320 = "lstr_180x320"
    LSTR_240X320 = "lstr_240x320"
    LSTR_360X640 = "lstr_360x640"
    LSTR_480X640 = "lstr_480x640"
    LSTR_720X1280 = "lstr_720x1280"

model_type = ModelType.LSTR_360X640
model_path = f"models/{model_type.value}.onnx"

# Initialize video
# cap = cv2.VideoCapture("video.mp4")
#videoUrl = "https://youtu.be/2CIxM7x-Clc"
#videoPafy = pafy.new(videoUrl)
#print(videoPafy.streams)
cap = cv2.VideoCapture(r"C:\iitisoc\LSTR-Lane detection_real\ONNX-LSTR-Lane-Detection\input_videos\real_environment_input.mp4")


start_time = 0
cap.set(cv2.CAP_PROP_POS_FRAMES,start_time)
fps = cap.get(cv2.CAP_PROP_FPS)
# Initialize lane detection model
lane_detector = LSTR(model_type, model_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


cv2.namedWindow("Detected lanes", cv2.WINDOW_NORMAL)	

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'XVID'), 20, (width,height))

while cap.isOpened():
	try:
		# Read frame from the video
		ret, frame = cap.read()
	except:
		continue

	if ret:	
           start_time = time.time() 
		
           # Detect the lanes
           detected_lanes, lane_ids = lane_detector.detect_lanes(frame)
           output_img = lane_detector.draw_lanes(frame)
        
           total_time = time.time()- start_time
        
           fps = 1/(time.time() - start_time)
           print(int(fps))
        
	
           cv2.imshow("Detected lanes", output_img)
           out.write(output_img)

	else:
		break

	# Press key q to stop
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
out.release()
cv2.destroyAllWindows()