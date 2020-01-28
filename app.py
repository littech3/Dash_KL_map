import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

app = dash.Dash(__name__, meta_tags = [{"name": "viewport", "content": "width=device-width"}])
server = app.server

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

list_of_locations = {
    "Aceras Office": {"lat": 3.1117915, "lon": 101.6650816},
    "Mid Valley": {"lat": 3.118384, "lon": 101.6754279},
    "KLCC Twin Towers": {"lat": 3.1579361, "lon": 101.7118006},
    "KL Tower": {"lat": 3.1528496, "lon": 101.7015546},
}

# Initialize data frame
df = pd.read_csv("C:\\Users\\tecktze\\Desktop\\Dash\\map\\data.csv")
list_of_category = df['Category'].unique()

# Layout of Dash App
app.layout = html.Div(
    children = [
        html.Div(
            className = "row",
            children = [
                # Column for user controls
                html.Div(
                    className = "four columns div-user-controls",
                    children = [
                        html.Img(className = "logo", src = app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H2("DASH - KL MAP APP"),
                        html.Div(
                            className = "row",
                            children = [
                                html.Div(
                                    className = "div-for-dropdown",
                                    children = [
                                        dcc.Dropdown(
                                            id = "location-dropdown", 
                                            options = [
                                                {"label": i, "value": i} 
                                                for i in list_of_locations
                                            ],
                                            placeholder = "Select a location",
                                        )
                                    ]
                                ),
                                html.Div(
                                    className = "div-for-dropdown",
                                    children = [
                                        # Dropdown to select category
                                        dcc.Dropdown(
                                            id = "bar-selector",
                                            options = [
                                                {"label": i , "value": i} for i in list_of_category
                                            ],
                                            multi = True, 
                                            placeholder = "Select category",
                                        )
                                    ]
                                )
                            ],
                        ),
                        html.P(id = "total-locations"),
                        html.P(id = "total-locations-selection")
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className = "eight columns div-for-charts bg-grey",
                    children = [
                        dcc.Graph(id = "map-graph"),
                    ]
                ),
            ],
        ),
    ]
)

# Show total number of locations based on selection
@app.callback(
    Output("total-locations", "children"),
    [Input("bar-selector", "value")],
)
def update_total_locations(list_of_category):

    print(type(list_of_category))
    if list_of_category:
        
        count =  df[df['Category'].isin(list_of_category)].shape[0]
        return "Locations in selected category: {:,d}".format(count)    

# Update Map Graph based on category picker and location dropdown
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("bar-selector", "value"),
        Input("location-dropdown", "value")
    ]
)
def update_graph(list_of_category, selectedLocation):
    zoom = 12.0
    latInitial = 3.1397306
    lonInitial = 101.6644228
    bearing = 0

    if selectedLocation:
        zoom = 15.0
        latInitial = list_of_locations[selectedLocation]["lat"]
        lonInitial = list_of_locations[selectedLocation]["lon"]
    
    if list_of_category:
        dff = df[df['Category'].isin(list_of_category)]
    else:
        dff = df

    def SetColor(x):
        if(x == "Shopping Mall"):
            return "orange"
        elif(x == "Office"):
            return "red"
        else:
            return "black"

    return go.Figure(
        data = [
            Scattermapbox(
                lat = dff["Lat"],
                lon = dff["Lon"],
                mode = "markers",
                hoverinfo="lat+lon+text",
                text= dff["Place"],
                marker = dict(
                    color = list(map(SetColor, dff["Category"])),
                    size = 15
                )
            ),
            #Scattermapbox(
            #    lat = [list_of_locations[i]["lat"] for i in list_of_locations],
            #    lon = [list_of_locations[i]["lon"] for i in list_of_locations],
            #    mode = "markers",
            #    hoverinfo = "text", 
            #    text = [i for i in list_of_locations],
            #    marker = dict(size = 8, color = "#ffa0a0"),
            #)
        ],
        layout = Layout(
            autosize = True,
            margin = go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox = dict(
                accesstoken = mapbox_access_token,
                center = dict(lat = latInitial, lon = lonInitial),
                style = "open-street-map",
                bearing = bearing,
                zoom = zoom 
            ),
            updatemenus = [
                dict(
                    buttons = (
                        [
                        dict(
                            args=[
                                {
                                "mapbox.zoom": 12,
                                "mapbox.center.lon": 101.6644228,
                                "mapbox.center.lat": 3.1397306,
                                "mapbox.bearing": 0,
                                "mapbox.style": "dark",
                                }
                            ],
                            label = "Reset Zoom",
                            method = "relayout", 
                        )
                    ]
                    ),
                    direction = "left", 
                    pad = {"r": 0, "t": 0, "b": 0, "l":0},
                    showactive = False,
                    type = "buttons",
                    x = 0.45,
                    y = 0.02,
                    xanchor = "left",
                    yanchor = "bottom",
                    bgcolor = "#323130",
                    borderwidth = 1,
                    bordercolor = "#6d6d6d",
                    font = dict(color="#FFFFFF"),
                )
            ],
        ),
    )

if __name__ == "__main__":
    app.run_server(debug = True)
