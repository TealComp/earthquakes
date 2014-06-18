#!/usr/bin/env python
# import and explore earthquake data from USGS
# http://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php
# (c) TealComp.com 20140327

# --- import modules ---
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time as time
import datetime as datetime
import calendar as calendar
from mpl_toolkits.basemap import Basemap

# --- functions ---
def str2datetime(timestr):
	""" Convert time string to datetime object """
	return datetime.datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%fZ')

def plot_quakes(quakes):
	""" Plot quakes in passed dataframe """

	heatcolors = ('#FFFF00', '#FF9900', '#CC3333')
	heatcolor = None

	cenlat = np.mean(quakes['latitude'])
	cenlon = np.mean(quakes['longitude'])
	fig = plt.figure(figsize=(9,9))
	m = Basemap(resolution = 'l', projection='merc', llcrnrlat = -80, urcrnrlat = 80, llcrnrlon = -180, urcrnrlon = 180, lat_0 = cenlat, lon_0 = cenlon)
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	m.fillcontinents(color = '#0CAA43', lake_color = 'aqua')
	m.drawmapboundary(fill_color = '#0B4BD2')
	x, y = m(quakes['longitude'], quakes['latitude'])
	
	for i in range(len(x)):
		if quakes['depth'][i:i+1].any() < 70:
			heatcolor = heatcolors[1]
		elif 70 <= quakes['depth'][i:i+1].any() < 300:
			heatcolor = heatcolors[2]
		else:
			heatcolor = heatcolors[3]
		m.plot(x[i:i+1], y[i:i+1], heatcolor, marker = 'o', markersize = (np.pi * quakes['mag'][i:i+1]**2)/2, alpha = 0.6)
	fig.show()

def plot_quake_mag_by_time(quakes):
	""" plot earthquake magnitudes by time """
	x, y = str2datetime(quakes['time']), quakes['mag']

	plt.plot(x,y)

def quake_feature_stats(quakes, feature):
	""" Return dictionary containing mininum ('min'), maximum ('max'), mean, and standard deviation ('std') for the specified feature """

	return {'min' : np.min(quakes[feature]), 
		'max' : np.max(quakes[feature]),
		'mean' : np.mean(quakes[feature]),
		'std' : np.std(quakes[feature])}


# --- read data ---
eq = pd.read_csv('usgs_earthquakes_all_20140327.csv', sep=',', header=0)

# describe the data set
date_min = np.min([str2datetime(tm) for tm in eq['time']])
date_max = np.max([str2datetime(tm) for tm in eq['time']])
print('The current data set includes USGS earthquake records from {0} to {1}.'.format(date_min, date_max))

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('Feature  \tMinimum\tMaximum\tMean\tStandard Deviation')
stats_depth = quake_feature_stats(eq, 'depth')
print('{0}\t{1:0.1f}\t{2:0.1f}\t{3:0.1f}\t{4:0.1f}'.format(
	'Depth (km)',
	stats_depth['min'],
	stats_depth['max'],
	stats_depth['mean'],
	stats_depth['std']))
stats_mag = quake_feature_stats(eq, 'mag')
print('{0}\t{1:0.1f}\t{2:0.1f}\t{3:0.1f}\t{4:0.1f}'.format(
	'Magnitude',
	stats_mag['min'],
	stats_mag['max'],
	stats_mag['mean'],
	stats_mag['std']))

# pause for user
print('')
junk = raw_input('Press ENTER to examine daily quake counts; else press CTRL-C')

# examine daily quake counts
quake_counts = []
#num_days = (date_max - date_min).days
this_date = date_min.date()
while this_date <= date_max.date():
	cnt = 0
	for tm in eq['time']:
		eqdate = str2datetime(tm).date()
		if this_date == eqdate:
			cnt = cnt + 1
	quake_counts.append((this_date, cnt))
	this_date = this_date + datetime.timedelta(days=1)
for item in quake_counts:
	print('{0}: {1}'.format(item[0].isoformat(), item[1]))



# pause for user
print('')
junk = raw_input('Press ENTER to generate a map of quakes; else press CTRL-C')

# generate map of quakes
print('\nThis may take a moment ...')
plot_quakes(eq)
print('The plot is complete.  Take a look!')

# select desired subset, say those quakes with magnitudes greater than
# the mean
#mean_mag = np.mean(eq['mag'])

#print('Quakes in this 30-day period had a mean magnitude of {0:0.2f} with a standard deviation of {1:0.2f}'.format(mean_mag))
#my_quakes = eq[eq['mag'] > mean_mag]
#my_times = [tm for tm in my_quakes['time']]
#my_lats = [lat for lat in my_quakes['latitude']]
#my_lons = [lon for lon in my_quakes['longitude']]
#my_depths = [depth for depth in my_quakes['depth']]
#my_mags = [mag for mag in my_quakes['mag']]

#print('The following quakes had magnitudes greater than the mean for this 30-day period:')
#print('Time\tMagnitude\tLatitude\tLongitude\tDepth (m)')
#for i in range(len(my_times)):
#	print('{0}\t{1:0.2f}\t{2:0.6f}\t{3:0.6f}\t{4:0.1f}'.format(
#		my_times[i],
#		my_mags[i],
#		my_lats[i],
#		my_lons[i],
#		my_depths[i]))




#events = []
#for i in range(len(eq)):
#	dt = str2datetime(eq['time'][i])
#	lat = eq['latitude'][i]
#	lon = eq['longitude'][i]
#	depth = eq['depth'][i]
#	mag = eq['mag'][i]
#
#	events.append((dt, mag))
#
#plt.plot(events[0], events[1], 'b+')
#	timenow = datetime.datetime.now()
#	since = (timenow - dt)
#	print('{0} hours before now'.format(since.seconds / 3600))

#	print('{0}:{1}:{2}:{3}:{4}'.format(since, lat, lon, depth, mag))

