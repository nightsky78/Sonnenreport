from flask import Flask, render_template, request, redirect, url_for
import db_handler
import logging
import calculation
from datetime import datetime
import aggregate
import pandas as pd

# first set the log level
logging.basicConfig(level=logging.DEBUG)

# take the latest data and aggregate it. Later we make a button out of this. 
aggregate.aggregate_data()

app = Flask(__name__)

@app.route('/')
def index():
    # Define the text content for each tile
    # Get tile 1
    
    # Get the data from the database
    db = db_handler.Database('sonnen_data.db')
    data = db.select_manual_input()
    add_cost = db.select_add_cost()
    pprice = db.select_powerprice()
    fprice = db.select_feedprice()
    
    cal_cons = calculation.Calculator(data, pprice)

    consumption = cal_cons.consumption()

    time_diff = cal_cons.ave_profit()

    cal_feed = calculation.Calculator(data, fprice)

    feed = cal_feed.grid_feed()

    add_cost_sum = 0
    for row in add_cost:
        add_cost_sum += row[2]
  
    logging.debug('Consumption', consumption)
    logging.debug('Add Cost', add_cost_sum)

    ave_profit = (consumption + feed - add_cost_sum)/time_diff

    break_even = cal_cons.break_even(ave_profit)

    tile1 = break_even
    tile2 = "{:.2f} €".format(ave_profit)
    tile3 = "{:.2f} €".format(feed)
    tile4 = "{:.2f} €".format(consumption)
    tile5 = "{:.2f} €".format(-1 * add_cost_sum)

    # Render the HTML template with the text content passed as arguments
    return render_template('index.html', tile1=tile1, tile2=tile2, tile3=tile3, tile4=tile4, tile5=tile5)

@app.route('/manual_input', methods=['GET', 'POST'])
def manual_input():
    if request.method == 'POST':
        # Check if delete button was clicked
        if 'delete_button' in request.form:
            # Get the IDs of the rows to be deleted
            delete_ids = request.form.getlist('delete')
            logging.debug(delete_ids)
            # Delete the rows from the database
            db = db_handler.Database('sonnen_data.db')
            db.delete_manual_input(delete_ids)
        else:
        # Get the data from the form
            consumption = float(request.form['consumption'])
            independence_share = float(request.form['independence'])
            independence = consumption * independence_share/100
            production = float(request.form['production'])
            grid_feedin_share = float(request.form['grid_feedin'])
            grid_feedin = grid_feedin_share * production/100
            date = request.form['date']
            
            # Write the data to the database
            db = db_handler.Database('sonnen_data.db')
            db.insert_data(consumption, independence, production, grid_feedin, date, 'M')

    # retrieve data from database
    db = db_handler.Database('sonnen_data.db')
    manual_input_data = db.select_manual_input()
    logging.debug(manual_input_data)

    try:
        manual_input_data = [[row[0], row[1], row[2], row[3], row[4], datetime.strptime(row[5], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d'), row[6]] for row in manual_input_data]
    except TypeError as e:
        print(e)

    return render_template('manual_input.html', manual_input=manual_input_data)

@app.route('/add_cost', methods=['GET', 'POST'])
def add_cost():
    if request.method == 'POST':
        # Check if delete button was clicked
        if 'delete_button' in request.form:
            # Get the IDs of the rows to be deleted
            delete_ids = request.form.getlist('delete')
            logging.debug(delete_ids)
            # Delete the rows from the database
            db = db_handler.Database('sonnen_data.db')
            db.delete_add_cost(delete_ids)
        else:
        # Get the data from the form
            category = request.form['category']
            description = request.form['description']
            cost = float(request.form['cost'])
            date = request.form['date']
            
            # Write the data to the database
            db = db_handler.Database('sonnen_data.db')
            db.insert_add_cost(category, description, cost, date)

    # retrieve data from database
    db = db_handler.Database('sonnen_data.db')
    add_cost_data = db.select_add_cost()
    logging.debug(add_cost_data)

    try:
        add_cost_data = [[row[0], row[3], row[1], row[2], datetime.strptime(row[4], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')] for row in add_cost_data]
    except TypeError as e:
        print(e)

    return render_template('add_cost.html', add_cost=add_cost_data)

if __name__ == '__main__':
    app.run(debug=True)
