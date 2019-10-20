from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin 
import facial_recognition
app = Flask(__name__)
CORS(app) 
api = Api(app)

#port = int(os.getenv('PORT', 8080)) 
class check(Resource):
    def get(self):
        return {'data': facial_recognition.check()}

api.add_resource(check, '/facialrecognition/')
    
if __name__ == '__main__': 
    app.run() # deploy with debug=False

