from bottle import Bottle
from bottle_rest import API, Resource

app = Bottle()
api = API()
app.install(api)

food = {
    "carrot": {"type": "vegetable"},
    "squash": {"type": "vegetable"},
    "apple": {"type": "fruit"},
    "orange": {"type": "fruit"}
}

class Food(Resource):
    def get(self):
        if "type" in self.params:
            type = self.params["type"]
            return {n: f for n, f in food.items() if f["type"] == type}
        return {"food": food}

api.addResource(Food, '/food')

if __name__ == '__main__':
    app.run(debug=True)