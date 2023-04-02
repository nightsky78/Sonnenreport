from flask import Flask, render_template
import db_handler
import logging
import calculation

# first set the log level
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    # Define the text content for each tile
    # Get tile 1
    
    # Get the data from the database
    db = db_handler.Database('sonnen_data.db')
    data = db.select_all()
    pprice = db.select_powerprice()
    logging.debug(data)
    logging.debug(pprice)
    
    cal = calculation.Calculator(data, pprice)

    consumption = cal.consumption()


    
    logging.debug(consumption)

    tile1 = 'Tile 1 content'
    tile2 = 'Tile 2 content'
    tile3 = 'Tile 3 content'
    tile4 = "{:.2f} €".format(consumption)

    # Render the HTML template with the text content passed as arguments
    return render_template('index.html', tile1=tile1, tile2=tile2, tile3=tile3, tile4=tile4)

if __name__ == '__main__':
    app.run(debug=True)
