import pandas as pd
from datetime import datetime, timedelta
import logging

class Calculator:
    def __init__(self, calc_data, data_price):
        self.calc_data = calc_data
        self.price = data_price

    def consumption(self):

        # create a pandas DataFrame for the battery data
        columns = ['id', 'consumption', 'independence', 'production', 'GridFeedIn', 'date', 'Source']
        
        df = pd.DataFrame(self.calc_data, columns=columns)
        
        # create a pandas dataframe for the power price
        columns = ['id', 'start_date', 'end_date', 'price']
        
        price_df = pd.DataFrame(self.price, columns=columns)

        # ensure timestamp column is in datetime format
        df['date'] = pd.to_datetime(df['date'])  
        
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
        merged_df = pd.merge_asof(df.sort_values('date'), price_df.sort_values('start_date'), 
                          left_on='date', right_on='start_date', 
                          direction='backward', suffixes=('', '_price'))
        
        # create a new column with the price applicable for the data.
        merged_df['price'] = merged_df['price_price'].fillna(method='ffill')

        # drop the unnecessary columns
        merged_df.drop(['id_price', 'start_date', 'end_date', 'price_price'], axis=1, inplace=True)

        print(merged_df)

        results = (merged_df.apply(lambda x: x['independence']*x['price'], axis=1)).sum()


        logging.debug('calculation completed')


        return(results)


    def grid_feed(self):

        # create a pandas DataFrame for the battery data
        columns = ['id', 'consumption', 'independence', 'production', 'GridFeedIn', 'date', 'Source']
        
        df = pd.DataFrame(self.calc_data, columns=columns)
        
        # create a pandas dataframe for the power price
        columns = ['id', 'start_date', 'end_date', 'price']
        
        price_df = pd.DataFrame(self.price, columns=columns)

        # ensure timestamp column is in datetime format
        df['date'] = pd.to_datetime(df['date'])  

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
        merged_df = pd.merge_asof(df.sort_values('date'), price_df.sort_values('start_date'), 
                          left_on='date', right_on='start_date', 
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

        print(merged_df)

        results = (merged_df.apply(lambda x: x['GridFeedIn']*x['price'], axis=1)).sum()

        logging.debug('calculation completed')


        return(results)

    def perdaydata(self):

        columns = ['id', 'output_num', 'charging', 'discharging', 'GridFeedIn_W',
           'consumption_avg', 'consumption_w', 'production_w', 'usoc', 
           'timestamp', 'remaining_capacity_wh']
        
        df = pd.DataFrame(self.calc_data, columns=columns)

        # Convert timestamp column to datetime object
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Sort the DataFrame by timestamp column
        df = df.sort_values('timestamp')

        # Calculate the time difference between consecutive rows
        df['delta_hours'] = (df['timestamp'] - df['timestamp'].shift(1)).dt.total_seconds() / 3600

        # Create a new column for the product of output_num and time difference
        df['consumption_avg_time_diff'] = df['consumption_avg'] * df['delta_hours']
        df['production_time_diff'] = df['production_w'] * df['delta_hours']
        df['grid_feed_time_diff'] = df.apply(lambda x: x['GridFeedIn_W'] * x['delta_hours'] if x['GridFeedIn_W'] > 0 else 0, axis=1)  
        df['grid_cons_time_diff'] = df.apply(lambda x: -1 * x['GridFeedIn_W'] * x['delta_hours'] if x['GridFeedIn_W'] < 0 else 0, axis=1)  

#        df.to_excel('output.xlsx', index=False)

        df.set_index('timestamp', inplace=True)

        # group by day and sum the 'consumption_w' column
        consumption_by_day = df.groupby(pd.Grouper(freq='D'))['consumption_avg_time_diff'].sum()

        production_by_day = df.groupby(pd.Grouper(freq='D'))['production_time_diff'].sum()

        feed_in_by_day = df.groupby(pd.Grouper(freq='D'))['grid_feed_time_diff'].sum()

        grid_cons_by_day = df.groupby(pd.Grouper(freq='D'))['grid_cons_time_diff'].sum()

        print(grid_cons_by_day)       

        # The concat() function uses the index to align the data from multiple dataframes or series. 
        # In this case, since the timestamp column is used as the index for all the input series, 
        # the resulting concatenated dataframe will have a single timestamp column. The values from each 
        # series will be aligned with the timestamp index and placed in their respective columns. 
        # Therefore, when concatenating the series objects with a common index (timestamp), 
        # the resulting dataframe will have only one timestamp column.
        df_combined = pd.concat([consumption_by_day, production_by_day, feed_in_by_day, grid_cons_by_day], axis=1)

      
        print('done with indexing')   

        return df_combined
    
    def ave_profit(self):

        # create a pandas DataFrame for the battery data
        columns = ['id', 'consumption', 'independence', 'production', 'GridFeedIn', 'Date', 'Source']
        
        df = pd.DataFrame(self.calc_data, columns=columns)

        # Convert the Date column to a datetime data type
        df['Date'] = pd.to_datetime(df['Date'])

        # Calculate the time difference between the first and last date
        time_diff = max(df['Date']) - min(df['Date'])

        # Print the time difference in days
        return time_diff.days
    
    def break_even(self, ave_profit):
        
        cost = 40000
        start_data = '2023-03-17'
        
        # Convert the start_data to a datetime object
        start_date = datetime.strptime(start_data, '%Y-%m-%d').date()
        
        # Calculate the number of days to break-even
        days_to_break_even = cost / ave_profit
        
        # Calculate the break-even date
        break_even_date = start_date + timedelta(days=days_to_break_even)
       
        # Print the break-even date
        # logging.debug("The break-even date is:", break_even_date)

        return break_even_date