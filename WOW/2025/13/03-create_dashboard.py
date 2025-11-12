import powerbpy as pbi
import os

# Define the path to the dashboard
dashboard_path = os.path.join(os.getcwd(), "sanky_demo")


# Create a new blank dashboard
pbi.create_new_dashboard(parent_dir = os.getcwd(), report_name = "sanky_demo")

# add the data from step 2
pbi.add_local_csv(dashboard_path = dashboard_path, 
            data_path = "data/final_dataset.csv" )


# add a table
pbi.add_table(dashboard_path = dashboard_path,
              page_id = "page1", 
              table_id = "sales_table", 
              data_source = "final_dataset", 
              variables = ["Name", "Sales First 180 Days", "Sales Last 180 Days", "Starting Size", "Ending Size"],
              x_position = 615, 
              y_position = 0, 
              height = 800, 
              width = 615,
              add_totals_row = False,
              table_title = "Store Sales Details",
              #column_widths = {"Name":200,"Sales First 180 Days":100,"Sales Last 180 Days":100},
              tab_order = -1001,
              z_position = 6000 )


pbi.add_sanky_chart(dashboard_path = dashboard_path,
              page_id = "page1", 
              chart_id = "sales_sanky", 
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
              width = 615,
)