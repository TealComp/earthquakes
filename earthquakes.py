#!/usr/bin/env python
# import and explore earthquake data from USGS
# http://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php
# (c) TealComp.com 20140327

# --- import modules ---
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import time as time
import datetime as datetime
import calendar as calendar

# --- functions ---
def str2datetime(timestr):
	""" Convert time string to datetime object """
	return datetime.datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%S.%fZ')

def plot_quakes(quakes):
	""" Plot quakes in passed dataframe """

	# create a set of heatcolor codes
	heatcolors = ('#FFFF00', '#FF9900', '#CC3333')
	heatcolor = None            # initialize heatcolor to None

	cenlat = np.mean(quakes['latitude'])    # find central latitude
	cenlon = np.mean(quakes['longitude'])   # find central longitude
	fig = plt.figure(figsize=(9,9))         # create a new figure
        # create a map using a mercator projection
	m = Basemap(resolution='l', 
                    projection='merc',
                    llcrnrlat=-80, urcrnrlat=80,
                    llcrnrlon=-180, urcrnrlon=180,
                    lat_0=cenlat, lon_0=cenlon)
	m.drawcoastlines()            # add coastlines
	m.drawcountries()             # add country borders
	m.drawstates()                # add state borders
	# fill in countinents and lakes
	m.fillcontinents(color = '#0CAA43', lake_color = 'aqua')
	# draw boundary around map
	m.drawmapboundary(fill_color = '#0B4BD2')
	# generate x and y values from longitude and latitude
	# x, y = m(quakes['longitude'], quakes['latitude'])
	lats = [ v for v in quakes['latitude'] ]
	lons = [ v for v in quakes['longitude'] ]
	depths = [ v for v in quakes['depth'] ]
	mags = [ v for v in quakes['mag'] ]
	x, y = m(lons, lats)

	# loop through x values
	for i in range(len(x)):
		if depths[i:i+1] < 70:
			# set color for depths less than 70
			heatcolor = heatcolors[0]
		elif 70 <= depths[i:i+1] < 300:
			# set color for depths between 70 and 300
			heatcolor = heatcolors[1]
		else:
			# set color for depths greater than or equal to 300
			heatcolor = heatcolors[2]
		# plot quakes using circles with colors appropriate for
		# depth and radius relative to magnitude
		m.plot(x[i], y[i], heatcolor, marker = 'o', markersize = (np.pi * mags[i]**2)/2, alpha = 0.6)
		sys.stdout.write('. ')
		sys.stdout.flush()
	fig.show()


def plot_quake_counts(quakes):
	""" plot earthquake counts by day as histogram """
	dates = []                    # initialize list of dates
	quake_counts = []             # initialize list for quake counts
	this_date = date_min.date()   # initialize date iterator
	# loop through dates until all dates have been examined
	while this_date <= date_max.date():
		cnt = 0               # initialize quake counter
		# loop through quake data, looking for dates
		# matching the current date
		for tm in eq['time']:
			if this_date == str2datetime(tm).date():
				cnt = cnt + 1
		# store the date and daily counts in lists
		dates.append(this_date)
		quake_counts.append(cnt)
		sys.stdout.write('. ')
		sys.stdout.flush()
		this_date = this_date + datetime.timedelta(days=1)
	# plot quake counts as a series of horizontal lines
	plt.hlines(dates, 
		   0, quake_counts,
		   colors='b',
		   linestyles='solid')
	plt.title('Daily Quake Counts')
	plt.xlabel('Number of Quakes')
	plt.ylabel('Date')
	plt.grid(True)
	plt.show()
	print('')


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
print('\nThe current data set includes USGS earthquake records from {0} to {1}.'.format(date_min, date_max))

print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
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

print('\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('For the quake with greatest magnitude during the period, the following data were collected:')
print(eq.loc[eq['mag'].argmax()])


# pause for user
#print('')
#junk = raw_input('Press ENTER to plot daily quake counts; else press CTRL-C')

# generate plot of daily quake counts
print('\nGenerating plot of daily quake counts')
print('This may take a moment ...')
plot_quake_counts(eq)
print('The plot is complete.  Take a look!')

# pause for user
#print('')
#junk = raw_input('Press ENTER to generate a map of quakes; else press CTRL-C')

# generate map of quakes with magnitude greater than mag_limit
mag_limit = 6.0
print('\nGenerating map of quakes with magnitudes greater than or equal to {0}'.format(mag_limit))
print('This may take a moment ...')
criterion = eq['mag'].map(lambda x: x >= mag_limit)
plot_quakes(eq[criterion])
print('\nThe plot is complete.  Take a look!')

