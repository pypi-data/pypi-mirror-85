import pandas as pd
import numpy as np

file_name = 'teneriffe_wind_normalized_10m.csv'
csv_file = pd.read_csv(file_name, delimiter=',', decimal='.', header=None)
csv_file = csv_file.multiply(1000)
time = np.arange(1388530800.0,1388530800.0+600*len(csv_file), 600)

time = pd.DataFrame(time)
csv_file.insert(0,'time', time)
# csv_file_new = pd.concat([time, csv_file], axis=1)
csv_file.to_csv('new_wind_profile.csv', decimal='.', sep=',', index=False, header=None)
