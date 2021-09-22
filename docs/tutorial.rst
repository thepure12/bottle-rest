========
Tutorial
========
TODO

Installation
------------
Bottle-REST is not dependant on external library other than `Bottle <https://bottlepy.org/>`_. Download 
`bottle_rest.py <https://raw.githubusercontent.com/thepure12/bottle-rest/main/bottle_rest.py>`_ 
and `bottle.py <https://bottlepy.org/bottle.py>`_ (if you don't already have it) into your project directory.

.. code-block:: bash
    
    $ wget https://bottlepy.org/bottle.py
    $ wget https://raw.githubusercontent.com/thepure12/bottle-rest/main/bottle_rest.py

Quickstart
----------
Once you have both Bottle and Bottle-REST installed, we can create a basic API.

.. code-block:: python

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

Save this to a file called app.py (or 
`download <https://raw.githubusercontent.com/thepure12/bottle-rest/main/examples/hello-world/app.py>`_ it) and run it.

.. code-block::

    $ python app.py
    Bottle v0.13-dev server starting up (using WSGIRefServer())...
    Listening on http://127.0.0.1:8080/
    Hit Ctrl-C to quit.

Using curl to test:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/
    {"msg":"hello world"}

Routing
-------
TODO

.. code-block:: python

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

| `Download <https://raw.githubusercontent.com/thepure12/bottle-rest/main/examples/routing/app.py>`_

Using curl to test:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food \
    > --header "Content-Type: application/json" \
    > --data '{"name":"carrot"}'
    {"name": "carrot"]}
    $ curl http://127.0.0.1:8080/food
    {"food":["carrot"]}

Endpoints
---------
TODO

.. code-block:: python

    api.addResource(Food, "/food", "/foods")

.. code-block:: bash
    
    $ curl http://127.0.0.1:8080/food
    {"food":[]}
    $ curl http://127.0.0.1:8080/foods
    {"food":[]}

TODO

.. code-block:: python

    api.addResource(Food, "/food", "/food/<name>")

.. code-block:: bash
    
    $ curl http://127.0.0.1:8080/food
    {"food":[]}
    $ curl http://127.0.0.1:8080/food/carrot
    {"name": "carrot"}
    
Data Validation
---------------
TODO

.. code-block:: python

    food = {"carrot": {"type": "vegetable"}}

    class Food(Resource):
        def get(self, name=None):
            if name and name in food:
                return {name: food[name]}
            return {"food": food}

        def post(self, name, type="junk"):
            food[name] = {"type": type}
            return {name: {"type": type}}

    api.addResource(Food, '/food', '/food/<name>')

TODO

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food
    {"food":{"carrot":{"type":"vegetable"}}}

    # Get food named carrot
    $ curl http://127.0.0.1:8080/food/carrot 
    {"carrot":{"type":"vegetable"}}

    # Add food named candy with default type
    $ curl http://127.0.0.1:8080/food \
    > --header "Content-Type: application/json" \
    > --data '{"name":"candy"}'
    {"candy":{"type":"junk"}}

    # Add food named apple with type fruit
    $ curl http://127.0.0.1:8080/food \
    > --header "Content-Type: application/json" \
    > --data '{"name":"apple", "type": "fruit"}'
    {"apple":{"type":"fruit"}}

    # Update carrot type
    $ curl http://127.0.0.1:8080/food/carrot \
    > --header "Content-Type: application/json" \
    > --data '{"type":"veggie"}'
    {"carrot":{"type":"veggie"}}

    $ curl http://127.0.0.1:8080/food
    {
        "food": {
            "carrot":{"type":"veggie"},
            "candy":{"type":"junk"},
            "apple":{"type":"fruit"}
        }
    }

URL Params
--------------
TODO

.. code-block:: python

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

TODO

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food
    {"food":{"carrot":{"type":"vegetable"},"squash":{"type":"vegetable"},"apple":{"type":"fruit"},"orange":{"type":"fruit"}}}
    $ curl http://127.0.0.1:8080/food?type=fruit
    {"apple":{"type":"fruit"},"orange":{"type":"fruit"}}
