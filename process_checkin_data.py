import sys
import os
import pandas as pd
import numpy as np
from dateutil import parser
import traceback

if len(sys.argv) < 2:
    print("Please enter the data path as the first argument")
    exit()

data_path = sys.argv[1]

checkin_day_hour_counts = []
for date in os.listdir(data_path):
    try:
        df = pd.read_csv(os.path.join(data_path, date, "checking.csv"), engine="python")
        hour_counts = np.zeros(24, dtype=int)
        for index, row in df.iterrows():
            checkin_time = row["checkin"]
            if checkin_time == "0":
                continue
            hour = parser.parse(checkin_time).hour
            hour_counts[hour] = hour_counts[hour] + 1
        day = parser.parse(date).day
        checkin_day_hour_counts.append((day, hour_counts))
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"An unknown exception occurred when processing {date}. Skipped.")
        traceback.print_exc()

# print(checkin_day_hour_counts)

echarts_data = [[day, hour, hour_count] for hour, hour_count in enumerate(hour_counts)
                for day, hour_counts in checkin_day_hour_counts]
print(echarts_data)
