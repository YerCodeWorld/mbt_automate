
# USED IN STEP 1
def get_columns(data: str):
    """
    The way I removed the header was splitting by new lines a returning the joint of the rest of indexes.
    There's probably a better way to do that.
    :param data:
    :return: removed header
    """
    data = data.split("\n")
    header = data[0].split(",")
    # We also return the length of the splitted header to know how many commas are necessary to identify split points
    return (len(header), header), "\n".join(data[1:])

# USED IN STEP 2
def get_company(data: [], company_index: int) -> (str, list[str]):
    """
    Only thing we are doing here is determining the company based on the information we get in the company colum.
    We then return the data that we take advantage of the split call from
    :param data:
    :param company_index:
    :return:
    """
    company_data: str = data.strip().split("\n")
    return company_data[0].split(",")[company_index], company_data

# USED IN STEP 2
def get_services(data: {}, valid_data):

    def separate_by_type(info, mode):
        return ",".join([col for i, col in enumerate(info) if i in mode])

    arrivals, departures = [], []
    # Every row is equal to a transportation service. It is a string right now. The first character determines the type
    # of service since that's the colum we can find it on, although we could add some sort of more solid approach.
    for service in data:
        service_type = service[0]
        service_data = service.split(",")

        if service_type.lower() == "d":
            departures.append(separate_by_type(service_data, valid_data["departures"]))
        else:
            arrivals.append(separate_by_type(service_data, valid_data["arrivals"]))

    return "\n".join(arrivals), "\n".join(departures)

# USED IN STEP TWO FROM MAIN FUNCTION
def get_valid_indexes(header):
    # We will make these below be taken from the JSON config file
    valid_a, valid_d = ["Cliente", "Pickup", "Vuelo", "Pax", "Hacia"], ["Cliente", "Pickup", "Pax", "Desde"]

    data = {
        "arrivals": [],
        "departures": [],
        "company": int
    }

    for i, colum in enumerate(header):
        if colum in valid_d:
            data["departures"].append(i)

        if colum in valid_a:
            data["arrivals"].append(i)

        if colum.lower() == "comp":
            data["company"] = i

    return data

