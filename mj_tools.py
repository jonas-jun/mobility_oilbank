import pandas as pd
import numpy as np
from haversine import haversine
import folium

class check_price:

    def __init__(self, df):
        self.df = df
        self.df_rm = self.df.drop_duplicates(['address'])
        self.arr = np.array(self.df)
        self.arr_rm = np.array(self.df_rm)

    def check_duplicate(self, name):
        '''
        check there is any other station who has same name
        :param name: name of station to check
        :return: list of stations
        '''
        if name not in list(self.df['name']):
            raise ValueError ('this station is not in the dataframe')

        self.arr_except_target = np.array(self.df_rm.loc[self.df_rm['name']!=name])

        self.target = list()
        for i in range(len(self.arr_rm)):
            if self.arr_rm[i][0] == name:
                self.target.append(self.arr_rm[i])

        return self.target

    def get_near_by_idx(self, idx, distance):

        if idx not in list(range(len(self.target))):
            raise IndexError ('put reliable index in')

        loc_a = (self.target[idx][-2], self.target[idx][-1])

        self.result1 = list()
        for i in range(len(self.arr_except_target)):
            loc_b = (self.arr_except_target[i][-2], self.arr_except_target[i][-1])
            if haversine(loc_a, loc_b) <= distance:
                self.result1.append(self.arr_except_target[i])

        return self.result1

    def get_average(self, year, month, week):
        '''
        :return: mean price of other stations in get_near_by_idx when input date
        '''
        self.date = '{}년 {:02}월 {}주'.format(year, month, week) # 입력 날짜 포맷 변경
        print('지정한 날짜는: {}'.format(self.date))

        # 주소만 list로 뽑아내기
        self.address = list()
        for i in range(len(self.result1)):
            self.address.append(self.result1[i][1])

        # 근처의 경쟁사 주유소들의 해당 날짜 정보 추출
        self.result2 = list()
        for i in range(len(self.arr)):
            if self.arr[i][1] in self.address and self.arr[i][2] == self.date and self.arr[i][3] != '현대오일뱅크':
                self.result2.append(self.arr[i])
        print('해당 날짜의 근처 경쟁사들의 정보:')
        print(self.result2)

        # 가솔린과 디젤 가격 평균 계산
        self.prices = dict()
        for i in self.result2:
            self.prices.setdefault('G', []).append(i[6])
            self.prices.setdefault('D', []).append(i[7])
        mean_G, mean_D = np.mean(self.prices['G']), np.mean(self.prices['D'])
        return mean_G, mean_D


class mapping:
    '''
    folium mapping class
    you should input DataFrame format,
    and need columns ['name', 'do_brand', 'self', 'lat', 'lon]
    '''
    def __init__(self, zoom_start=8):
        self.m = folium.Map(location = [36.5053542, 127.70434191], zoom_start=zoom_start)

    def add_circle(self, df, color, radius=5):

        self.df = df
        c_options = ['beige', 'black', 'blue', 'cadetblue', 'darkblue', 'darkgreen', 
        'darkpurple', 'darkred', 'gray', 'green', 'lightblue', 'lightgray', 'lightgreen', 
        'lightred', 'orange', 'pink', 'purple', 'red', 'white']
        if color not in c_options:
            raise ValueError ('Invalid color option')
        
        for i in range(len(self.df)):
            folium.CircleMarker(location=[list(self.df.lat)[i], list(self.df.lon)[i]],
                popup=list(self.df.name)[i], color=color, radius=radius).add_to(self.m)
        
        print('added {} points!'.format(len(self.df)))
        
    def export_map(self, filename):
        self.filename = str(filename)+'.html'
        self.m.save(self.filename)