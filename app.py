from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS
import os.path
import pickle
import pandas as pd

from routinghelp import getstartpincode
from routinghelp import getaddress
from routinghelp import getpath
from prediction import getPredictions

app = Flask(__name__)
CORS(app)

@app.route('/update', methods=['POST'])
def updateweights():
    try:
        data = request.json
        newWeight=data
        with open('./storage/weight.pkl', 'rb') as f:
            listData = pickle.load(f)
            oldWeight=listData[0]
            oldCount=listData[1]
        
        oldWeight = {key: (value *oldCount) for key, value in oldWeight.items()}
        
        for key, new_value in newWeight.items():
            key=int(key)
            if key in oldWeight:
                oldWeight[key] = oldWeight[key] + new_value
            else:
                print("issues")
        oldWeight = {key: (value / (oldCount+1)) for key, value in oldWeight.items()}
        # print(sum(oldWeight.values()))
        with open('./storage/weight.pkl', 'wb') as f:
            pickle.dump([oldWeight,oldCount+1], f)
        return "SUCCESS"
    except:
        return "FAILURE"


@app.route('/globalmodelstatus', methods=['GET'])
def getglobalmodelstatus():
    if(os.path.isfile("./nextpredict.csv")):
        print("hello")
        timeModified = os.path.getmtime("./nextpredict.csv")
        modificationDatetime = datetime.fromtimestamp(timeModified)
        formattedDatetime = modificationDatetime.strftime('%Y-%m-%d %H:%M:%S')
        return formattedDatetime
    else:
        return "2024-04-29 01:30:23"
    

@app.route('/predict', methods=['GET'])
def predict():
    try:
        getPredictions()
        return "SUCCESS"
    except:
        return "FAILURE"



@app.route('/routes', methods=['POST'])
def getroutes():
    try:
        Days=['Monday','Tuesday','Wednesday','Thursday','Friday']
        routes={}
        data = request.json
        area=str(data['area']).replace(" ","")
        print(area)
        capacity=(data['capacity'])
        areapincodes=getstartpincode(area)


        for day in Days:
            dayRoute=[]
            for i in range(4):
                timeDetails={}
                startPoint=areapincodes[i]
                endPoint=areapincodes[3-i]

                timeDetails['StartPoint']=getaddress(str(startPoint))
                timeDetails['EndPoint']=getaddress(str(endPoint))
                timeDetails['PeopleCount']=50

                timeDetails['Stops']=[timeDetails['StartPoint']]
                path=getpath(timeDetails['StartPoint'],timeDetails['EndPoint'])
                for eachpath in path:
                    timeDetails['Stops'].append(eachpath)
                timeDetails['Stops'].append(timeDetails['EndPoint'])
                dayRoute.append(timeDetails)
            routes[day]=dayRoute
        return jsonify(routes)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal Server Error'}), 500
    


if __name__ == '__main__':
    if(os.path.isfile("./storage/weight.pkl")):
        pass
    else:
        df = pd.read_csv("bayareapincodes.csv")
        zip_codes = df['ZipCodes'].unique()
        equal_percentage = 100 / len(zip_codes)
        zip_percentages = {zip_code: equal_percentage for zip_code in zip_codes}
        with open('./storage/weight.pkl', 'wb') as f:
            pickle.dump([zip_percentages,1], f)
        print(zip_percentages)
    app.run(host='0.0.0.0',port=8000, debug=True)
