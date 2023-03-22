# Vehicle Routing Workbook

`VRP_code.ipynb` is a playbook for exercising point-to-point questions.

`routing_with_xy_coordinates.ipynb` is a playbook for exercising the routing questions.

## From Point to Point 

- How to display an area graph which consists of nodes (intersection) and edges (paths)?

- How to identify a node closest to a specific location?

- How to find the shortest route between locations?

- How to figure out the best route in terms of travel time or travel distance?

## From The Routing Perspective

According to Wikipedia, 

> The vehicle routing problem is a combinatorial optimization and integer programming problem which asks "What is the optimal set of routes for a fleet of vehicles to traverse in order to deliver to a given set of customers?" 

<img src="https://github.com/kellychin79/vehicle_routing/blob/main/image.png" width="500" height="300" alt="me" />

<sub><sup>source: https://www.researchgate.net/figure/The-Capacitated-Vehicle-Routing-Problem-Scheme-The-capacitated-vehicle-routing-problem_fig1_285712366</sup></sub>

If there are 1 depo and 5 destinations, all possible paths are 4 * 3 * 2 = 24 paths. For 1 vehicle, we want to find the best route of 6 paths (1 path to 1 destination + back to depo). 

The performance was fairly fine in getting solutions within 1 second for 3 to 8 destinations. The runtime increased to 15 seconds for 9 destinations and had exponential increase to 165 seconds when it reaches 10 desintaions.

## Considering multiple vehicles...

___


### Packages

#### OSMnx https://osmnx.readthedocs.io/en/stable/
 A Python package that lets you download geospatial data from OpenStreetMap and model, project, visualize, and analyze real-world street networks and any other geospatial geometries. 
*Required dependencies: sklearn, numpy.core.multiarray*

#### NetworkX https://networkx.org/documentation/stable/reference/functions.html
A Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

#### Folium https://python-visualization.github.io/folium/
A Python library gives you access to the mapping strengths of the Leaflet JavaScript library. It allows you to create interactive geographic visualizations that you can share as a website.
*Required dependencies: numba, mapclassify, matplotlib*

