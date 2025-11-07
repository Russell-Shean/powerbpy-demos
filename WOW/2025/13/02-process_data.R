library(dplyr)
library(lubridate)
library(tidyr)
library(readr)

# NOTE: all this assumes that you have WOW/2025/13 
# as the root directory
# Not powerbpy-demos

# setwd("WOW/2025/13")

# Read in datasets
store <- read_csv("data/store.csv")
sales <- read_csv("data/sales.csv")


# get a dictionary of stores and names
store_names <- store |> 
  select(StoreKey, Description) |>
  distinct()

# Determine sales totals for first 180 days and later sales
# By each store

  
sales_by_store_and_date <- sales |>
  group_by(StoreKey ) |>
  mutate(time_period = case_when(OrderDate <= min(OrderDate) + days(180) ~ "first_180",
                                 OrderDate >= max(OrderDate) - days(180) ~ "last_180",
                                 .default = "middle_period")) |> 
  ungroup() |>
  group_by(StoreKey, time_period) |>
  summarise(store_total_sales = sum(NetPrice), .groups = "drop") |> 

# Classify sales as large, medium and small
  mutate(sales_size = case_when(store_total_sales < 1000 ~ "Small",
                                store_total_sales > 1000  & 
                                  store_total_sales <= 5000 ~ "Medium",
                                store_total_sales > 5000 ~ "Large",
                                .default = NA) ) |>
  
  
  # attach store names to dataframe
  left_join(store_names) |>
  
  # widen the dataframe 
  pivot_wider(names_from = time_period,
              values_from = c(store_total_sales, sales_size)) |>
  
  # select the columns we need
  select(Name = Description,
         `Sales First 180 Days` = store_total_sales_first_180,
         `Sales Last 180 Days` = store_total_sales_last_180,
         `Starting Size` = sales_size_first_180,
         `Ending Size` = sales_size_last_180) 


sales_by_store_and_date |>
  write.csv("data/final_dataset.csv", row.names = FALSE)




