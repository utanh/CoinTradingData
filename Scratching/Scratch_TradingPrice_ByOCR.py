import pyautogui
import keyboard
from PIL import Image

import numpy as np
import pandas as pd

from datetime import timedelta

import easyocr

year = 2014
csv_path = "C:/Users/Admin/Desktop/BitcoinByDay/Bitcoin_"+str(year) + ".csv"
#df = pd.DataFrame(columns=['Date', 'BTC_Price', 'Open', 'High', 'Low', 'Close', 'BTC_Volume'])
df = pd.read_csv(csv_path)
df = df.drop('Unnamed: 0', axis=1)
print(df.columns)
reader = easyocr.Reader(['en'])
print("Model done!")

months = ['January', 'February', 'March',
          'April', 'May', 'June',
          'July', 'August', 'September',
          'October', 'November', 'December']
def _OCR(np_img):
    result = reader.readtext(np_img)

    Date, BTC_Price, Open, High, Low, Close, BTC_Volume = None, None, None, None, None, None, None

    for i in range(len(result)):
        if result[i][1].split(' ')[0] in months and str(year) in result[i][1]:
            Date = result[i][1]

        elif 'Price' in result[i][1] and '.' in result[i][1]:
            BTC_Price = result[i][1].split(': ')[-1][1:]

        elif 'Open' in result[i][1] and '.' in result[i][1]:
            Open = result[i][1].split(': ')[-1][1:]

        elif 'High' in result[i][1] and '.' in result[i][1]:
            High = result[i][1].split(': ')[-1][1:]

        elif 'Low' in result[i][1] and '.' in result[i][1]:
            Low = result[i][1].split(': ')[-1][1:]

        elif 'Close' in result[i][1] and '.' in result[i][1]:
            Close = result[i][1].split(': ')[-1][1:]

        elif 'Volume' in result[i][1]:
            if len(result[i][1].split(': ')) >= 2:
                BTC_Volume = result[i][1].split(': ')[-1]
            else:
                BTC_Volume = result[i+1][1]
    print(Date, BTC_Price, Open, High, Low, Close, BTC_Volume)
    return [Date, BTC_Price, Open, High, Low, Close, BTC_Volume]

running = False
if keyboard.read_key() == 's':
    running = True

while running:
    # Screen shot
    im = pyautogui.screenshot()
    np_im = np.array(im)
    print('-------------------------------------ScreenShot done!')
    
    #OCR with Capture
    df.loc[len(df)] = _OCR(np_im)
    print(df.loc[len(df)-1])
    print(len(df))
    
    # Move mouse to x+1, y
    x, y = pyautogui.position()
    pyautogui.moveTo(x+1,y)
    
    if keyboard.is_pressed('p'):
        running = False

    df.to_csv(csv_path)
