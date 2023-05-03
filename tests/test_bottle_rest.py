import unittest
from bottle import Bottle, debug
from src.bottle_rest import API, Resource
from webtest import TestApp, TestResponse

DEBUG = False

class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.bottle_app = Bottle()
        debug(DEBUG)
        self.api = API(debug=DEBUG)
        self.bottle_app.install(self.api)
        self.app = TestApp(self.bottle_app)

    def testInstall(self):
        # Installing in setup, every test should fail if this one fails
        pass

    def testAddResourceToAPI(self):
        class Food(Resource):
            pass
        self.api.addResource(Food, "/food")

    def testGetResource(self):
        class Food(Resource):
            def get(self):
                pass
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.get("/food")
        self.assertEqual(res.status_code, 200)

    def testPostResource(self):
        class Food(Resource):
            def post(self):
                pass
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.post("/food")
        self.assertEqual(res.status_code, 200)

    def testPutResource(self):
        class Food(Resource):
            def put(self):
                pass
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.put("/food")
        self.assertEqual(res.status_code, 200)

    def testDeleteResource(self):
        class Food(Resource):
            def delete(self):
                pass
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.delete("/food")
        self.assertEqual(res.status_code, 200)

    def testJSONRequest(self):
        class Food(Resource):
            test = self
            def post(self, food):
                self.test.assertEqual(food, "carrot")
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.post_json("/food", {"food": "carrot"})
        self.assertEqual(res.status_code, 200)

    def testJSONReqMissingField(self):
        class Food(Resource):
            test = self
            def post(self, food):
                self.test.assertEqual(food, "carrot")
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.post_json("/food", {}, expect_errors=True)
        self.assertEqual(res.status_code, 400)
        self.assertIn("food", res.json)

    def testJSONReqOptionField(self):
        class Food(Resource):
            test = self
            def post(self, food=None):
                if food:
                    self.test.assertEqual(food, "carrot")
                else:
                    self.test.assertEqual(food, None)
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.post_json("/food", {"food": "carrot"})
        self.assertEqual(res.status_code, 200)
        res: TestResponse = self.app.post_json("/food", {})
        self.assertEqual(res.status_code, 200)

    def testParamsRequest(self):
        class Food(Resource):
            test = self
            def get(self):
                self.test.assertEqual(self.params["type"], "fruit")
        self.api.addResource(Food, "/food")
        res: TestResponse = self.app.get("/food", params={"type": "fruit"})
        self.assertEqual(res.status_code, 200)

    def testRouteVariable(self):
        class Food(Resource):
            test = self
            def get(self, name):
                self.test.assertEqual(name, "apple")
        self.api.addResource(Food, "/food/<name>")
        res: TestResponse = self.app.get("/food/apple")
        self.assertEqual(res.status_code, 200)

    def testRouteVarMissing(self):
        class Food(Resource):
            test = self
            def get(self, name):
                self.test.assertEqual(name, "apple")
        self.api.addResource(Food, "/food", "/food/<name>")
        res: TestResponse = self.app.get("/food", expect_errors=True)
        self.assertEqual(res.status_code, 400)
        self.assertIn("name", res.json)