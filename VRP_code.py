#!/usr/bin/env python
# coding: utf-8

# In[42]:


# pip install networkx


# In[47]:


import networkx as nx


# In[44]:


# pip install scikit-learn


# In[52]:


import numpy as np


# In[49]:


import sklearn


# In[43]:


# pip install osmnx


# In[48]:


import osmnx as ox


# In[46]:


# pip install mapclassify


# In[53]:


import mapclassify


# In[50]:


import matplotlib


# In[45]:


# pip install folium


# In[51]:


import folium


# In[87]:


# pip install geopy


# In[88]:


from geopy.geocoders import Nominatim


# In[54]:


import pandas as pd


# In[83]:


import urllib.request, urllib.error, urllib.parse
import json


# ## Use networkx and osmnx to view nodes and edges of an area

# In[55]:


# download and model the street network for an area:
G = ox.graph_from_place("Rolesville, NC, USA", network_type="drive") # G is an input graph

# visualize it
ox.plot_graph(G)


# In[56]:


# Convert node and edge GeoDataFrames to a MultiDiGraph.

nodes, edges = ox.graph_to_gdfs(G)
nodes.head(5)


# Coordinates of starting and ending: (35.9264448,-78.4624239) ==> (35.9181458,-78.4686471)

# In[57]:


# get the nearest network node to the origin point and destination point (x (longitude) & y (latitude) coordinates)
orig_node = ox.nearest_nodes(G, X= -78.4624239, Y = 35.9264448)
dest_node = ox.nearest_nodes(G, X= -78.4686471, Y = 35.9181458)


# In[58]:


print(orig_node)
print(dest_node)


# In[59]:


# Solve shortest path from origin node(s) to destination node(s).
route = nx.shortest_path(G, orig_node, dest_node, 
                         weight='length') # find the shortest path by minimizing distance traveled 


# In[60]:


route


# In[61]:


ox.plot_graph_route(G, route) #, route_linewidth=6, node_size=0, bgcolor='k')


# ## Use osmnx.folium module to view nodes and edges of an area

# In[62]:


ox.plot_graph_folium(G)


# ## Use GeoDataFrame to color osmnx edges by areas

# In[63]:


place = ["Rolesville, NC", "Garner, NC", "Apex, NC"]
gdf_nodes = gdf_edges = None
for place in place:
    # Create graph from OSM within the boundaries of some geocodable place(s).
    G2 = ox.graph_from_place(place, retain_all=True, network_type='drive')
    # Convert node and edge GeoDataFrames to a MultiDiGraph.
    nodes2, edges2 = ox.graph_to_gdfs(G2)
    nodes2["place"] = place
    edges2["place"] = place
    if gdf_nodes is None:
        gdf_nodes = nodes2
        gdf_edges = edges2
    else:
        gdf_nodes = pd.concat([gdf_nodes, nodes2])
        gdf_edges = pd.concat([gdf_edges, edges2])

# returns Folium Map instance
gdf_edges.explore(column="place", cmap='spring', # matplotlib.Colormap
                  height=500, width=1000) 


# In[64]:


gdf_edges.head()


# ## Show route in a default background

# In[81]:


ox.plot_route_folium(G, route, color='#cc0000', weight=5, opacity=0.8)


# ## Show route in a not-so-transparent background

# In[82]:


# set up background
m1 = folium.Map()

