import os
import subprocess as sp
import spotipy
import json
import webbrowser
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from pynput.keyboard import Key, Controller
import win32api

keyboard = Controller()


paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

username = 'dx07czymv0wlmnuq29rzqgny1'
clientID = 'Your_Client_Id'
clientSecret = 'Your_Client_Secret'
redirectURI = 'http://google.com/'

def pause():
    #Key.media_play_pause
    win32api.keybd_event(0xb3, 34)

def start_over():
    keyboard.press('0')

def open_notepad():
    os.startfile(paths['notepad'])

def volume_change(vol):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeDb = volume.GetMasterVolumeLevel()
        volume.SetMasterVolumeLevel(currentVolumeDb + vol, None)
        return""
    except Exception:
        return"not possible"

def open_cmd():
    os.system('start cmd')

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def close_camera():
    sp.run('Taskkill /IM WindowsCamera.exe /F', shell=True)

def open_calculator():
    sp.Popen(paths['calculator'])