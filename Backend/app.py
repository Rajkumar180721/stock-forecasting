
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from pandas.tseries.offsets import MonthEnd
from datetime import datetime

import pandas as pd
import numpy as np
import json, io

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = pd.read_csv('datasets/INFY.csv')
data = data.dropna()
data['Date'] = pd.to_datetime(data["Date"])

sc = MinMaxScaler(feature_range=(0,1))
trainData = data.iloc[:,4:5].values
sc.fit_transform(trainData)

google_model = load_model('google_model.hdf5')
infosys_model = load_model('infosys_model.hdf5')
# google_model = tf.keras.models.load_model('google_model.hdf5')
# infosys_model = tf.keras.models.load_model('infosys_model.hdf5')


price_filter = {
    'Today': -2,
    'Week': -7,
    # 'Month': -30
}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



@app.route('/getStockInfo', methods=['GET'])
@cross_origin()
def index():
    global data
    code = request.args.get('code')
    filter = request.args.get('filter')

    if (code != 'infosys'):
        return jsonify({'status': 'ERROR', 'msg': 'Model not trained yet!!!'})

    last60 = data['Close'][-60:].values
    last60 = last60.reshape((60, 1))
    last60 = sc.transform(last60)
    last60 = last60.reshape((1, 60, 1))
    predicted = infosys_model.predict(last60)
    predicted = sc.inverse_transform(predicted)[0, 0]

    print(predicted)
    
    prices = []
    if filter != 'Month':
        prices = data['Close'][price_filter[filter]:].values
    else:
        prices = []

    # return jsonify({'status': 'SUCCESS', 'result': []})
    return json.dumps({'status': 'SUCCESS', 'result': {'name': code, 'predicted': predicted.item(), 'prices': prices}}, cls=NumpyEncoder)
    # return jsonify({'status': 'SUCCESS', 'result': {'name': code, 'predicted': str(predicted), 'prices': json.dumps(prices, cls=NumpyEncoder)}})



@app.route('/getMonthlyReport', methods=['GET'])
@cross_origin()
def getMonthlyReport():
    global data
    fromDate = request.args.get('from')
    toDate = request.args.get('to')

    dateFormat = '%Y-%m-%d'
    fromDate = datetime.strptime(fromDate, dateFormat)
    toDate = datetime.strptime(toDate, dateFormat)

    lastDate = pd.to_datetime(toDate, format=dateFormat) + MonthEnd(0)
    toDateIsLast = toDate == lastDate
    # print(toDate - fromDate)

    filteredData = data[(data['Date'] >= fromDate) & (data['Date'] <= toDate)]
    filteredDataList = filteredData['Close'].values.tolist()

    start = filteredData.index[0] - 61
    end = start+60

    pastvalues = data['Close'][start:end].values.tolist()
    predicted_list = []

    days_to_pred = (toDate - fromDate).days
    for i in range(len(filteredDataList)):
        # consider only last 60 values
        pastvalues = pastvalues[-60 : ]

        # convert to numpy array
        pastarr = np.array(pastvalues)

        reshaped = pastarr.reshape((60, 1))
        transformed = sc.transform(reshaped)
        reshaped2 = transformed.reshape((1, 60, 1))

        # print(reshaped2.shape)

        predicted = infosys_model.predict(reshaped2, verbose=0)
        predicted = sc.inverse_transform(predicted)[0, 0]
        predicted_list.append(predicted)

        pastvalues.append(filteredDataList[i])
    
    table = {
        'Date': filteredData['Date'].astype(str),
        'Actual': filteredData['Close'].values,
        'Predicted': predicted_list
    }
    tmp = pd.DataFrame(table)

    # tmp.to_excel('Report/report.xlsx')
    # print('File written success')
    # print(predicted_list)
    # return json.dumps({'status': 'SUCCESS'})
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

    tmp.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()

    r = make_response(out.getvalue())
    
    fromDate = fromDate.strftime('%d-%m-%Y')
    toDate = toDate.strftime('%d-%m-%Y')
    r.headers["Content-Disposition"] = f"attachment; filename=Prediction-Report-{fromDate}-to-{toDate}.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    
    # Finally return response
    return r


if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
