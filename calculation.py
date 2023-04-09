import pandas as pd
from datetime import datetime
import logging

class Calculator:
    def __init__(self, data_battery, data_price):
        self.battery = data_battery
        self.price = data_price

    def consumption(self):

        # create a pandas DataFrame for the battery data
        columns = ['id', 'output_num', 'charging', 'discharging', 'GridFeedIn_W',
           'consumption_avg', 'consumption_w', 'production_w', 'usoc', 
           'timestamp', 'remaining_capacity_wh']
        
        df = pd.DataFrame(self.battery, columns=columns)
        
        # create a pandas dataframe for the power price
        columns = ['id', 'start_date', 'end_date', 'price']
        
        price_df = pd.DataFrame(self.price, columns=columns)

        # ensure timestamp column is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])  
        
        # Create a new column delta_hours in the data frame with the time delta in hours between consecutive rows.
        # the shift method of pandas to shift the timestamps of the data frame by one row
        df['delta_hours'] = (df['timestamp'] - df['timestamp'].shift(1)).dt.total_seconds() / 3600

        # Create a new column with the price applicable for the data. 
        # convert startdate and enddate to datetime objects
        # Make sure that the last row end_date is replace it with now.
        now = datetime.now()
        price_df.iloc[-1, price_df.columns.get_loc('end_date')] = now

        price_df['start_date'] = pd.to_datetime(price_df['start_date'])
        price_df['end_date'] = pd.to_datetime(price_df['end_date'])

        # create a new column in df for the price
        df['price'] = 0

        # iterate over the rows of df and add the price from price_df
        merged_df = pd.merge_asof(df.sort_values('timestamp'), price_df.sort_values('start_date'), 
                          left_on='timestamp', right_on='start_date', 
                          direction='backward', suffixes=('', '_price'))
        
        # create a new column with the price applicable for the data.
        merged_df['price'] = merged_df['price_price'].fillna(method='ffill')

        # drop the unnecessary columns
        merged_df.drop(['id_price', 'start_date', 'end_date', 'price_price'], axis=1, inplace=True)


        # The apply() function in pandas to apply a function to each row of a DataFrame. 
        # a lambda function is a small anonymous function that can take any number of arguments, 
        # but can only have one expression. It is called "anonymous" because it does not have 
        # a name like a regular function. Instead, it is defined using the lambda keyword and 
        # is typically used to create short, throwaway functions that can be passed as arguments 
        # to other functions or used in one-off situations where a named function would be unnecessary 
        # or cumbersome.
        # In Pandas, the axis parameter in a function determines whether the function should be 
        # applied to rows (axis=0) or columns (axis=1) of a dataframe.
        # calculate the consumption and return the result
        total_consumption = (merged_df.apply(lambda row: row['delta_hours'] * row['consumption_w']/1000 * row['price'], axis=1)).sum()

        total_grid_feed_in = (merged_df.apply(lambda row: -1 * row['delta_hours'] * row['GridFeedIn_W']/1000 * row['price'] if row['GridFeedIn_W'] < 0 else 0, axis=1)).sum()


        logging.debug('calculation completed')


        return(total_consumption-total_grid_feed_in)


    def grid_feed(self):

        # create a pandas DataFrame for the battery data
        columns = ['id', 'output_num', 'charging', 'discharging', 'GridFeedIn_W',
           'consumption_avg', 'consumption_w', 'production_w', 'usoc', 
           'timestamp', 'remaining_capacity_wh']
        
        df = pd.DataFrame(self.battery, columns=columns)
        
        # create a pandas dataframe for the power price
        columns = ['id', 'start_date', 'end_date', 'price']
        
        price_df = pd.DataFrame(self.price, columns=columns)

        # ensure timestamp column is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])  
        
        # Create a new column delta_hours in the data frame with the time delta in hours between consecutive rows.
        # the shift method of pandas to shift the timestamps of the data frame by one row
        df['delta_hours'] = (df['timestamp'] - df['timestamp'].shift(1)).dt.total_seconds() / 3600

        # Create a new column with the price applicable for the data. 
        # convert startdate and enddate to datetime objects
        # Make sure that the last row end_date is replace it with now.
        now = datetime.now()
        price_df.iloc[-1, price_df.columns.get_loc('end_date')] = now

        price_df['start_date'] = pd.to_datetime(price_df['start_date'])
        price_df['end_date'] = pd.to_datetime(price_df['end_date'])

        # create a new column in df for the price
        df['price'] = 0

        # iterate over the rows of df and add the price from price_df
        merged_df = pd.merge_asof(df.sort_values('timestamp'), price_df.sort_values('start_date'), 
                          left_on='timestamp', right_on='start_date', 
                          direction='backward', suffixes=('', '_price'))
        
        # create a new column with the price applicable for the data.
        merged_df['price'] = merged_df['price_price'].fillna(method='ffill')

        # drop the unnecessary columns
        merged_df.drop(['id_price', 'start_date', 'end_date', 'price_price'], axis=1, inplace=True)


        # The apply() function in pandas to apply a function to each row of a DataFrame. 
        # a lambda function is a small anonymous function that can take any number of arguments, 
        # but can only have one expression. It is called "anonymous" because it does not have 
        # a name like a regular function. Instead, it is defined using the lambda keyword and 
        # is typically used to create short, throwaway functions that can be passed as arguments 
        # to other functions or used in one-off situations where a named function would be unnecessary 
        # or cumbersome.
        # In Pandas, the axis parameter in a function determines whether the function should be 
        # applied to rows (axis=0) or columns (axis=1) of a dataframe.
        # calculate the consumption and return the result

        total_grid_feed_in = (merged_df.apply(lambda row: row['delta_hours'] * row['GridFeedIn_W']/1000 * row['price'] if row['GridFeedIn_W'] > 0 else 0, axis=1)).sum()


        logging.debug('calculation completed')


        return(total_grid_feed_in)


