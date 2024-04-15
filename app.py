from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/globalmodelstatus', methods=['GET'])
def getglobalmodelstatus():
    return "1:30"
    performers={}
    return jsonify(performers)



@app.route('/routes', methods=['POST'])
def getroutes():
    try:
        data = request.json
        # selected_stock = data.get('stock')
        return "Okay"
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