# show route
ox.plot_route_folium(G, route, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# ## Impute a new speed column `speed_kph` on all edges missing `maxspeed` data
# 
# By default, this imputes free-flow travel speeds for all edges via the **mean maxspeed value** of the edges of each highway type. 
# 
# This default mean-imputation can obviously be imprecise, and the user can **override it by passing in hwy_speeds** and/or fallback arguments that correspond to local speed limit standards. 

# In[66]:


edges.head(3)


# No `speed_kph` yet

# In[67]:


edges.groupby('highway').count()['name'] # documentation: https://wiki.openstreetmap.org/wiki/Key:highway


# In[68]:


speed_dict = {'residential': 56.3, # Often lined with housing.
              'secondary': 88.5, # Often link towns.
              'primary': 88.5, # Often link larger towns
              'tertiary': 97} # Often link smaller towns and villages

G3 = ox.add_edge_speeds(G, hwy_speeds = speed_dict)

nodes3, edges3 = ox.graph_to_gdfs(G3)

edges3.head(3)


# In[69]:


# Calculates free-flow travel time along each edge, based on length and speed_kph attributes. 
G3 = ox.add_edge_travel_times(G3)

nodes3, edges3 = ox.graph_to_gdfs(G3)

edges3.head(3)


# Take the first row (`u=195423398` & `v=195595367`) as an example: 56.3 km_per_hr /(60x60) x 10.5 sec = 0.164 km = 164 m

# ## Compare two ways to solve shortest path

# In[70]:


route_length = nx.shortest_path(G3, orig_node, dest_node, 
                                weight='length') # find the shortest path by minimizing distance traveled 
route_time = nx.shortest_path(G3, orig_node, dest_node, 
                              weight='travel_time') # find the shortest path by minimizing distance traveled 


# In[71]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G3, route_length, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# In[72]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G3, route_time, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# Looks the same b/c the distance is too short

# ## Let's try on a longer travel

# In[73]:


G4 = ox.graph_from_place("Raleigh, USA", network_type="drive") 

ox.plot_graph(G4)


# In[74]:


node_r , edge_r = ox.graph_to_gdfs(G4)
x = []
for i in edge_r['highway'].values:
    if i not in x:
        x.append(i)
x


# In[75]:


G4 = ox.add_edge_speeds(G4, hwy_speeds = speed_dict)
G4 = ox.add_edge_travel_times(G4)

nodes4, edges4 = ox.graph_to_gdfs(G4)

# starting: 35.9158332,-78.4714274 #Rolesville Town Hall
# ending: 35.7891446,-78.8509757 #H mart @ Cary
orig_node4 = ox.nearest_nodes(G4, X= -78.4714274, Y = 35.9158332)
dest_node4 = ox.nearest_nodes(G4, X= -78.8509757, Y = 35.7891446)

route_length4 = nx.shortest_path(G4, orig_node4, dest_node4, weight='length')
route_time4 = nx.shortest_path(G4, orig_node4, dest_node4, weight='travel_time') 


# In[76]:


orig_node4


# In[77]:


dest_node4


# Minimal travel distance

# In[78]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G4, route_length4, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# Minimal travel time

# In[79]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G4, route_time4, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# Yay, the results are different now!

# ## Automatically get GeoLocation

# In[154]:


# Create GeoDataFrame of OSM entities within boundaries of geocodable place(s).
def make_graph_geocodable_place(places):
    if type(places) == list and len(places) > 1:
        
        print(places[0]+' is being graphed...')
        G = ox.graph_from_place(places[0], network_type="drive") 
        
        for i in range(1, len(places)):
            
            print(places[i]+' is being graphed...')            
            G1 = ox.graph_from_place(places[i], network_type="drive") 
            
            # Compose two graphs by combining nodes and edges into a single graph.
            G = nx.compose(G, G1) 
            
    else:
        G = ox.graph_from_place(places, network_type="drive") 
    
    print(ox.plot_graph(G))
    
    return G


# In[166]:


G_new = make_graph_geocodable_place(['Rolesville, NC', 'Raleigh, NC', 'Cary, NC', 'Wake Forest, NC', 'Apex, NC'])


# In[181]:


# Create GeoDataFrame of OSM entities within some distance N, S, E, W of a point.
def make_graph_point(point, dist=50000): 
    G = ox.graph_from_point(point, dist=dist, # dist is in meters
                            network_type="drive") 
    
    print(ox.plot_graph(G))
    
    return G


# In[119]:


def get_geoloc(name):
    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    getLoc = loc.geocode(name)
 
    print(getLoc.address)
    print(getLoc.latitude, getLoc.longitude,'\n')
    
    return getLoc.latitude, getLoc.longitude


# In[182]:


G_new = make_graph_point(get_geoloc('Raleigh'))


# In[183]:


orig_coor = get_geoloc('Rolesville Town Hall')
dest_coor = get_geoloc('UNC at Chapel Hill')


# In[121]:


def get_orig_dest_nodes(G, orig_coor, dest_coor):
    orig_node = ox.nearest_nodes(G, X= orig_coor[1], Y = orig_coor[0])
    dest_node = ox.nearest_nodes(G, X= dest_coor[1], Y = dest_coor[0])
    
    return orig_node, dest_node


# In[184]:


orig_node, dest_node = get_orig_dest_nodes(G_new, origin_coor, dest_coor)


# In[123]:


def get_shortest_route(G, orig_node, dest_node, method):
    return nx.shortest_path(G, orig_node, dest_node, weight=method) 


# Minimal travel distance

# In[224]:


r_length = get_shortest_route(G_new, orig_node, dest_node, method='length')

m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G_new, r_length, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# Minimal travel time

# In[225]:


r_time = get_shortest_route(G_new, orig_node, dest_node, method='travel_time')

m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G_new, r_time, route_map=m1, color='#cc0000', weight=5, opacity=0.8)


