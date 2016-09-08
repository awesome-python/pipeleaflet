# PipeLeaflet - Simple Maps / Leaflet Visualizations 

This module was  mainly designed to use only leaflet APIs after having trouble embedding MapBox's API when trying to build a d3 dashboard. Something completely in leaflet and easy to use seemed necessary, I think its best or stuf like algorithm development and hopefully soon visualization. 

```
pip install pipeleaflet
```

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

![](https://cloud.githubusercontent.com/assets/10904982/18152204/29826368-6fc2-11e6-9e01-2c3304ad715a.png)

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

# making geojson of the csv file
bl.make_points(fatalities,filename='fatalities.geojson')

# parsing / writing out the html to index.html
# we now have colorkey fields to style by 
# colorkey fields are just 6-digit hex rgb strings 
load(['fatalities.geojson'],colorkey='COLORKEY')
```
![](https://cloud.githubusercontent.com/assets/10904982/18152205/298e14f6-6fc2-11e6-9b46-953ceac4cf69.png)

I often find myself using this fo things like algorithm development almost always with a SimpleHTTPServer as localhost, so if you use this module like I do you'll probably end up using the a() (which isn't necessarily recommended but its alot easier) function which is essentially a hacky make_html() method that grabs all geojsons in the current directory and LOADS AND OPENS the output in your browser. You can still pass the kwargs into a() method like you would load().

#### Other Useful Methods 
While pipeleaflet is mainly intended to only style objects for colors, method exists to style other aspects of objects either based on a column field or a static value for the whole file. Currently it supports 5 different visualization options. It accepts the options in a list of dictionary objects.
The objects it options it currently supports:
* color
* weight (Polygons / lines)
* radius (Points Only)
* opacity
* zooms

Zooms can accept 3 different types of values that have a different action, 1) the bool True, if this is sent in as the zooms dict value, the file will be active on all layers but the map will only load what is in the viewing window, 2) a lower zoom value and higher zoom value that indicates what range the file we'll be active, 3) two header values inserted like the integer zoom values as a list like the integer option previously. This will dynamically set the range in which the layer is active based on the values within a dataframe. If zooms values are given then pipeleaflet will assume you only want the viewing window to be values to be on the map. 

*Note for viewing windows for polygons / line segments, pipeleaflet expects a geojson file created with pipegeojson with kwargs "bounds = True", which creates an object in geojson that's interfacing the window bounds to do this operation.*

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

![](https://cloud.githubusercontent.com/assets/10904982/18152206/29932f7c-6fc2-11e6-972f-1a5f3488913b.png)

Finally I'll show an example of iterfacing with a postgis database and styling an entire database and based on roadway hierarchy and styling accordingly. Not that exciting but I still thought it would be worth showing a post_gis or larger example. For the record this isn't at all the most efficient way to do this in pandas I just didn't feel like writing an apply method that would be more confusing to look at anyway. 

```Python
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
```

![](https://cloud.githubusercontent.com/assets/10904982/18152408/98868efa-6fc3-11e6-9750-3a49c40710a7.png)

I'll add an example of how to display maps in Jupyter notebooks as well. (not hard)

Thats about all, its still a working process there are probably some bugs in logic etc., but things like zoom-level dependent layers and window-bound dependent object loading have already been implemented in other projects as well as pipegeojson already supporting a bounds api where the upperleft/lowerright extrema points of an object can be compared easily against the window boundries. The only problem is implementing it again without making a mess.  
