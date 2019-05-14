import sys
import os
import pandas as pd
import numpy as np
from dateutil import parser
import traceback

__author__ = "Ye"

if len(sys.argv) < 2:
    print("Please enter the data path as the first argument")
    exit()

data_path = sys.argv[1]

checkin_day_hour_counts = []
checkout_day_hour_counts = []

dates = list(filter(lambda filename: os.path.isdir(
    os.path.join(data_path, filename)), os.listdir(data_path)))
print(f"Dates: {dates}")
with open("data/dates.txt", "w") as f:
    f.write(str(dates))
for date in dates:
    try:
        df = pd.read_csv(os.path.join(
            data_path, date, "checking.csv"), engine="python")
        checkin_hour_counts = np.zeros(24, dtype=int)
        checkout_hour_counts = np.zeros(24, dtype=int)
        for index, row in df.iterrows():
            checkin_time = row["checkin"]
            if checkin_time != "0":
                hour = parser.parse(checkin_time).hour
                checkin_hour_counts[hour] = checkin_hour_counts[hour] + 1
            checkout_time = row["checkout"]
            if checkout_time != "0":
                hour = parser.parse(checkout_time).hour
                checkout_hour_counts[hour] = checkout_hour_counts[hour] + 1
        day = parser.parse(date).day
        checkin_day_hour_counts.append((day, checkin_hour_counts))
        checkout_day_hour_counts.append((day, checkout_hour_counts))
    except FileNotFoundError:
        pass
    except Exception as e:
        print(
            f"An unknown exception occurred when processing {date}. Skipped.")
        traceback.print_exc()

# print(checkin_day_hour_counts)

echarts_checkin_data = [[day, hour, hour_count]
                        for day, hour_counts in checkin_day_hour_counts
                        for hour, hour_count in enumerate(hour_counts)]
print(f"Echarts check-in data: {echarts_checkin_data}")
with open("data/processed_checkin_data.txt", "w") as f:
    f.write(str(echarts_checkin_data))

echarts_checkout_data = [[day, hour, hour_count]
                         for (day, hour_counts) in checkout_day_hour_counts
                         for hour, hour_count in enumerate(hour_counts)]
print(f"Echarts check-out data: {echarts_checkout_data}")
with open("data/processed_checkout_data.txt", "w") as f:
    f.write(str(echarts_checkout_data))