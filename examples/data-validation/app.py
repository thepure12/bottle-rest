from bottle import Bottle
from bottle_rest import API, Resource

app = Bottle()
api = API()
app.install(api)

food = {"carrot": {"group": "vegetable"}}

class Food(Resource):
    def get(self, name=None):
        if name and name in food:
            return {name: food[name]}
        return {"food": food}

    def post(self, name, group="junk"):
        food[name] = {"group": group}
        return {name: {"group": group}}

api.addResource(Food, '/food', '/food/<name>')

if __name__ == '__main__':
    app.run(debug=True)