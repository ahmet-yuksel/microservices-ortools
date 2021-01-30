from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def get_optimal_routes(data):
    try:

        vehicle_loc = list(set([input["start_index"] for input in data.vehicles]))
        manager = pywrapcp.RoutingIndexManager(len(data.matrix),len(data.vehicles), vehicle_loc, vehicle_loc)

        # [END index_manager]

        # Create Routing Model.
        # [START routing_model]
        routing = pywrapcp.RoutingModel(manager)

        # [END routing_model]

        # Create and register a transit callback.
        # [START transit_callback]
        def duration_callback(from_index, to_index):

            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data.matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(duration_callback)
        # [END transit_callback]

        # Define cost of each arc.
        # [START arc_cost]
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # [END arc_cost]


        # [START duration_constraint]
        dimension_name = 'Time'
        routing.AddDimension(
            transit_callback_index,
            1,  # no slack
            100000,  # vehicle maximum travel duration
            True,  # start cumul to zero
            dimension_name)
        duration_dimension = routing.GetDimensionOrDie(dimension_name)
        duration_dimension.SetGlobalSpanCostCoefficient(100)
        # [END duration]


        # [START search parameters]
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
        # [END parameters]

        # Solve the problem.
        # [START solve]
        solution = routing.SolveWithParameters(search_parameters)
        # [END solve]

        # [START prepare_response]
        if solution:
            return prepare_response(data, manager, routing, solution)

        return {'ResponseCode': -4, 'ResponseMessage': 'solution not found'}
    except:
        return {'ResponseCode': -5, 'ResponseMessage': 'unexpected error'}
    # [END get_optimal_routes]


def prepare_response(data, manager, routing, solution):

    sum_route_duration = 0
    newdict = {}

    for vehicle_start_index in range(len(data.vehicles)):
        index = routing.Start(vehicle_start_index)
        route_duration = 0
        route_list = []
        while not routing.IsEnd(index):
            if vehicle_start_index != manager.IndexToNode(index):
                job_id = [x for x in data.jobs if x['location_index'] == manager.IndexToNode(index)][0]
                route_list.append(job_id["id"])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_duration += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_start_index)

        vehicle_id = [x for x in data.vehicles if x['start_index'] == vehicle_start_index][0]
        newdict[vehicle_id["id"]] = route_list
        sum_route_duration = route_duration + sum_route_duration
    return {'ResponseCode': 0, 'total_delivery_duration': sum_route_duration, 'optimal_routes': newdict}

    # [END prepare_response]
