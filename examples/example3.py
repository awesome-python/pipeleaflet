import pandas as pd
import berrl as bl
from pipeleaflet import *

data1 = pd.read_csv('polygon_example.csv')
data2 = pd.read_csv('points_example.csv')
data3 = pd.read_csv('line_example.csv')
data4 = pd.read_csv('blocks_example.csv')

bl.make_polygon(data1,filename='polygon.geojson')
bl.make_points(data2,filename='points.geojson')
bl.make_line(data3,filename='line.geojson')

dictrow1 = {'color':'#25D2EA','weight':10}
dictrow2 = {'color':'#CC33FF','radius':1}
dictrow3 = {'color':'#FFE800','weight':20}

filenames = ['polygon.geojson','points.geojson','line.geojson']
stylerows = [dictrow1,dictrow2,dictrow3,dictrow4]

load(filenames,stylerows=stylerows)

