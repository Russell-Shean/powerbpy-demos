import powerbpy as pbi
import os

# Define the path to the dashboard
dashboard_path = os.path.join(os.getcwd(), "sanky_demo")

# define the absolute path to the data because Power BI can't handle relative paths
# I will later add steps to the add data functions to convert relative paths to absolute paths

data_location = os.path.join(os.getcwd(), "data/final_dataset.csv" )

# Create a new blank dashboard
pbi.create_new_dashboard(parent_dir = os.getcwd(), report_name = "sanky_demo")

# add the data from step 2
pbi.add_local_csv(dashboard_path = dashboard_path, 
            data_path = data_location )


# add a table