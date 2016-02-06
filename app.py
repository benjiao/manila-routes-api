from flask import Flask
from flask import make_response
from flask_restful import Resource, Api
from flask.ext.pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'manila_routesdb'

api = Api(app)
mongo = PyMongo(app)


def get_shapes(shape_id):
    shapes = mongo.db.shapes.find({"shape_id", shape_id})
    return [shape for shape in shapes]


def get_route_trips(route_id):
    trips = mongo.db.trips.find({'route_id': route_id})
    trips_list = []

    if trips is not None:
        for trip in trips:
            if trip.get('shape_id') != "":
                trips_list.append({
                    'trip_id': trip.get('trip_id'),
                    'shape': trip.get('shape')
                })

    return trips_list


class Routes(Resource):
    def get(self):
        routes = mongo.db.routes.find()

        response_content = []
        for route in routes:
            trips = get_route_trips(route.get("route_id"))
            if len(trips) > 0:
                response_content.append({
                    'route_id': route.get('route_id'),
                    'name': route.get('route_long_name'),
                    'agency_id': route.get('agency_id'),
                    'trips': trips
                })

        return response_content


class RoutesItem(Resource):
    def get(self, route_id):
        route = mongo.db.routes.find_one({'route_id': route_id})
        trips = get_route_trips(route.get("route_id"))

        response = {
            'route_id': route.get('route_id'),
            'name': route.get('route_long_name'),
            'agency_id': route.get('agency_id'),
            'trips': trips
        }
        return response


api.add_resource(Routes, '/routes')
api.add_resource(RoutesItem, '/routes/<string:route_id>')

if __name__ == '__main__':
    app.run(debug=True)
