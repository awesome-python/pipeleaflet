from pipeleaflet import *
import pandas as pd
import berrl as bl
import numpy as np

# loading a csv file of traffic fatalities
fatalities = pd.read_csv('wv_fatalities.csv')

# Adding the COLORKEY field by iterating through categorriclas of
# the input field in this case the field represents causes of traffic fatalities
# A field called COLORKEY if automatically added behind the scenes
# a groupby and a generator is all thatas going on 
fatalities = bl.unique_groupby(fatalities,'VAR23C')
print fatalities

# making geojson of the csv file
bl.make_points(fatalities,filename='fatalities.geojson')

# parsing / writing out the html to index.html
# we now have colorkey fields to style by 
# colorkey fields are just 6-digit hex rgb strings 
load(['fatalities.geojson'],colorkey='COLORKEY')
