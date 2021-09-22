from bottle import Bottle
from bottle_rest import API, Resource

app = Bottle()
api = API()
app.install(api)

food = []

class Food(Resource):
    def get(self):
        return {"food": food}

    def post(self, name):
        food.append(name)
        return {"name": food}

api.addResource(Food, '/food')

if __name__ == '__main__':
    app.run(debug=True)