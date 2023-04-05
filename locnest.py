from colored import fg, bg, attr
import json
import os



settingFile = ('setting.json') # setting file name
settings = {'aimKey' : ''} # setting the aim key to save file


if os.path.exists(settingFile): # check if Program is already run and loads premade 
    from locaim import locaimmed
    locaimmed()
elif not os.path.exists(settingFile): # first time running locnest will go through settings
    aimkey = input(f"{fg(57)}{attr('bold')}[+] Enter the Aim Key to Set: {attr(0)}")
    settings.update({'aimKey' : aimkey})
    # saving the aim key in settings
    with open("setting.json", 'w') as f:
        json.dump(settings, f)


if __name__ == '__main__':
    from locaim import locaimmed
    locaimmed()