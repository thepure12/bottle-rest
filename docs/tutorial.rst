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

Save this to a file called app.py and run it.