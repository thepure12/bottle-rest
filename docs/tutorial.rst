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

HTTP Methods
------------
Bottle-REST is built on Bottle's request routing. Each resources gives you access
to the get(), post(), put(), delete() decorators by defining the methods in your resource.

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

| `Raw <https://raw.githubusercontent.com/thepure12/bottle-rest/main/examples/routing/app.py>`_

Using curl to test:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food \
    > --header "Content-group: application/json" \
    > --data '{"name":"carrot"}'
    {"name": "carrot"]}
    $ curl http://127.0.0.1:8080/food
    {"food":["carrot"]}

Endpoints
---------
Resources can also handle multiple URLs. Pass multiple URLs into the addResource() method and
each will be routed to your resource.

.. code-block:: python

    api.addResource(Food, "/food", "/foods")

.. code-block:: bash
    
    $ curl http://127.0.0.1:8080/food
    {"food":[]}
    $ curl http://127.0.0.1:8080/foods
    {"food":[]}

Resources also handle Bottle's dynamic routes. These are routes that contain *wildcards*, where a wildcard  is:
"name enclosed in angle brackets (e.g. ``<name>``) and accepts one or more characters up to the next slash (/)".
Each wildcard is passed in as a keyword argument to the Resource method that the request routes to.

| See Bottle's `Dynamic Routes <https://bottlepy.org/docs/dev/tutorial.html#dynamic-routes>`_ 

.. code-block:: python

    class Food(Resource):
        def get(self, name):
            return {"food": name}

    api.addResource(Food, "/food", "/food/<name>")

.. code-block:: bash
    
    $ curl http://127.0.0.1:8080/food/carrot
    {"name": "carrot"}
    
Data Validation
---------------
TODO

.. code-block:: python

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

TODO

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food
    {"food":{"carrot":{"group":"vegetable"}}}

    # Get food named carrot
    $ curl http://127.0.0.1:8080/food/carrot 
    {"carrot":{"group":"vegetable"}}

    # Add food named candy with default group
    $ curl http://127.0.0.1:8080/food \
    > --header "Content-group: application/json" \
    > --data '{"name":"candy"}'
    {"candy":{"group":"junk"}}

    # Add food named apple with group fruit
    $ curl http://127.0.0.1:8080/food \
    > --header "Content-group: application/json" \
    > --data '{"name":"apple", "group": "fruit"}'
    {"apple":{"group":"fruit"}}

    # Add food without a name
    $ curl http://127.0.0.1:8080/food \
    > --header "Content-Type: application/json" \
    > --data '{"group":"fruit"}'
    {"name":"This feild is is required"}

    # Update carrot group
    $ curl http://127.0.0.1:8080/food/carrot \
    > --header "Content-group: application/json" \
    > --data '{"group":"veggie"}'
    {"carrot":{"group":"veggie"}}

    $ curl http://127.0.0.1:8080/food
    {
        "food": {
            "carrot":{"group":"veggie"},
            "candy":{"group":"junk"},
            "apple":{"group":"fruit"}
        }
    }

URL Params
--------------
TODO

.. code-block:: python

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

TODO

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food
    {"food":{"carrot":{"group":"vegetable"},"squash":{"group":"vegetable"},"apple":{"group":"fruit"},"orange":{"group":"fruit"}}}
    $ curl http://127.0.0.1:8080/food?group=fruit
    {"apple":{"group":"fruit"},"orange":{"group":"fruit"}}
