from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS
from pyzipcode import ZipCodeDatabase


from routinghelp import getstartpincode
from routinghelp import getpincode

app = Flask(__name__)
CORS(app)

@app.route('/globalmodelstatus', methods=['GET'])
def getglobalmodelstatus():
    return "2024-04-29 01:30:23"



@app.route('/routes', methods=['POST'])
def getroutes():
    zcdb = ZipCodeDatabase()
    print(zcdb[getstartpincode()].latitude)
    try:
        Days=['Monday','Tuesday','Wednesday','Thursday','Friday']
        routes={}
        data = request.json
        area=str(data['name'])
        print(data['capacity'])
        areapincodes=getpincode(area)
        startPoint=areapincodes[0]
        startPointLat=zcdb[startPoint].latitude
        startPointLong=zcdb[startPoint].longitude
        
        endPoint=areapincodes[-1]
        endPointLat=zcdb[endPoint].latitude
        endPointLong=zcdb[endPoint].longitude
        for day in Days:
            dayRoute=[]
            for i in range(1,23,10):
                timeDetails={}
                timeDetails['StartPoint']=(str(startPoint),str(startPointLat),str(startPointLong))
                timeDetails['EndPoint']=(str(endPoint),str(endPointLat),str(endPointLong))
                timeDetails['Time']=str(i)+":23"
                timeDetails['PeopleCount']=50
                timeDetails['Stops']=[timeDetails['StartPoint'],("XYZ","37.331077","-121.997805"),("qwe","37.334693","-121.988087"),timeDetails['EndPoint']]
                dayRoute.append(timeDetails)
            routes[day]=dayRoute
        return jsonify(routes)
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
