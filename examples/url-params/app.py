from bottle import Bottle
from bottle_rest import API, Resource

app = Bottle()
api = API()
app.install(api)

food = {
    "carrot": {"group": "vegetable"},
    "squash": {"group": "vegetable"},
    "apple": {"group": "fruit"},
    "orange": {"group": "fruit"}
}

class Food(Resource):
    def get(self):
        if "group" in self.params:
            group = self.params["group"]
            return {n: f for n, f in food.items() if f["group"] == group}
        return {"food": food}

api.addResource(Food, '/food')

if __name__ == '__main__':
    app.run(debug=True)