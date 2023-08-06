from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic


class Helper:
    @staticmethod
    def calc_time(point_a, point_b, appt_time=10, buffer=0):
        distance = round(geodesic(point_a, point_b).miles)
        # Assuming each mile takes only 6 mins
        return distance * 6 + buffer + appt_time

    @staticmethod
    def get_time(person_i, person_j, buffer):
        if person_i['type'] == 'Doctor' and person_j['type'] == 'Doctor':
            return 0
        if person_i['type'] == 'Doctor':
            if person_j.get('department') not in person_i.get('speciality'):
                return 1000
        return Helper.calc_time(person_i['location'], person_j['location'], person_j.get('appt_duration') or person_i.get('appt_duration'), buffer)



class Scheduler:
    def __init__(self, doctors: list, patients: list, buffer: int = 10):
        super().__init__()
        self.sanity_check(doctors, patients)
        self.doctors = doctors
        self.patients = patients
        self.buffer = buffer
        self.distances = []
        self.travel_times = []
        self.people_dict = {}
        total_people = len(doctors) + len(patients)
        for i in range(total_people):
            self.travel_times.append([0] * total_people)

    def verify_geo_coordinates(self, geocode):
        lat, lon = geocode
        if lat < -90 or lat > 90:
            raise Exception(
                'ValueError', 'Latitude must be between -90 and 90')
        if lon < -180 or lon > 180:
            raise Exception(
                'ValueError', 'Longitude must be between -180 and 180')

    def sanity_check(self, doctors: list, patients: list):
        if len(doctors) == 0:
            raise Exception('ValueError', 'Min 1 doctor needs to be present')
        if len(patients) == 0:
            raise Exception('ValueError', 'Min 1 patient needs to be present')
        
        for patient in patients:
            if patient.get('department') == None:
                raise Exception('ValueError', 'Appointment must belong to one predefined department')

        for doctor in doctors:
            if doctor.get('location') == None:
                raise Exception(
                    'ValueError', 'Doctor location must be present')
            if doctor.get('speciality') == None or len(doctor.get('speciality')) == 0:
                raise Exception(
                    'ValueError', 'Doctor speciality cannot be empty and must be present')
            self.verify_geo_coordinates(doctor.get('location'))

        for patient in patients:
            if patient.get('location') == None:
                raise Exception(
                    'ValueError', 'Patient location must be present')
            self.verify_geo_coordinates(patient.get('location'))

    def calc_distances(self):
        # self.distances = [[0] * (len(self.doctors) + len(self.patients) + 1)]
        self.distances = []
        total_people = [{'type': 'Doctor', 'logical_id': person['id'], 'location': person['location'], 'speciality': person['speciality']}
                        for person in self.doctors]
        total_people = total_people + [{'type': 'Patient', 'logical_id': person['id'], 'location': person['location'], 'appt_duration': person['appt_duration'], 'department': person['department']}
                                       for person in self.patients]
        
        self.people_dict = {i: person for i, person in enumerate(total_people)}

        for i, person_i in enumerate(total_people):
            distance_person_i = []
            for j, person_j in enumerate(total_people):
                time = Helper.get_time(person_i, person_j, self.buffer)
                appt_time = 0 if person_i['type'] == 'Doctor' and person_j['type'] == 'Doctor' else (person_j.get('appt_duration') or person_i.get('appt_duration')) - self.buffer
                self.travel_times[i][j] = time - appt_time
                distance_person_i.append(time)
            self.distances.append(distance_person_i)

    def get_solution(self, data, manager, routing, solution):
        """Prints solution on console."""
        routes = []
        max_route_distance = 0
        for doctor in range(data['doctors']):
            index = routing.Start(doctor)
            route = []
            plan_output = 'Time for doctor {}:\n'.format(doctor)
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                route.append(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, doctor)
            route.append(manager.IndexToNode(index))
            routes.append(route)
            plan_output += '{}\n'.format(manager.IndexToNode(index))
            plan_output += 'Time of the route: {} mins\n'.format(
                route_distance)
            # print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        # print('Maximum of the route time: {} mins'.format(max_route_distance))
        return routes

    def create_model_data(self):
        self.calc_distances()
        data = {}
        data['distance_matrix'] = self.distances
        data['doctors'] = len(self.doctors)
        data['starts'] = [x for x in range(len(self.doctors))]
        data['ends'] = [x for x in range(len(self.doctors))]
        return data


    def generate_route(self, routes):
        travel_routes = []
        for route in routes:
            travel_route = []
            prev = None
            for route_id in route:
                person = self.people_dict.get(route_id)
                if prev == None:
                    prev = route_id
                    travel_route.append({
                        'type': person['type'],
                        'id': person['logical_id'],
                        'travel_time': 0,
                        'buffer': 0,
                        'appt_duration': 0
                    })
                else:
                    if person['type'] == 'Patient':
                        travel_route.append({
                            'type': person['type'],
                            'id': person['logical_id'],
                            'travel_time': self.travel_times[prev][route_id],
                            'buffer': self.buffer,
                            'appt_duration': self.people_dict[route_id]['appt_duration']
                        })
                    else:
                        travel_route.append({
                            'type': person['type'],
                            'id': person['logical_id'],
                            'travel_time': self.travel_times[prev][route_id],
                            'buffer': 0,
                            'appt_duration': 0
                        })
                    prev = route_id
            travel_routes.append(travel_route)
        return travel_routes

    def run(self):
        data = self.create_model_data()
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['doctors'], data['starts'],
                                               data['ends'])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Time as constraint.
        dimension_name = 'Time'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            540,  # vehicle maximum travel time 9 hrs in a day
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            routes = self.get_solution(data, manager, routing, solution)
            travel_routes = self.generate_route(routes)
            return travel_routes