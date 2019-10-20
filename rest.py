from flask import Flask
import facial_recognition
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin 
import facial_recognition
app = Flask(__name__)
CORS(app) 
api = Api(app)

#port = int(os.getenv('PORT', 8080)) 
@app.route('/',methods = ['GET','POST'])
def get(self):
    if request.method == 'POST':
        data=request.form.get('text')
        facial_recognition()
        if data == 'check':
            result = facial_recognition.check()
            print(result)
        if data == 'add embeddings':
            dat = request.form.get('which addition?')
            if dat == 'visitor':
                facial_recognition.add_visitor_embedding()
                print('done!')
            elif dat == 'member':
                facial_recognition.add_member_embedding()
                print('done!')
            else:
                None
                print('Not Allowed!')
        
    return {'data': result}

    
if __name__ == '__main__': 
    app.run() # deploy with debug=False

