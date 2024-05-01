from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/globalmodelstatus', methods=['GET'])
def getglobalmodelstatus():
    return "2024-04-29 01:30:23"
    performers={}
    return jsonify(performers)



@app.route('/routes', methods=['POST'])
def getroutes():
    try:
        Days=['Monday','Tuesday','Wednesday','Thursday','Friday']
        routes={}
        data = request.json
        for day in Days:
            dayRoute=[]

            for i in range(1,23,10):
                timeDetails={}
                timeDetails['StartPoint']=("ABC","37.350167","-121.923513")
                timeDetails['EndPoint']=("DEF","37.322546","-122.031882")
                timeDetails['Time']=str(i)+":23"
                timeDetails['PeopleCount']=50
                timeDetails['Stops']=[("ABC","37.350167","-121.923513"),("XYZ","37.331077","-121.997805"),("qwe","37.334693","-121.988087"),("DEF","37.322546","-122.031882")]
                dayRoute.append(timeDetails)

            routes[day]=dayRoute
        print(data)
        return jsonify(routes)
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
