from bottle import Bottle
from bottle_rest import API, Resource

app = Bottle()
api = API()
app.install(api)

class HelloWorld(Resource):
    def get(self):
        return {'msg': 'hello world'}

api.addResource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)