'''
This script creates a new dashboard using the data we downloaded and processesd
'''
# pylint: disable=import-error
# pylint: disable=invalid-name

import os

from powerbpy import Dashboard

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
              variables = ["Name", 
                           "Sales First 180 Days", 
                           "Sales Last 180 Days", 
                           "Starting Size", 
                           "Ending Size"],
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
