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

Using curl to test:

.. code-block:: bash

    $ curl http://127.0.0.1:8080/food \
    > --header "Content-Type: application/json" \
    > --data '{"name":"carrot"}'
    {"name":["carrot","carrot"]}

    $ curl http://127.0.0.1:8080/food
    {"food":["carrot","carrot"]}