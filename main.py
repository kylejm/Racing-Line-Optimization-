import numpy as np
import pandas 
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from scipy.signal import savgol_filter


# Data Unpacking 
data = pandas.read_csv('Silverstone.csv') # Import track data (data from https://github.com/TUMFTM/racetrack-database/blob/master/tracks/Silverstone.csv)

x_mid = np.array(data.loc[:,'# x_m'])
y_mid = np.array(data.loc[:,'y_m'])
center = np.array(data.loc[:,['# x_m','y_m']])

track_width_right = np.array(data.loc[:,'w_tr_right_m'])
track_width_left = np.array(data.loc[:,'w_tr_left_m'])

plt.rcParams["figure.figsize"] = [7.50, 7.00]
plt.rcParams["figure.autolayout"] = True

inside_avg_left = np.mean(track_width_left) # Using means to make a smoother curve
inside_avg_right = np.mean(track_width_right)

center_line = LineString(center)
inside_line = center_line.parallel_offset(inside_avg_left, 'left')
outside_line = center_line.parallel_offset(inside_avg_right, 'right')
plt.plot(*center_line.xy,'b')
plt.plot(*inside_line.xy,'b')
plt.plot(*outside_line.xy,'b')

yhat = savgol_filter(y_mid,40,3)
car_mid = []

for i in range(len(x_mid)-1):
    car_mid.append([x_mid[i],yhat[i]])

car_mid = LineString(car_mid)
#plt.plot(*car_mid.xy,'g')

car_left = car_mid.parallel_offset(1,'left')
car_right = car_mid.parallel_offset(1,'right')
plt.plot(*car_left.xy,'g.')
plt.plot(*car_right.xy,'g.')

# How Accurate This racing line is
# Dynamically change track width
# More exaggerated curves
# Run Savgol until waviest line that hits all parts of track 
plt.show()