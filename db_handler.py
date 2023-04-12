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

    def insert_data(self, consumption, independence, production, grid_feedin, date):
        # insert a new row into the manual_input table
        query = '''INSERT INTO manual_input (consumption_w, independence_w, production_w, grid_feedin_w, date) 
                   VALUES (?, ?, ?, ?, ?)'''
        self.cursor.execute(query, (consumption, independence, production, grid_feedin, date))
        self.conn.commit()

    def select_manual_input(self):
        self.cursor.execute("SELECT * FROM manual_input ORDER BY date")
        data = self.cursor.fetchall()
        return data
        
    def delete_manual_input(self, delete_ids):
        """
        Deletes the rows with the given IDs from the manual_input table.

        Args:
            delete_ids (list[int]): A list of IDs to delete.

        Raises:
            sqlite3.Error: If the deletion fails.
        """
        # Create a string with placeholders for the IDs
        id_placeholders = ','.join('?' * len(delete_ids))

        # Execute the delete query
        try:
            self.conn.execute(f'DELETE FROM manual_input WHERE id IN ({id_placeholders})', delete_ids)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e


    def close_connection(self):
        self.conn.close()