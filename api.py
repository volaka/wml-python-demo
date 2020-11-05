from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from ibm_watson_machine_learning import APIClient
from dotenv import load_dotenv, find_dotenv
from waitress import serve

import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Temperature Guesser',
    description='A simple temperature guesser application which uses watson machine learning service',
)

ns = api.namespace('temp', description='Temperature operations')

temp = api.model('Temp', {
    'id': fields.Integer(readonly=True, description='The tempearture unique identifier'),
    'time': fields.Integer(required=True, description='Request time'),
    'humidity': fields.Integer(required=True, description='Request time'),
    'value': fields.Float(required=True, description='The temperature')
})


class Temp(object):
    def __init__(self):
        self.counter = 0
        self.temps = []

    def get(self, id):
        for temp in self.temps:
            if temp['id'] == id:
                return temp
        api.abort(404, "Temperature {} doesn't exist".format(id))

    def create(self, data):
        temp = data
        temp['id'] = self.counter = self.counter + 1
        scoring_payload = {
            "input_data": [{    
                'fields': ["time","humidity"],
                'values': [[data["time"], data["humidity"]]]}]
        }
        predictions = client.deployments.score(deployment_uid, scoring_payload)
        temp["value"] = predictions["predictions"][0]["values"][0][0]
        self.temps.append(temp)
        return temp

    def update(self, id, data):
        temp = self.get(id)
        temp.update(data)
        return temp

    def delete(self, id):
        temp = self.get(id)
        self.temps.remove(temp)

TEMP = Temp()

@ns.route('/')
class TempList(Resource):
    '''Shows a list of all temperature requests, and lets you POST to request  new temperature'''
    @ns.doc('list_temps')
    @ns.marshal_list_with(temp)
    def get(self):
        '''List all tasks'''
        return TEMP.temps

    @ns.doc('create_temp')
    @ns.expect(temp)
    @ns.marshal_with(temp, code=201)
    def post(self):
        '''Create a new task'''
        #print(api.payload)
        return TEMP.create(api.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Temperature not found')
@ns.param('id', 'The temperature identifier')
class TempResource(Resource):
    '''Show a single temperature item and lets you delete them'''
    @ns.doc('get_temp')
    @ns.marshal_with(temp)
    def get(self, id):
        '''Fetch a given resource'''
        return TEMP.get(id)

    @ns.doc('delete_temp')
    @ns.response(204, 'Temperature deleted')
    def delete(self, id):
        '''Delete a temperature given its identifier'''
        TEMP.delete(id)
        return '', 204

    @ns.expect(temp)
    @ns.marshal_with(temp)
    def put(self, id):
        '''Update a temperature given its identifier'''
        return TEMP.update(id, api.payload)

@ns.route('/healthz')
class Health(Resource):
    '''Returns "OK" when application is ready'''
    @ns.doc('health')
    def get(self):
        '''Return OK'''
        return { 'health': 'OK' }, 200


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    api_key = os.environ.get("APIKEY")
    location = os.environ.get("REGION")

    print(os.environ.get("APIKEY"), os.environ.get("REGION"))

    wml_credentials = {
        "apikey": api_key,
        "url": 'https://' + location + '.ml.cloud.ibm.com'
    }

    client = APIClient(wml_credentials)
    client.set.default_space(os.environ.get("SPACE_UID"))
    deployment_uid=os.environ.get("DEPLOYMENT_UID")
    serve(app, host="0.0.0.0", port=5000)
    #app.run(debug=True, host="0.0.0.0")