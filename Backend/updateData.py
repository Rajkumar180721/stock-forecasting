

from multiprocessing import Pool
from datetime import datetime

import yfinance as yf
import time, json


today = datetime.today().strftime('%d/%m/%Y')
previous = ''

def dateObject(date):
    return datetime.strptime(date, "%d/%m/%Y")


def checkUpdate():
    global today, previous
    with open('App_State.json', 'r') as file:
        state = json.load(file)
    today = dateObject(today)
    previous = dateObject(state['lastUpdate'])

    return today > previous


def updateState():
    with open('App_State.json', 'r') as file:
        state = json.load(file)

    state['lastUpdate'] = datetime.today().strftime('%d/%m/%Y')
    with open('App_State.json', 'w') as file:
        json.dump(state, file)


def writeData(code:str):
    start="2016-01-01"
    end="2022-11-06"
    # print(code, start, end)
    df = yf.download(code, start, end)
    if not df.empty:
        df.to_csv(f'datasets/{code}.csv')
    return 'SUCCESS'


def main():
    start = time.time()
    
    end = time.time()
    print('Finished ', end-start, 'seconds')



if __name__ == "__main__":
    # main()
    checkUpdate()