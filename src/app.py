from components import filterContainer, mainContainer
import callbacks
import dash_bootstrap_components as dbc
from dash import Dash, html


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="VanWeather Climate Tracker")
server = app.server
app.title = 'VanWeather'
#app._favicon = ()

# Import customized css file
html.Div(id='Header', children=[
    html.Link(
        rel='stylesheet',
        href='assets/app.css'
    )
])

# Doing the app layout
app.layout = html.Div([
    html.Div([filterContainer], className='nav_bar'), 
    html.Div([mainContainer], className='left_div'),
], className='main_div')

# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')
