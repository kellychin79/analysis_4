#!/usr/bin/env python
# coding: utf-8

# In[255]:


# pip install networkx


# In[256]:


# pip install osmnx


# In[257]:


# pip install scikit-learn


# In[258]:


# pip install folium


# In[259]:


# pip install mapclassify


# In[260]:


import networkx as nx


# In[261]:


import osmnx as ox


# In[262]:


import sklearn


# In[263]:


import matplotlib


# In[264]:


import folium


# In[265]:


import numpy as np


# In[266]:


import mapclassify


# In[267]:


import pandas as pd


# ## Use networkx and osmnx to view nodes and edges of an area

# In[268]:


# download and model the street network for an area:
G = ox.graph_from_place("Rolesville, NC, USA", network_type="drive") # G is an input graph

# visualize it
ox.plot_graph(G)


# Coordinates of starting and ending: (35.9264448,-78.4624239) ==> (35.9181458,-78.4686471)

# In[269]:


# get the nearest network node to the origin point and destination point (x (longitude) & y (latitude) coordinates)
orig_node = ox.nearest_nodes(G, X= -78.4624239, Y = 35.9264448)
dest_node = ox.nearest_nodes(G, X= -78.4686471, Y = 35.9181458)


# In[270]:


print(orig_node)
print(dest_node)


# In[271]:


# Solve shortest path from origin node(s) to destination node(s).
route = nx.shortest_path(G, orig_node, dest_node, 
                         weight='length') # find the shortest path by minimizing distance traveled 


# In[272]:


route


# In[273]:


ox.plot_graph_route(G, route) #, route_linewidth=6, node_size=0, bgcolor='k')


# ## Use osmnx.folium module to view nodes and edges of an area

# In[274]:


ox.plot_graph_folium(G)


# In[275]:


nodes.head(5)


# ## Use GeoDataFrame to color osmnx edges by areas

# In[276]:


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


# In[277]:


gdf_edges.head()


# ## Show route in a not-so-transparent background

# In[278]:


# set up background
m1 = folium.Map()

# show route
ox.plot_route_folium(G, route, route_map=m1, tiles = 'asss', color='#cc0000', weight=5, opacity=0.8)


# ## Impute a new speed column `speed_kph` on all edges missing `maxspeed` data
# 
# By default, this imputes free-flow travel speeds for all edges via the **mean maxspeed value** of the edges of each highway type. 
# 
# This default mean-imputation can obviously be imprecise, and the user can **override it by passing in hwy_speeds** and/or fallback arguments that correspond to local speed limit standards. 

# In[279]:


edges.head(3)


# In[280]:


sorted(np.array(edges['speed_kph'].unique()))


# In[281]:


edges.groupby('highway').count()['name'] # documentation: https://wiki.openstreetmap.org/wiki/Key:highway


# In[282]:


speed_dict = {'residential': 56.3, # Often lined with housing.
              'secondary': 88.5, # Often link towns.
              'primary': 88.5, # Often link larger towns
              'tertiary': 97} # Often link smaller towns and villages

G3 = ox.add_edge_speeds(G, hwy_speeds = speed_dict)

nodes3, edges3 = ox.graph_to_gdfs(G3)

edges3.head(3)


# In[283]:


sorted(np.array(edges3['speed_kph'].unique()))


# In[284]:


# Calculates free-flow travel time along each edge, based on length and speed_kph attributes. 
G3 = ox.add_edge_travel_times(G3)

nodes3, edges3 = ox.graph_to_gdfs(G3)

edges3.head(3)


# Take the first row (`v=195595367`) as an example: 56.3 km_per_hr /(60x60) x 10.5 sec = 0.164 km = 164 m

# ## Compare two ways to solve shortest path

# In[285]:


route_length = nx.shortest_path(G3, orig_node, dest_node, 
                                weight='length') # find the shortest path by minimizing distance traveled 
route_time = nx.shortest_path(G3, orig_node, dest_node, 
                              weight='travel_time') # find the shortest path by minimizing distance traveled 


# In[286]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G3, route_length, route_map=m1, tiles = 'asss', color='#cc0000', weight=5, opacity=0.8)


# In[287]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G3, route_time, route_map=m1, tiles = 'asss', color='#cc0000', weight=5, opacity=0.8)


# Looks the same b/c the distance is too short

# In[288]:


## Let's try on a longer travel
G4 = ox.graph_from_place("Raleigh, USA", network_type="drive") 

ox.plot_graph(G4)


# In[289]:


node_r , edge_r = ox.graph_to_gdfs(G4)
x = []
for i in edge_r['highway'].values:
    if i not in x:
        x.append(i)
x


# In[290]:


G4 = ox.add_edge_speeds(G4, hwy_speeds = speed_dict)
G4 = ox.add_edge_travel_times(G4)

nodes4, edges4 = ox.graph_to_gdfs(G4)

# starting: 35.9158332,-78.4714274 
# ending: 35.7891446,-78.8509757 #h mart
orig_node4 = ox.nearest_nodes(G4, X= -78.4714274, Y = 35.9158332)
dest_node4 = ox.nearest_nodes(G4, X= -78.8509757, Y = 35.7891446)

route_length4 = nx.shortest_path(G4, orig_node4, dest_node4, weight='length')
route_time4 = nx.shortest_path(G4, orig_node4, dest_node4, weight='travel_time') 


# In[291]:


orig_node4


# In[292]:


dest_node4


# In[293]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G4, route_length4, route_map=m1, tiles = 'asss', color='#cc0000', weight=5, opacity=0.8)


# In[294]:


m1 = folium.Map(height=400, width=600)
ox.plot_route_folium(G4, route_time4, route_map=m1, tiles = 'asss', color='#cc0000', weight=5, opacity=0.8)


# Yay, different now!

# In[ ]:




