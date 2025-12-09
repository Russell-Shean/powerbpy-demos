import requests
import py7zr
import os
import tempfile

import pandas as pd
import numpy as np

from powerbpy import Dashboard

'''
Step 1 Download data --------------------------------------------
Download the data from Github and 
then extract the individual datasets from the compressed archive file. 
'''

# step 1: obtain data from github --------------------------------------------------------------

# Define paths
dataset_url = "https://github.com/sql-bi/Contoso-Data-Generator-V2-Data/releases/download/ready-to-use-data/csv-10k.7z" 
data_destination_dir = "data"


# make sure the folder exists
os.makedirs(data_destination_dir, exist_ok=True)

# download the zip file from the internet
response = requests.get(dataset_url, stream=True)
response.raise_for_status()

# write to file
with tempfile.NamedTemporaryFile(suffix=".7z", delete=False) as tmp_file:
    with open(tmp_file.name, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)



# extract the data 
with py7zr.SevenZipFile(tmp_file.name, mode="r") as z:
    z.extractall(path=data_destination_dir)


'''
Step 2 Process data --------------------------------------------
Proccess the data we downloaded 
'''


# Read in the datasets
store = pd.read_csv("data/store.csv")
sales = pd.read_csv("data/sales.csv")

# Create a dictionary of names and codes
store_names = (
                store[["StoreKey", "Description"]]
               .drop_duplicates()
               .reset_index(drop=True)
               )



# Makes sure OrderDate is a date
sales["OrderDate"] = pd.to_datetime(sales["OrderDate"])

# Create a new dataframe with aggregate sales total
# By date periods and store

sales_by_store_and_date = (
    sales

    # assign seems to be similiar to mutate
    .assign(

        # np.select appears to be similiar to case_when
        time_period = lambda df: np.select(


            # Define to logical conditions to check for
            [
                df["OrderDate"] <= df
                                   .groupby("StoreKey")["OrderDate"]
                                   .transform("min") 
                                   + pd.Timedelta(days=180),

                df["OrderDate"] >= df
                                   .groupby("StoreKey")["OrderDate"]
                                   .transform("max") 
                                   - pd.Timedelta(days=180)
            ],

            # Define labels if the conditions are met
            ["first_180",
             "last_180"],

             # Define a default for if neither condition is matched
             default="middle_period"



        )
    ) 

    # calculate grouped sales totals by time period and store
    .groupby(["StoreKey", "time_period"], as_index=False)
    .agg(store_total_sales = ("NetPrice", "sum"))


    # label the sales volumes as small, medium and large
    .assign(

        sales_size = lambda df: np.select(



            [
                df["store_total_sales"] < 1000,

                (df["store_total_sales"] >= 1000) &
                (df["store_total_sales"] < 5000),

                df["store_total_sales"] >= 5000
 
            ],

            [ 
                "Small",
                "Medium",
                "Large"
            ],
        default="Unknown" 


        ) 


    )

    # Merge the store names onto the dataframe
    .merge(
        
        store_names, 
        on = "StoreKey",
        how = "left"

    )

    # pivot the dataframe to expand the time period and sales size columns wider
    .pivot(
        index="Description",
        columns="time_period",
        values=['store_total_sales', "sales_size"]
    )

)


# undo the multi indexing of column names 
# (I don't even want to try to imagine how Power BI would try to handle multi-indexed columns lol)
sales_by_store_and_date.columns = [
    f"{val}_{col}" for val, col in sales_by_store_and_date.columns
]

# finish the final steps in the chain
sales_by_store_and_date = (

    sales_by_store_and_date

    # reset the index
    .reset_index()

    # select the columns we want
    .loc[:, ["Description", 
             "store_total_sales_first_180",
             "store_total_sales_last_180",
             "sales_size_first_180",
             "sales_size_last_180"]]

    # Rename the columns we want
    .rename(columns={
        'Description': 'Name',
        'store_total_sales_first_180': 'Sales First 180 Days',
        'store_total_sales_last_180': 'Sales Last 180 Days',
        'sales_size_first_180': 'Starting Size',
        'sales_size_last_180': 'Ending Size'
    })

)

# write to file
sales_by_store_and_date.to_csv("data/final_dataset.csv", index=False)   


'''
Step 3 Create dashboard --------------------------------------------
Create a new dashboard using the data we downloaded and processesd
'''

# Define the path to the dashboard
dashboard_path = os.path.join(os.getcwd(), "sanky_demo")


# Create a new blank dashboard
my_dashboard = Dashboard.create(dashboard_path)

# add the data from step 2
my_dashboard.add_local_csv(data_path = "data/final_dataset.csv" )

# Add a new page to the dashboard
page1 = my_dashboard.new_page(page_name="A demonstration sanky chart")


# add a table
page1.add_table(visual_id = "sales_table", 
              data_source = "final_dataset", 
              variables = ["Name", "Sales First 180 Days", "Sales Last 180 Days", "Starting Size", "Ending Size"],
              x_position = 615, 
              y_position = 0, 
              height = 800, 
              width = 615,
              add_totals_row = False,
              table_title = "Store Sales Details")


page1.add_sanky_chart(visual_id = "sales_sanky", 
              data_source = "final_dataset",
              chart_title="Store Starting and Ending Size",
              starting_var="Starting Size",
              starting_var_values=["Large", "Medium", "Small"], 
              ending_var="Ending Size",
              ending_var_values=["Large", "Medium", "Small"],
              values_from_var="Name", 
              x_position=0, 
              y_position=0, 
              height = 800, 
              width = 615)

