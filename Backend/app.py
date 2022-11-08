
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
# from markupsafe import escape
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


google_model = tf.keras.models.load_model('google_model.hdf5')
infosys_model = tf.keras.models.load_model('infosys_model.hdf5')


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
    code = request.args.get('code')
    filter = request.args.get('filter')

    if (code != 'infosys'):
        return jsonify({'status': 'ERROR', 'msg': 'Model not trained yet!!!'})

    data = pd.read_csv('datasets/INFY.csv')
    data = data.dropna()
    # train, _ = train_test_split(data, test_size=0.1, shuffle=False)
    trainData = data.iloc[:,4:5].values
    sc = MinMaxScaler(feature_range=(0,1))
    sc.fit_transform(trainData)
    last60 = data['Close'][-60:].values
    last60 = last60.reshape((1, 60, 1))
    last60.shape
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


if __name__ == '__main__':
    app.debug = True
    app.run() #go to http://localhost:5000/ to view the page.
