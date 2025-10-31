import pandas as pd
import numpy as np

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

                (df["store_total_sales"] > 1000) &
                (df["store_total_sales"] < 5000),

                df["store_total_sales"] > 5000
 
            ],

            [ 
                "Small",
                "Medium",
                "Large"
            ]






        ) 


    )



)

print(sales_by_store_and_date)

