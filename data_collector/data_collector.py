import cv2, time, os
import numpy as np
from lib import frame_rate_camera, config

def centered_rect_points(frame, rect_width, rect_height):
    if len(frame.shape) == 3:
        frame_height, frame_width, colour_depth = frame.shape
    else:
        frame_height, frame_width = frame.shape

    p1x = frame_width // 2 - rect_width // 2
    p1y = frame_height // 2 - rect_height // 2

    p2x = frame_width // 2 + rect_width // 2
    p2y = frame_height // 2 + rect_height // 2

    return (p1x, p1y), (p2x, p2y)

def draw_centered_rect(frame, rect_width, rect_height):
    cv2.rectangle(frame, *centered_rect_points(frame, rect_width+10, rect_height+10), (255, 0, 0), 5)

if __name__ == '__main__':

    background = None

    running = True

    cam = frame_rate_camera.FrameRateCamera(30) # start a fps controlled camera on the default camera at 30fps

    while running:

        frame = cam.frame # get the current frame from the camera

        cv2.putText(frame, "%.2f"%cam.current_fps, (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255)) # only used to show the current frame rate


        draw_centered_rect(frame , *config.CAPTURE_RECTANGLE)

        cv2.imshow("Camera output", frame) # show the image in a window

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        key_press = cv2.waitKey(1)
        if key_press == ord('`'): # if the user presses tilde
            running = False
        elif ord('a') <= key_press <= ord('z'):
            if background is not None:
                frame = frame - background
            rect_point1, rect_point2 = centered_rect_points(frame, *config.CAPTURE_RECTANGLE)

            cropped_frame = frame[rect_point1[1]: rect_point2[1], rect_point1[0]: rect_point2[0]]

            resized_image = cv2.resize(cropped_frame, config.EXPORT_SIZE)
            new_filename = f'dataset\\{chr(key_press)}\\{chr(key_press)}{time.time()}.jpg'
            if not os.path.exists(f'dataset\\{chr(key_press)}'):
                os.makedirs(f'dataset\\{chr(key_press)}')
            cv2.imwrite(new_filename, resized_image)
            print(f'saved {new_filename}')
        elif ord('1') == key_press:
            background = frame.copy()
            print('background recorded')


    cv2.destroyAllWindows() # destroy image window

    #camera is automatically released
