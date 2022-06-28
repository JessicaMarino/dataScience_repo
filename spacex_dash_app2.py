#import wget
#url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
#wget.download(url)
#url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget.download(url)

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label':'CCAFS LC-40','value':'CCAFS LC-40'},{'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                            {'label':'KSC LC-39A','value':'KSC LC-39A'},{'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={str(kg): str(kg) for kg in range(0, 10000, 1000)},
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add a callback function in spacex_dash_app.py
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        total_success = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(total_success, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        total_success = filtered_df['class'].value_counts().reset_index()
        fig = px.pie(total_success, values='class', 
        names='index', 
        title=('Total Success Launches in '+ entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'), 
    Input('payload-slider', 'value')
)    
def get_scatter_chart(entered_site, payload_range):
    limits_kg = payload_range

    inRange = spacex_df[(spacex_df['Payload Mass (kg)']>=limits_kg[0])&(spacex_df['Payload Mass (kg)']<=limits_kg[1])]

    if entered_site == 'ALL':
        fig = px.scatter(inRange, x='Payload Mass (kg)', y='class', color="Booster Version Category",
         #   title='Correlation between Payload and Success for all Sites')
         title = str(limits_kg))
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[inRange['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
            title=('Correlation between Payload and Success for ' + entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=3007) 