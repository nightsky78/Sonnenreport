import data_request
import json
import config

# get the URL from the config file
url = config.get_url()

# get the data
# loads function converts JSON-formatted string into a Python dictionary object. The name "loads" stands for "load string", indicating that the function operates on a string rather than a file.
data = json.loads(data_request.get_data(url))

print(data["Apparent_output"])