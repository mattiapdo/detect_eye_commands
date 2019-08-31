# deifine a class named PiVideoStream

# imports
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class PiVideoStream:
    def __init__(self, resolution = (320, 240), framerate = 32):
        #initialize camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size = resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format = 'bgr', use_video_port = True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = False

    def start(self):
        '''This method is used to spawn a thread
        that calls the update  method.'''

        # start the thread to read frames from the video PiVideoStream
        Thread(target = self.update, args = ()).start()
        return self

    def update(self):
        '''This method continuously polls the RaspberryPi camera module,
        grabs the most recent frame from the video stream and stores it
        in the frame variable.  It's important to note that this thread is separate
        from our main Python script'''

        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in preparation
            # for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread and
            # resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

        def read(self):
            '''This method returns the frame most recently read'''
            return self.frame

        def stop(self):
            '''This method is used to stop the thread'''
            self.stopped = True
            
