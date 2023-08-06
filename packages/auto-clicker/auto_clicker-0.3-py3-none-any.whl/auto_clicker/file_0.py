import pyautogui
import numpy as np
import cv2 # installed with pip install opencv-python
from pynput.mouse import Controller, Button

mouse = Controller()

class imagepos():
    def __init__(self,image,offx=0,offy=0):
        self.__pos = imagesearch(image)
        self.__posx = self.__pos[0] + offx
        self.__posy = self.__pos[1] + offy

    def click(self):
        mouse.position = (self.__posx,self.__posy)
        mouse.click(Button.left, 1)

    def hover(self):
        mouse.position = (self.__posx,self.__posy)

    def press(self):
        mouse.position = (self.__posx,self.__posy)
        mouse.press(Button.left)


def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc
