from flask import Flask, render_template
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import folium

server = Flask(__name__)

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/about')
def about():
    return render_template('about.html')

@server.route('/viz')
def viz():
    return render_template('viz.html')

app = Dash(__name__, server=server, url_base_pathname='/dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the data
df = pd.read_csv('combined_brd_perpoint_data.csv')
df['year'] = pd.to_datetime(df['startDate']).dt.year

# Load the count data
count_df = pd.read_csv('combined_brd_countdata_data.csv')
count_df['year'] = pd.to_datetime(count_df['startDate']).dt.year

# Map of site IDs to full names
site_names = {
    'ABBY': 'Abby Road',
    'BARR': 'Barrow Environmental Observatory',
    'BART': 'Bartlett Experimental Forest',
    'BLAN': 'Blandy Experimental Farm',
    'BONA': 'Bonanza Creek',
    'CLBJ': 'Caddo-LBJ National Grasslands',
    'CPER': 'Central Plains Experimental Range',
    'DCFS': 'Dakota Coteau Field School',
    'DEJU': 'Delta Junction',
    'DELA': 'Dead Lake',
    'DSNY': 'Disney Wilderness Preserve',
    'GRSM': 'Great Smoky Mountains National Park',
    'GUAN': 'Guanica Forest',
    'HARV': 'Harvard Forest',
    'HEAL': 'Healy',
    'JERC': 'Jones Ecological Research Center',
    'JORN': 'Jornada LTER',
    'KONZ': 'Konza Prairie Biological Station',
    'LAJA': 'Lajas Experimental Station',
    'LENO': 'Lenoir Landing',
    'MOAB': 'Moab',
    'NIWO': 'Niwot Ridge',
    'NOGP': 'Northern Great Plains Research Laboratory',
    'OAES': 'Klemme Range Research Station',
    'ONAQ': 'Onaqui',
    'ORNL': 'Oak Ridge',
    'OSBS': 'Ordway-Swisher Biological Station',
    'RMNP': 'Rocky Mountain National Park',
    'SCBI': 'Smithsonian Conservation Biology Institute',
    'SERC': 'Smithsonian Environmental Research Center',
    'SJER': 'San Joaquin Experimental Range',
    'SOAP': 'Soaproot Saddle',
    'SRER': 'Santa Rita Experimental Range',
    'STEI': 'Steigerwaldt Land Services',
    'STER': 'North Sterling',
    'TALL': 'Talladega National Forest',
    'TEAK': 'Lower Teakettle',
    'TOOL': 'Toolik',
    'TREE': 'Treehaven',
    'UKFS': 'University of Kansas Field Station',
    'UNDE': 'University of Notre Dame Environmental Research Center',
    'WOOD': 'Woodworth'
}
# Color mapping for years
color_mapping = {
    2017: '#FF5733',
    2018: '#33FF57',
    2019: '#3357FF',
    2020: '#FFFF33',
    2021: '#FF33FF',
    2022: '#FFA500'
}

def create_map():
    center_lat = df['decimalLatitude'].mean()
    center_lon = df['decimalLongitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['decimalLatitude'], row['decimalLongitude']],
            radius=5,
            popup=f"Year: {row['year']}, Site: {row['siteID']}",
            color=color_mapping.get(row['year'], '#000000'),
            fill=True,
            fillColor=color_mapping.get(row['year'], '#000000'),
            fillOpacity=0.7
        ).add_to(m)

    for site, name in site_names.items():
        site_data = df[df['siteID'] == site]
        if not site_data.empty:
            site_lat = site_data['decimalLatitude'].mean()
            site_lon = site_data['decimalLongitude'].mean()
            
            folium.Marker(
                location=[site_lat, site_lon],
                popup=folium.Popup(f'<span style="font-size: 14pt;"><b>{name}</b></span>', max_width=300),
                icon=folium.Icon(color='blue', icon='fa-dove', prefix='fa')
            ).add_to(m)
            
            folium.Circle(
                location=[site_lat, site_lon],
                radius=20000,
                color='gray',
                fill=True,
                fillColor='gray',
                fillOpacity=0.1,
                popup=folium.Popup(f'<span style="font-size: 14pt;"><b>{name}</b></span>', max_width=300)
            ).add_to(m)
        
        # Create a legend for the years
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 100px; height: auto; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:1px solid black; padding:10px;">
        <h4 style="margin-top:0;">Year</h4>
        '''

        for year, color in color_mapping.items():
            legend_html += f'<i style="background: {color}; width: 10px; height: 10px; float: left; margin-right: 5px; opacity:0.7; margin-top:5px;"></i>{year}<br>'

        legend_html += '</div>'

        m.get_root().html.add_child(folium.Element(legend_html))


    return m


app.layout = html.Div([
    html.H1("Bird Observation Dashboard"),
    html.Iframe(id='map', srcDoc=create_map().get_root().render(), width='100%', height='600'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': name, 'value': site} for site, name in site_names.items()],
        value=list(site_names.keys())[0],
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
        value=df['year'].max(),
        style={'width': '50%'}
    ),
    html.Div([
        dcc.Graph(id='species-density-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='observations-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='detection-method-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='species-count-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='temperature-graph', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='wind-speed-graph', style={'display': 'inline-block', 'width': '48%'})  
    ])
])

# Callback to update graphs
@app.callback(
    [Output('observations-graph', 'figure'),
     Output('temperature-graph', 'figure'),
     Output('wind-speed-graph', 'figure'),
     Output('species-count-graph', 'figure'),
     Output('detection-method-graph', 'figure'),
     Output('species-density-graph', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graphs(selected_site, selected_year):
    filtered_df = df[df['siteID'] == selected_site]
    filtered_count_df = count_df[count_df['siteID'] == selected_site]
    
    obs_data = filtered_count_df.groupby('year').size().reset_index(name='count')
    obs_fig = px.bar(obs_data, x='year', y='count', 
                     title=f"Number of Observations by Year - {site_names[selected_site]}")
    
    temp_fig = px.box(filtered_df, x='year', y='observedAirTemp', 
                      title=f"Air Temperature Distribution by Year - {site_names[selected_site]}")
    
    wind_fig = px.box(filtered_df, x='year', y='kmPerHourObservedWindSpeed', 
                      title=f"Wind Speed Distribution by Year - {site_names[selected_site]}")
    
    species_count = filtered_count_df.groupby('year')['scientificName'].nunique().reset_index()
    species_fig = px.line(species_count, x='year', y='scientificName', 
                          title=f"Number of Unique Species by Year - {site_names[selected_site]}")
    
    detection_method = filtered_count_df['detectionMethod'].value_counts().reset_index()
    detection_fig = px.pie(detection_method, values='count', names='detectionMethod', 
                           title=f"Distribution of Detection Methods - {site_names[selected_site]}")
    
    year_filtered_count_df = filtered_count_df[filtered_count_df['year'] == selected_year]
    species_density = year_filtered_count_df.groupby(['vernacularName', 'scientificName']).size().reset_index(name='count')
    
    density_fig = px.pie(species_density, values='count', names='vernacularName',
                         title=f"Species Population Density - {site_names[selected_site]} ({selected_year})",
                         hover_data=['scientificName'])
    
    density_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return obs_fig, temp_fig, wind_fig, species_fig, detection_fig, density_fig

# if __name__ == '__main__':
#     server.run(debug=True)

if __name__ == '__main__':
    app.run(port=4000, debug=True)