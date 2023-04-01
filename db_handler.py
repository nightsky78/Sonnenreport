import sqlite3

class PersonDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    
    def insert_dataset(self, output_num, charging, discharging, consumption_avg, consumption_w, production_w, rsoc, timestamp, remaining_capacity_wh):
        self.cursor.execute("INSERT INTO example_table (output_num, charging, discharging, consumption_avg, consumption_w, production_w, rsoc, timestamp, remaining_capacity_wh) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (output_num, charging, discharging, consumption_avg, consumption_w, production_w, rsoc, timestamp, remaining_capacity_wh))
        self.conn.commit()
    
    def select_all(self):
        self.cursor.execute("SELECT * FROM people")
        return self.cursor.fetchall()
    
    def get_records_by_date_range(self, start_date, end_date):
        query = "SELECT name, age FROM people WHERE date_created BETWEEN ? AND ?"
        self.cursor.execute(query, (start_date, end_date))
        records = self.cursor.fetchall()
        return records
       
    def close_connection(self):
        self.conn.close()