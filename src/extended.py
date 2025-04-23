"""
Called extended as these are just part of the main core logic.
Only that separated for better maintainability, and also because these are like
helper functions for the actual process.
"""

def remove_tildes():
    pass

# USED IN STEP 2
def get_services(data: {}, valid_data):

    # I dont like how these nested functions look in here but whatever
    def get_edge_cases(col: str):
        # TODO: Add logic to dynamically add/remove edge cases
        # they could be stored in the JSON config file
        edge_cases = {
            "punta cana": "puj",
            "hotel & casino": "puj",
            "hotel": "",
            "paradisus": "paradisus to puj",
            "meliá": "melia caribe beach to puj"
        }
        for edge_case in edge_cases.keys():
            if edge_case in col.lower():
                col = col.lower().replace(edge_case, edge_cases[edge_case]).upper()
        return col

    def separate_by_type(info, valid):
        l = []
        for i, col in enumerate(info):
            if i in valid:
                # These are cases in which the name of the hotel must be something different than what is first written
                # The hotel column is always the last in the mode
                if i == valid[-1]:
                    col = get_edge_cases(col)
                l.append(col)

        return ",".join(l)
        # return ",".join([col for i, col in enumerate(info) if i in mode])

    arrivals, departures = [], []
    # Every row is equal to a transportation service. It is a string right now. The first character determines the type
    # of service since that's the colum we can find it on, although we could add some sort of more solid approach.
    for service in data:
        service_type = service[0]
        service_data = service.split(",")  # It would be nice to add some smart search for extra commas, which ruin our logic

        if service_type.lower() == "d":
            departures.append(separate_by_type(service_data, valid_data["departures"]))
        else:
            arrivals.append(separate_by_type(service_data, valid_data["arrivals"]))

    return "\n".join(arrivals), "\n".join(departures)

# USED IN STEP TWO FROM MAIN FUNCTION
def get_valid_indexes(header):
    # We will make these below be taken from the JSON config file
    valid_a = ["Cliente", "Pickup", "Vuelo", "Pax", "Hacia"]
    valid_d = ["Cliente", "Pickup", "Pax", "Desde"]

    data = {
        "arrivals": [],
        "departures": [],
        "company": int,
        "name": int
    }

    for i, colum in enumerate(header):
        if colum in valid_d:
            data["departures"].append(i)

        if colum in valid_a:
            data["arrivals"].append(i)

        # Get the company index
        if colum.lower() == "comp":
            data["company"] = i

        if colum.lower() == "nombre":
            data["name"] = i

    return data

