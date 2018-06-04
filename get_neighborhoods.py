import pandas as pd
import numpy as np
import scipy
import sklearn
import matplotlib.pyplot as plt


# Define file name
file_name_911 = '911-calls.csv'

# Import file as a pandas data frame
data_frame_911 = pd.read_csv(file_name_911)

# Print neighborhoods
neighborhoods = data_frame_911['Neighborhood'].unique()

print(neighborhoods.size)

#Reduce dataframe to only neighborhood and response time info
crime_neighborhood_response_df = data_frame_911[['Neighborhood', 'Response Time (sec)']].dropna(subset=['Response Time (sec)'])#.groupby('Neighborhood').count().iloc[:,0]
#Get mean response time and count statistics associated with each neighborhood
crime_neighborhood_response_incidents = crime_neighborhood_response_df.groupby(['Neighborhood']).agg(['mean', 'count'])

#Print data to terminal
print(crime_neighborhood_response_incidents)

#Create bar graph
crime_neighborhood_response_incidents.plot(kind='bar')#camis_count.plot(kind='hist',bins=20)
plt._show()
