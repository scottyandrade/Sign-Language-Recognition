import cv2, time, numpy as np
from lib import circular_buffer


class FrameRateCamera:
    def __init__(self, fps, resize=None, frame_rate_counter=20, camera_index = 0) -> None:
        super().__init__()

        self.__camera = cv2.VideoCapture(camera_index)

        self.desired_fps = fps

        self.resize = resize

        self.__last_frame_time = time.time()

        self.__frame_times = circular_buffer.CircularBuffer(frame_rate_counter)

        if not self.__try_read()[0]:
            raise BaseException("Camera failed to read initial frame")

    def __try_read(self) -> tuple:

        ret, frame = self.__camera.read()

        if ret:
            self.current_frame = frame
            self.__frame_times.append(time.time() - self.__last_frame_time)
            self.__last_frame_time = time.time()
        else:
            print("Error reading frame")

        return ret, frame

    @property
    def current_fps(self) -> float:
        """
        Current framerate that the Camera is producing
        :return: The frames per second that the camera is actually outputting
        """
        time_sum = sum(self.__frame_times)  # total amount of time for last [self.frame_times.num_elements] frames

        time_average = time_sum / self.__frame_times.num_elements  # average amount of time between each frame

        return 1 / time_average  # seconds per frame to frames per second

    @property
    def __should_read_new_frame(self) -> bool:
        """
        Whether a new frame should be read to keep with the current desired framerate
        :return: True if a new frame should be read, False otherwise
        """
        time_delta = time.time() - self.__last_frame_time

        desired_frame_time_delta = 1 / self.desired_fps

        current_frame_time_delta = 1 / self.current_fps

        frame_rate_delta = desired_frame_time_delta - current_frame_time_delta # how fast we are reading frames compared to the desired speed, <0 is too slow, > 0 is too fast

        return time_delta >= (desired_frame_time_delta + frame_rate_delta)   # maybe change to take into account error from last frame if frame rate is super important

    @property
    def frame(self) -> np.ndarray:
        if self.__should_read_new_frame:
            self.__try_read()

        if self.resize is not None:
            return cv2.resize(self.current_frame, self.resize)

        return self.current_frame

    def __del__(self):
        self.__camera.release()
