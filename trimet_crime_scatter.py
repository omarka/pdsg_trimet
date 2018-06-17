import pandas as pd
import numpy as np
#import scipy
#import sklearn
import matplotlib.pyplot as plt


# Define file names
file_name_911 = '911-calls.csv'
file_name_neighborhoods = 'neighborhoods_gps.csv'
file_name_trimet = 'events_hour.csv'


# Import file as a pandas data frame
df_911 = pd.read_csv(file_name_911)
df_neighborhoods = pd.read_csv(file_name_neighborhoods)
df_trimet = pd.read_csv(file_name_trimet)

#Create dictionaries for longitude and latitude based on neighborhood
df_neighborhoods = df_neighborhoods.set_index('Neighborhood')
dictionary_neighborhoods_gps = df_neighborhoods.to_dict()
latitude_dictionary = dictionary_neighborhoods_gps['GPS Latitude']
longitude_dictionary = dictionary_neighborhoods_gps['GPS Longitude']


#Reduce dataframe to only neighborhood and response time info
crime_neighborhood_response_df = df_911[['Neighborhood', 'Response Time (sec)']].dropna(subset=['Response Time (sec)'])#.groupby('Neighborhood').count().iloc[:,0]
#Get mean response time and count statistics associated with each neighborhood
crime_neighborhood_response_incidents = crime_neighborhood_response_df.groupby(['Neighborhood']).agg(['mean'])#, 'count'])


print_neighborhood_statistics = False

if (print_neighborhood_statistics):
	# Print neighborhoods
	neighborhoods = df_911['Neighborhood'].unique()

	print(neighborhoods.size)

	#Print data to terminal
	print(crime_neighborhood_response_incidents)

	#Create bar graph
	crime_neighborhood_response_incidents.plot(kind='bar')#camis_count.plot(kind='hist',bins=20)
	plt._show()


#Find closest neighbor using L2 norm (space should be locally cartesian)
def find_closest_neighborhood(vehicle_lat, vehicle_long):
	dist = 1.e20
	candidate_nbhd = ''
	for nbhd, latitude in latitude_dictionary.items():
		longitude = longitude_dictionary[nbhd]
		candidate_dist = np.sqrt(np.square(vehicle_lat - latitude) + np.square(vehicle_long - longitude))
		if (candidate_dist < dist):
			dist = candidate_dist
			candidate_nbhd = nbhd
	return candidate_nbhd

df_trimet['Neighborhood'] = df_trimet.apply(lambda x: find_closest_neighborhood(x['vehicle_location_latitude'], x['vehicle_location_longitude']), axis=1)


#Reduce dataframe to only neighborhood and delay info
trimet_neighborhood_delay_df = df_trimet[['Neighborhood', 'delay']].dropna(subset=['delay', 'Neighborhood'])
#Get mean trimet delay time associated with each neighborhood
trimet_neighborhood_delay_count = trimet_neighborhood_delay_df.groupby(['Neighborhood']).agg(['mean'])#, 'count'])

#Combine trimet and crime data frames
trimet_neighborhood_delay_count['Crime response (s)'] = crime_neighborhood_response_incidents
trimet_neighborhood_delay_count.columns = trimet_neighborhood_delay_count.columns.get_level_values(0)
trimet_neighborhood_delay_count.rename(columns={'delay': 'Trimet delay (s)'}, inplace=True)
trimet_neighborhood_delay_count.dropna(inplace=True)
#Print relationship to terminal
print(trimet_neighborhood_delay_count)
#Print corrleation value
print(trimet_neighborhood_delay_count.corr())

#Scatter plot relationship
trimet_neighborhood_delay_count.plot.scatter(x='Crime response (s)',y='Trimet delay (s)')
plt._show()