import json
import pyautogui
import numpy as np
from win32api import GetSystemMetrics
import cv2
import torch
import pydirectinput
import time
import keyboard

''' Grabs the monitor size '''
width = GetSystemMetrics(0) 
height = GetSystemMetrics(1)

''' loads the model '''
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

''' Model configurations Optional but better for human and animal detection '''
# model.conf = 0.5  # confidence threshold (0-1)
# model.iou = 0.45  # NMS IoU threshold (0-1)
model.classes = [0, 15, 16]  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

def loadSettings():
    ''' loads the saved settings '''
    with open('lib\setting.json') as readSettings:
        loadSettings = json.load(readSettings)
        location = loadSettings['location']
        key = loadSettings['key']

    '''                                             left,       top, width, height '''
    screen = pyautogui.screenshot(region=(width/2 - 500/2, height/2 - 500/2, 500, 500))
    screen = np.array(screen)
    screen = screen[:, :, ::-1].copy()
    results = model(screen)

    for *box, conf, cls in results.xyxy[0]: #iterate over each player detected
        x1y1 = [int(x.item()) for x in box[:2]] # Gets the cord for box measurements
        x2y2 = [int(x.item()) for x in box[2:]] # Gets the cord for box measurements
        x1, y1, x2, y2 = *x1y1, *x2y2
        player = x1 < 5
        center_x = (int(x2) + int(x1)) /2
        center_y = (int(y2) + int(y1)) /2
        
        if not player:
            cv2.line(screen, (int(500//2), int(500//2)), (int(center_x), int(center_y)), (244, 242, 113), 2)
            cv2.rectangle(screen, x1y1, x2y2, (244, 113, 115), 2) #draw the bounding boxes for all of the player detections (except own)
            if location == 'Body':
                cv2.circle(screen, (int(center_x), int(center_y)), 1, (0, 255, 0), 5) # creates a circle in the middle of the enemy
                ''' change e to key you like '''
                if keyboard.is_pressed(key): 
                    pydirectinput.moveTo(int(width/2 - 500/2 + center_x), int(height/2 - 500/2 + center_y))
                    time.sleep(0.001)
            if location == 'Head':
                cv2.circle(screen, (int(center_x), int(y1 + 10)), 1, (0, 255, 0), 5) # creates a circle in the middle of the enemy
                if keyboard.is_pressed(key): 
                    pydirectinput.moveTo(int(width/2 - 500/2 + center_x), int(height/2 - 500/2 + int(y1 + 10)))
                    time.sleep(0.001)

    #cv2.imshow('LocNest', screen)

def stop():
    cv2.destroyAllWindows()
        
    

