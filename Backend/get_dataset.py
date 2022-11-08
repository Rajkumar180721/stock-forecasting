
from multiprocessing import Pool

import yfinance as yf
# import pandas as pd
import time, csv
# import plotly.graph_objs as go
# import plotly.express as px

def writeHistory(code:str):
    start="2016-01-01"
    end="2022-11-06"
    # print(code, start, end)
    df = yf.download(code, start, end)
    if not df.empty:
        df.to_csv(f'datasets/{code}.csv')
    return 'SUCCESS'
    


def getStock(code):
    stock = yf.Ticker(code)
    stockInfo = stock.info
    return stockInfo

def stockCodes():
    with open('Equity.csv', 'r') as file:
        csvFile = csv.reader(file)
        codes = [row[2] for row in csvFile]
        return codes

# def fetchStocks(stockCode):
    # return getStock(stockCode)

def main():
    start = time.time()
    
    codes = stockCodes()
    print(codes)
    # with Pool(100) as p:
    #     p.map(writeHistory, codes)

    end = time.time()
    print('Finished ', end-start, 'seconds')


if __name__ == "__main__":
    main()
