import db_handler
import logging
import calculation
from datetime import datetime

def aggregate_data():

    db = db_handler.Database('sonnen_data.db')

    data = db.select_all()

    cal_cons = calculation.Calculator(data, 0)

    daily_values = cal_cons.perdaydata()

    for index, row in daily_values.iterrows():
        consumption = round(row['consumption_avg_time_diff'] / 1000, 3)
        grid_cons = round(row['grid_cons_time_diff'] / 1000, 3)
        production = round(row['production_time_diff'] / 1000, 3)
        grid_feed = round(row['grid_feed_time_diff'] / 1000, 3)
        timestamp = index.strftime('%Y-%m-%dT%H:%M')
        db.insert_data(consumption, round(consumption - grid_cons, 3), production, grid_feed, timestamp, 'A')