import berrl as bl
import pandas as pd
from pipeleaflet import *
import numpy as np

# getting database
wv_roads = bl.get_database('routes')

# separating out road segments
interstates = wv_roads[wv_roads['signsystem'].astype(str) == '1']
us_routes = wv_roads[wv_roads['signsystem'].astype(str) == '2']
wv_routes = wv_roads[wv_roads['signsystem'].astype(str) == '3']
county_routes = wv_roads[wv_roads['signsystem'].astype(str) == '4']

colors = bl.get_heatmap51()
# setting color values
interstates['COLORKEY'] = colors[0]
us_routes['COLORKEY'] = colors[18]
wv_routes['COLORKEY'] = colors[36]
county_routes['COLORKEY'] = colors[-1]

# setting iterstate values
interstates['WGT'] = 5
us_routes['WGT'] = 3
wv_routes['WGT'] = 2
county_routes['WGT'] = 1

# concatenating all into one big dataframe
d = pd.concat([interstates,us_routes,county_routes,wv_routes])

bl.make_postgis_lines(d,'wvroutes.geojson')
a(styledicts=[{'color':'COLORKEY','weight':'WGT'}])