# PipeLeaflet - Simple Maps / Leaflet Visualizations 

This module relies heavily, on [pipegeojson](https://github.com/murphy214/pipegeojson) and/or [berrl](https://github.com/murphy214/berrl) in the sense that it relies essentially on pandas representations of geospatial objects to be parsed directly into geojson. Unlike other geojson parsing tools this carries every value in the dataframe into the geojson's properties meaning you can do some typical data analysis like visualizations extremely easily by controlling what geojson properties styles a geospatial object. 

This module is sort of the other side of geojson parsing, it takes a list of geojsons filenames makes some assumptions about how it parsed (if it comes from the above it won't matter) and parses the appropriate javascript / html to load all geojson files you input. It also writes a popup context for every field in an object. So in other words fairly simple maps, that can be controlled by d3 like UI visualizations later on. 

#### How Does It Work?
The API to use this module is about as simple as it gets, basically at its most basic a list of geojson filenames in your current directory is all thats need to load a map. The main function / method is load() which by default accepts a list of geojsons. Below shows an example of me creating a map of traffic fatalities in my state. 

```Python
from pipeleaflet import *
import pandas as pd
import berrl as bl

# loading a csv file of traffic fatalities
fatalities = pd.read_csv('wv_fatalities.csv')

# making geojson of the csv file
bl.make_points(fatalities,filename='fatalities.geojson')

# parsing / writing out the html to index.html
load(['fatalities.geojson'])
```

Picture 1 Here

Of course being able to pass things between a dataframe and the representation of said items means you can style by fields and categoricals or combination of either / or in the next example I'll show how easy it is to style by adding a COLORKEY field to the entire dataframe. Below I'm simply doing a pandas groupby of a categorical value in the dataframe in this case the crash causes and apply a different color for every unique value in the field. 

```Python
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
```
Picture 2 Here

I often find myself using this fo things like algorithm development almost always with a SimpleHTTPServer as localhost, so if you use this module like I do you'll probably end up using the a() (which isn't necessarily recommended but its alot easier) function which is essentially a hacky make_html() method that grabs all geojsons in the current directory and LOADS AND OPENS the output in your browser. You can still pass the kwargs into a() method like you would load().

#### Other Useful Methods 
While pipeleaflet is mainly intended to only style objects for colors, method exists to style other aspects of objects either based on a column field or a static value for the whole file. Currently it supports 4 different visualization options. It accepts the options in a list of dictionary objects.
The objects it options it currently supports:
* color
* weight (Polygons / lines)
* radius (Points Only)
* opacity

The implementation tries to infer whether an entry is a field or a static input for the file, but no guarantees,if you wish to simply load a file under default conditions you can put an empty dict,False bool, or empty list into its position and the list and file will load under default conditions.

The example below shows the four main objects I use and there data dataframe representation. As well as some random styling inputs. 

```Python
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
styledicts = [dictrow1,dictrow2,dictrow3,dictrow4]

load(filenames,styledicts=styledicts)
```

Picture 3 here

Finally I'll show an example of iterfacing with a postgis database and styling an entire database and based on roadway hierarchy and styling accordingly. Not that exciting but I still thought it would be worth showing a post_gis or larger example. 

