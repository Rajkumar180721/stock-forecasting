
from datetime import datetime
import json



def dateObject(date):
    return datetime.strptime(date, "%d/%m/%Y")


def checkUpdate():

    with open('App_State.json', 'r') as file:
        state = json.load(file)

    today = datetime.today().strftime('%d/%m/%Y')
    today = dateObject(today)
    previous = dateObject(state['lastUpdate'])
    return today > previous


def updateState():
    with open('App_State.json', 'r') as file:
        state = json.load(file)

    state['lastUpdate'] = datetime.today().strftime('%d/%m/%Y')
    with open('App_State.json', 'w') as file:
        json.dump(state, file)
