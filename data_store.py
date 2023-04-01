import data_request
import json
import config
import db_handler
import time
import logging

# first set the log level
logging.basicConfig(level=logging.DEBUG)

# get the URL from the config file
url = config.get_url()

# get the data
# loads function converts JSON-formatted string into a Python dictionary object. The 
# name "loads" stands for "load string", indicating that the function operates on a string rather than a file.

while True:
        try:
            data = json.loads(data_request.get_data(url))
        except:
              logging.critical('Data request failed')

        logging.debug(f" The return data is: {data['Apparent_output']}, {data['BatteryCharging']}, {data['BatteryDischarging']}, {data['GridFeedIn_W']}, {data['Consumption_Avg']}, {data['Consumption_W']}, {data['Production_W']}, {data['USOC']}, {data['Timestamp']}, {data['RemainingCapacity_Wh']}")


        # now we need to store the data in the DB
        try:
              db = db_handler.Database('sonnen_data.db')
        except:
              logging.critical(' Data request failed.')

        
        try:
              db.insert_dataset(data["Apparent_output"], data["BatteryCharging"], data["BatteryDischarging"], 
                        data["GridFeedIn_W"], data["Consumption_Avg"], data["Consumption_W"], 
                        data["Production_W"], data["USOC"], data["Timestamp"], data["RemainingCapacity_Wh"] )
        except:
              logging.critical(" Data Insert failed.")
        
        time.sleep(10)


