import pandas as pd
import numpy as np
import scipy
import sklearn
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from tabulate import tabulate
#from kmodes.kmodes import KModes

from sklearn import decomposition


# Define file name
file_name_911 = '911-calls.csv'

# Import file as a pandas data frame
data_frame_911 = pd.read_csv(file_name_911)

#Set numpy seed
neighborhoods = data_frame_911['Neighborhood'].unique()

print(neighborhoods)

# Remove frames with scores < 0
