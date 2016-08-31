# PipeLeaflet - Simple Maps / Leaflet Visualizations 

This module relies heavily, on [pipegeojson](https://github.com/murphy214/pipegeojson) and/or [berrl](https://github.com/murphy214/berrl) in the sense that it relies essentially on pandas representations of geospatial objects to be parsed directly into geojson. Unlike other geojson parsing tools this carries every value in the dataframe into the geojson's properties meaning you can do some typical data analysis like visualizations extremely easily by controlling what geojson properties styles a geospatial object. 

This module is sort of the other side of geojson parsing, it takes a list of geojsons makes some assumptions about how it parsed (if it comes from the above it won't matter) and parses the appropriate javascript / html to load all geojson files you input. It also writes a popup context for every field in an object. So in other words fairly simple maps, that can be controlled by d3 like UI visualizations later on. 