# ## Get the distance

# #### use built-in function

# In[187]:


ox.distance.euclidean_dist_vec(orig_coor[0], orig_coor[1], dest_coor[0], dest_coor[1])


# Above is in coordinates’ unit. For 69.172 miles per degree, 0.576 coordinate unit equals 39.8 miles. It is pretty close to the 37.8 miles on Google Map.

# #### use edge data

# In[238]:


edges_new.head()


# In[228]:


def get_geodf(G):
    return ox.graph_to_gdfs(G)


# In[229]:


nodes_new, edges_new = get_geodf(G_new)


# In[233]:


def calculate_distance(route, edges):
    dist_in_miles = 0
    
    for i in range(0, len(route)-1):
        q = 'u=='+str(route[i])+' and v=='+str(route[i+1])
        dist_in_meter = edges.query(q)['length'].values
        dist_in_miles += float(dist_in_meter) * 0.000621371
    
    return str(round(dist_in_miles,2))


# In[235]:


print('The distance of shortest route by travel distance: ' +calculate_distance(r_length, edges_new)+' miles.')


# In[236]:


print('The distance of shortest route by travel time: ' +calculate_distance(r_time, edges_new)+' miles.')


# ## Get the time

# In[243]:


speed_dict = {'residential': 56.3, # Often lined with housing.
              'secondary': 88.5, # Often link towns.
              'primary': 88.5, # Often link larger towns
              'tertiary': 97} # Often link smaller towns and villages

def impute_speed_and_time(G, speed_dict=speed_dict):
    # first add speed data and then calculate travel_times
    G = ox.add_edge_speeds(G, hwy_speeds = speed_dict)
    G = ox.add_edge_travel_times(G)
    
    # Convert a MultiDiGraph to node and/or edge GeoDataFrames.
    return ox.graph_to_gdfs(G)


# In[244]:


nodes, edges = impute_speed_and_time(G_new)


# In[265]:


edges.head()


# Take the (`u=169878919` , `v=169878923`) for an example, `speed_kph` 56.3 = 56300 meters per hour = 938(*=56300/60*) meters per minute.
# 
# `length` 249.216 is in meters, so 249.216/938 = 0.26 minutes = 15.6 seconds
# 
# `travel_time` is in seconds.

# In[274]:


def calculate_time(route, edges):
    duration = 0
    
    for i in range(0, len(route)-1):
        q = 'u=='+str(route[i])+' and v=='+str(route[i+1])
        d = edges.query(q)['travel_time'].values
        duration += np.round(d, 2)
    
    return str(float(duration)/60) # seconds / 60 = minutes


# In[275]:


print('The duration of shortest route by travel distance: ' +calculate_time(r_length, edges)+' minutes.')


# In[276]:


print('The duration of shortest route by travel time: ' +calculate_time(r_time, edges)+' minutes.')


# ## Consider parking tolls

# ## Consider the delivery window

# In[ ]:




