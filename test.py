import db_handler
import logging
import calculation
from datetime import datetime


db = db_handler.Database('sonnen_data.db')

data = db.select_all()

cal_cons = calculation.Calculator(data, 0)

consumption = cal_cons.perdaydata()

print(consumption)