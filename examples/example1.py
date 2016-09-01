from pipeleaflet import *
import pandas as pd
import berrl as bl

# loading a csv file of traffic fatalities
fatalities = pd.read_csv('wv_fatalities.csv')

# making geojson of the csv file
bl.make_points(fatalities,filename='fatalities.geojson')

# parsing / writing out the html to index.html
load(['fatalities.geojson'])



