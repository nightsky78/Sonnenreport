import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    
    def insert_dataset(self, output_num, charging, discharging, GridFeedIn_W,  consumption_avg, consumption_w, production_w, usoc, timestamp, remaining_capacity_wh):
        self.cursor.execute("INSERT INTO sonnendata (output_num, charging, discharging, GridFeedIn_W, consumption_avg, consumption_w, production_w, usoc, timestamp, remaining_capacity_wh) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (output_num, charging, discharging, GridFeedIn_W, consumption_avg, consumption_w, production_w, usoc, timestamp, remaining_capacity_wh))
        self.conn.commit()

    def select_powerprice(self):
        self.cursor.execute("SELECT * FROM powerprice")
        return self.cursor.fetchall()    
    
    def select_feedprice(self):
        self.cursor.execute("SELECT * FROM feedprice")
        return self.cursor.fetchall()    
    

    def select_all(self):
        self.cursor.execute("SELECT * FROM sonnendata ORDER BY timestamp")
        return self.cursor.fetchall()
    
    def get_records_by_date_range(self, start_date, end_date):
        query = "SELECT * FROM sonnendata WHERE date_created BETWEEN ? AND ?"
        self.cursor.execute(query, (start_date, end_date))
        records = self.cursor.fetchall()
        return records
       
    def close_connection(self):
        self.conn.close()