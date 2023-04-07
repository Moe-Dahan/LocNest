import tkinter as tk
import os
import json
import torch
import pyautogui

running = False  # Global flag

settingFile = ('\lib\setting.json')
settings = {'location' : '', 'key' : ''}

''' CHECK IF CUDA IS AVAILABLE '''
if torch.cuda.is_available():
    pyautogui.alert("[!] CUDA ACCELERATION [ENABLED]")
else:
    pyautogui.alert("[!] CUDA ACCELERATION IS UNAVAILABLE PREFORMANCE IMPACTED")

''' Gui Starts off here '''
locNest = tk.Tk()
locNest.title('LocNest')
locNest.geometry('300x175')
locNest.iconbitmap("lib\\aim_achieve_accuracy_goal_strategy_target_focus_icon_212663.ico")
''' title frame starts '''
locNestTitleFrame = tk.Frame(locNest)
locNestTitle = tk.Label(locNestTitleFrame, text='LOCNEST: ', font=("Comic Sans MS", 15, "bold")).grid(row=0, column=0)
locNestOnOffLabel = tk.Label(locNestTitleFrame, text='OFF', font=("Comic Sans MS", 15, "bold"), fg='Black').grid(row=0, column=1) # switches label when locnest is on or off
locNestTitleFrame.place(x=65, y=0)

''' config settings start '''
locNestConfigFrame = tk.Frame(locNest)
locNestConfigHeadBodyLabel = tk.Label(locNestConfigFrame, text='Select Head or Body', font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, ipadx=5)
locNestConfigkeyLabel = tk.Label(locNestConfigFrame, text='Enter Aim Key', font=("Comic Sans MS", 10, "bold")).grid(row=0, column=1, ipadx=5)
locNestConfigKeyEntry = tk.Entry(locNestConfigFrame)
locNestConfigKeyEntry.grid(row=1, column=1)
locNestConfigFrame.place(x=5, y=40)

''' adds the button to add the config start '''
locNestAddButtonFrame = tk.Frame(locNest)

''' setting the options '''
options = ['Head', 'Body']

''' Data types options to set and read '''
clicked = tk.StringVar()
clicked.set('Choose Location')

''' setting the dropdown menu '''
locNestConfigHeadBody = tk.OptionMenu( locNestConfigFrame , clicked , *options )
locNestConfigHeadBody.grid(row=1, column=0)

''' addding the config file '''
def addItems():
    location = clicked.get()
    key = locNestConfigKeyEntry.get()
    settings.update({'location' : location, 'key' : key})
    if os.path.exists('lib\setting.json'):
        print(f'{settingFile} already exist')
        pass
    elif not os.path.exists(settingFile): # first time running locnest will go through settings
        with open("lib\setting.json", 'w') as f:
            json.dump(settings, f)

''' adding the add config button '''
locNestConfigButton = tk.Button(locNestAddButtonFrame, text='Add Config', font=("Comic Sans MS", 9, "bold"), width=15, command=addItems).grid(row=2, column=0)
locNestAddButtonFrame.place(x=90, y=100)

''' starting and stopping the locnest start '''
locNestStartStopFrame = tk.Frame(locNest)
def start():
    if running:
        from lib import startLocNest
        startLocNest.loadSettings()
    # After 1 second, call scanning again (create a recursive loop)
    locNest.after(1, start)

# enable the the scan
def Start_locNest():
    # Enable scanning by setting the global flag to True.
    global running
    running = True
    locNestOnOffLabel = tk.Label(locNestTitleFrame, text='ON', font=("Comic Sans MS", 15, "bold"), fg='Green').grid(row=0, column=1)

def Stop_locNest():
    # Stop scanning by setting the global flag to False.
    global running
    running = False
    from lib import startLocNest
    startLocNest.stop()
    locNestOnOffLabel = tk.Label(locNestTitleFrame, text='OFF', font=("Comic Sans MS", 15, "bold"), fg='Red').grid(row=0, column=1)
  
locNestStartButton = tk.Button(locNestStartStopFrame, text='Start LocNest', font=("Comic Sans MS", 9, "bold"), width=15, command=Start_locNest).grid(row=0, column=0, padx=5)
locNestStopButton = tk.Button(locNestStartStopFrame, text='Stop LocNest', font=("Comic Sans MS", 9, "bold"), width=15, command=Stop_locNest).grid(row=0, column=1, padx=5)
locNestStartStopFrame.place(x=20, y=135)
locNest.after(1, start)


locNest.mainloop()