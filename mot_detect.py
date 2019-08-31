# simple comment
## reminder for adding features
# # to be removed?
### link to documentation
#### additional resource

#### Eye blink detection with OpenCV, Python, and dlib https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
#### Increasing Raspberry Pi FPS with Python and OpenCV https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
#### Home surveillance and motion detection with the Raspberry Pi, Python, OpenCV, and Dropbox https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

#### Making a LED blink using the Raspberry Pi and Python https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/


from picamera import PiCamera
### https://picamera.readthedocs.io/en/release-1.10/api_array.html#picamera.array.PiRGBArray
### https://picamera.readthedocs.io/en/release-1.10/api_array.html#picamera.array.PiArrayOutput
from picamera.array import PiRGBArray PiArrayOutput
import json
import warnings
import datetime
import time
import cv2
import gestures
import pinOutputs
import dlib

warnings.filterwarnings("ignore")

t11 = t21 = t13 = t14 = t15 = time.time()
left_eye_pts =  [36, 37, 38, 39, 40, 41]
right_eye_pts = [42, 43, 44, 45, 46, 47]

# argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
args = vars(ap.parse_args())
conf = json.load(open(args['conf'])


# init camera
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiArrayOutput(camera, size = camera.resolution)

# camera warm up
print("Camera warming up")
## turn pin devoted to warming up ON
time.sleep(conf["camera_warmup_time"])
## turn pin devoted to warming up OFF

# capture frames
### https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.capture
## format to decide
## 'bgr' - Write the raw image data to a file in 24-bit BGR format
## 'bgra' - Write the raw image data to a file in 32-bit BGRA format

# detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") ### http://dlib.net/python/index.html#dlib.shape_predictor

# for each caption in an infinite sequence of captures
for f in camera.capture_continuous(rawCapture, format='bgr', use_video_port = True):

	# take the actual array with the image
	frame = f.array ## taking directly a cv2 object is faster?

	# basic processing
	frame = imutils.resize(frame, width = 500) # here we resize the picture: one of the tutorials does like that, maybe we don't need it
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to gray
	gray = cv2.GaussianBlur(gray, (21,21), 0) # this removes high frequency noise in the gray picture

	## detect faces in the gray frame
	faces = detector(gray)
	# if more than one face is detected
	if len(faces)>1:
		print("Multiple faces detected")
		## turn pin devoted to error ON

    for face in faces: # here in theory we should "iterate" only on a single face

		# find the points in the frame see landmarks_points.png in the project directory
        landmarks = predictor(gray, face)

        # detect blinking ratios
		right_blink_ratio = gestures.get_blinking_ratio(right_eye_pts, landmarks) # gestures.
        left_blink_ratio = gestures.get_blinking_ratio(left_eye_pts, landmarks) # gestures.
        avg_blink_ratio = (left_blink_ratio + right_blink_ratio) / 2

        # detect gaze ratios
		right_gaze_ratio = .gestures.get_gaze_ratio(right_eye_pts, landmarks) # gestures.
        left_gaze_ratio = gestures.get_gaze_ratio(left_eye_pts, landmarks) # gestures.
        avg_gaze_ratio = (left_gaze_ratio + right_gaze_ratio) / 2


	# Below a simple implementation for triggering each command.
	# We must test if this method leads to a stable enough sistem, on the contrary we must find a more robust solution: the randomness of the measurements
	# visualized by the plots in Measurement Analysis gives an insight of the possible issue: if flag == True and JUST BY CHANCE we measure a new value
	# such that recCond is not met, then the third condition is met (not recCond1 and flag1) and we stop counting the time by mistake

	# 1) eyeballs to right
	recCond1 = avg_gaze_ratio < 1  # recording condition (I put this line right after the imports.. now I keep it also here for code legibility and understanding)
	if recCond1 and not flag1:
		t11 = time.time() # t1 (1)
		duration1 = 0.
		flag1 = True
	if recCond1 and flag1:
		t21 = time.time() # t2 (1)
	if not recCond1 and flag1:
		duration1 = t21-t11
		flag1 = False
	#if not recCond1 and not flag1:
	#	flag1 = False
	if duration1 > 3:
		print("Eyeballs to right -> execute command #1")
		pinOutputs.send_signal(pin_number=3)

	# 2) eyeballs to left
	recCond2 = avg_gaze_ratio > 1.7
	if recCond2 and not flag2:
		t12 = time.time()
		duration2 = 0.
		flag2 = True
	if recCond2 and flag2:
		t22 = time.time()
	if not recCond2 and flag2:
		duration2 = t22-t12
		flag2 = False
	#if not recCond2 and not flag2:
	#	flag2 = False
	if duration2 > 3:
		print("Eyeballs to left -> execute command #2")
		pinOutputs.send_signal(pin_number=5)

	# 3) both eyes closed for more than 3 seconds
	recCond3 = avg_blink_ratio > 6
	if recCond3 and not flag3:
		t13 = time.time()
		duration3 = 0.
		flag3 = True
	if recCond3 and flag3:
		t23 = time.time()
	if not recCond3 and flag3:
		duration3 = t23-t13
		flag3 = False
	#if not recCond3 and not flag3:
	#	flag3 = False
	if duration3 > 3:
		print("Both eyes closed -> execute command #3")
		pinOutputs.send_signal(pin_number=7)

	# 4) right eye closed for more than 3 sec
	recCond4 = right_blink_ratio > 6
	if recCond4 and not flag4:
		t14 = time.time()
		duration4 = 0.
		flag4 = True
	if recCond4 and flag4:
		t24 = time.time()
	if not recCond4 and flag4:
		duration4 = t24-t14
		flag4 = False
	#if not recCond4 and not flag4:
	#	flag4 = False
	if duration4 > 3:
		print("Right eye closed -> execute command #4")
		pinOutputs.send_signal(pin_number=8)

	# 5) left eye closed for more than 3 sec
	recCond5 = left_blink_ratio > 6
	if recCond5 and not flag5:
		t15 = time.time()
		duration5 = 0.
		flag5 = True
	if recCond5 and flag5:
		t25 = time.time()
	if not recCond5 and flag5:
		duration5 = t25-t15
		flag5 = False
	#if not recCond5 and not flag5:
	#	flag5 = False
	if duration5 > 3:
		print("Left eye closed -> execute command #5")
		pinOutputs.send_signal(pin_number=10)

	# display to screen in case
	if conf['show_video']:
		### https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html
		## eventually remove parameter names - ie: winname, mat
		## eventually show gray instead of frame (which is coloured)
		cv2.imshow(winname= "Captured image", mat = frame)
		### “& 0xff” effectively masks the variable so it leaves only the value in the last 8 bits, and ignores all the rest of the bits
		key = cv2.waitKey(1) & 0xFF

		### ord() return an integer representing the Unicode code point of that character.  ord('a') returns the integer 97 and ord('€') (Euro sign) returns 8364

		# if 'q' is pressed, break from the loop
		if key == ord('q'):
			break

		# clear the stream in preparation for the next frame
		### again look at https://picamera.readthedocs.io/en/release-1.10/api_array.html#piarrayoutput
		rawCapture.truncate(size=0)

camera.close()
