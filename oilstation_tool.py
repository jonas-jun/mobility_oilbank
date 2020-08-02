import pandas as pd
import numpy as np
from haversine import haversine
import folium

class mj_tools:

    def __init__(self, df):
        self.df = df

    def get_near_stations(self, name, distance):

        if name not in list(df['name']):
            raise ValueError ('this station is not in the dataframe')

        self.drop_dup = self.df.drop_duplicates(['name'])
        self.arr = np.array(self.drop_dup)
        lat = np.array(self.drop_dup['lat'])
        lon = np.array(self.drop_dup['lon'])
        idx_ = list(self.drop_dup['name'].index(name))

