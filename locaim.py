import json
import pyautogui
import cv2
import numpy as np
from win32api import GetSystemMetrics
import torch
import keyboard
import pydirectinput
import time
from colored import fg, bg, attr



    
def locaimmed():
    ''' loads the saved settings '''
    with open('setting.json') as readSettings:
        loadedKey = json.load(readSettings)
        aKey = loadedKey["aimKey"]
    ''' Grabs the monitor size '''
    width = GetSystemMetrics(0) 
    height = GetSystemMetrics(1)

    print('[+] Checking Cuda Install....')
    if torch.cuda.is_available():
        print(f"{fg(47)}{attr('bold')}CUDA ACCELERATION [ENABLED]{attr(0)}")
    else:
        print(f"{fg(9)}{attr('bold')}[!] CUDA ACCELERATION IS UNAVAILABLE{attr(0)}")
        print(f"{fg(9)}{attr('bold')}[!] Check your PyTorch installation, else performance will be poor{attr(0)}")

    ''' Loads the model '''
    print(f'{fg(227)}{attr("bold")}[+] Loading Model.......{attr(0)}')
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    print(f'{fg(227)}{attr("bold")}[+] Model Loaded{attr(0)}')

    ''' Model configurations Optional but better for human and animal detection '''
    model.conf = 0.5  # confidence threshold (0-1)
    model.iou = 0.45  # NMS IoU threshold (0-1)
    model.classes = [0, 15, 16]  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

    while True:
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
                cv2.rectangle(screen, x1y1, x2y2, (244, 113, 115), 2) #draw the bounding boxes for all of the player detections (except own)
                cv2.circle(screen, (int(center_x), int(center_y)), 1, (0, 255, 0), 5) # creates a circle in the middle of the enemy
                ''' change e to key you like '''
                if keyboard.is_pressed(aKey): 
                    pydirectinput.moveTo(int(width/2 - 500/2 + center_x), int(height/2 - 500/2 + center_y))
                    time.sleep(0.001)


        cv2.imshow('LocNest', screen)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    print('Aim Key is not set run locnest.py first')