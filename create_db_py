import sqlite3

# Connect to the database (this will create a new file if it doesn't already exist)
conn = sqlite3.connect('sonnen_data.db')

# Create a new table with the columns you specified
conn.execute('''CREATE TABLE sonnendata
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             output_num INTEGER,
             charging BOOL,
             discharging BOOL,
             GridFeedIn_W NUMERIC, 
             consumption_avg NUMERIC,
             consumption_w NUMERIC,
             production_w NUMERIC,
             usoc NUMERIC,
             timestamp DATETIME,
             remaining_capacity_wh NUMERIC);''')

# Commit the changes and close the connection
conn.commit()
conn.close()
