import csv
from pymongo import MongoClient


def get_routes():
    with open('gtfs/routes.txt', 'rb') as f:
        routes = csv.DictReader(f, delimiter=',', quotechar='"')
        return [route for route in routes]


def get_stops():
    with open('gtfs/stops.txt', 'rb') as f:
        stops = csv.DictReader(f, delimiter=',', quotechar='"')
        return [stop for stop in stops]


def get_trips():
    with open('gtfs/trips.txt', 'rb') as f:
        trips = csv.DictReader(f, delimiter=',', quotechar='"')
        return [trip for trip in trips]


def get_shapes():
    with open('gtfs/shapes.txt', 'rb') as f:
        shapes = csv.DictReader(f, delimiter=',', quotechar='"')
        return [shape for shape in shapes]

if __name__ == '__main__':
    routes = get_routes()
    stops = get_stops()
    trips = get_trips()
    shapes = get_shapes()

    db = MongoClient().manila_routesdb

    # Clear DB
    db.routes.remove()
    db.stops.remove()
    db.trips.remove()
    db.shapes.remove()

    # Load Routes and Stops
    for route in routes:
        print "Route: %s" % route.get('route_id')
        db.routes.insert_one(route)

    for stop in stops:
        print "Stop: %s Route: %s" % (stop.get('stop_id'), stop.get('route_id'))
        db.stops.insert_one(stop)

    for shape in shapes:
        print "Shape ID: %s" % (shape.get('shape_id'))
        db.shapes.insert_one(shape)

    for trip in trips:
        if trip.get('shape_id') != "":
            print "Trip ID: %s Shape ID: %s" % (trip.get('trip_id'), trip.get('shape_id'))
            shape_points = db.shapes.find({'shape_id': trip.get('shape_id')}, projection={'_id': False})

            point_list = []
            for s in shapes:
                point_list.append({
                    'seq': s['shape_pt_sequence'],
                    'lat': s['shape_pt_lat'],
                    'lng': s['shape_pt_lon']
                })

            trip['shape'] = point_list
            db.trips.insert_one(trip)
