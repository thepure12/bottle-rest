from bottle import Bottle, run
from bottle_rest import API, Resource

local = True
debug = True
app = Bottle()
api = API(debug)
app.install(api)

class Foods(Resource):
     
    def __init__(self) -> None:
        self.foods = [
            {"name": "apple", "type": "fruit"},
            {"name": "carrot", "type": "vegetable"},
            {"name": "steak", "type": "meat"},
            {"name": "chicken", "type": "meat"}
        ]

    def get(self, name=None):
        if debug:
            print(f"Get {name if name else 'all food'}")
            print(f"Filter by {list(self.params.items())}")
        if name:
            return next(food for food in self.foods if food["name"] == name)
        if "type" in self.params:
            return {"foods": [food for food in self.foods if food["type"] == self.params["type"]]}
        return {"foods": self.foods}

    def post(self, name, type):
        if [food for food in self.foods if food["name"] == name]:
            return {"message": f"{name} already exists"}
        self.foods.append({
            "name": name,
            "type": type
        })
        return {"message": f"Added food {name}"}


# Routes
api.addResource(Foods, "/foods", "/foods/<name>")

# Run
if local:
    run(app=app, host="0.0.0.0", port="8080", reloader=True, debug=debug)
else:
    application = app
