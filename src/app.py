from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container(
    [
    dbc.Row([

        dbc.Col([dbc.Row(html.Div("Filters")), 
                dbc.Row(html.Div("Filter1")),
                dbc.Row(html.Div("Filter2")),
                dbc.Row(html.Div("Filter3")),
        ],
                md=2),
        dbc.Col(
            [
                dbc.Row(html.Div("VanWeather - Vancouver Climate Extreams Dash")),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div("KPI 1"),
                            html.Div("KPI 2"),
                            html.Div("KPI 3"),
                        ],
                            style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'}
                        ),
                    ]),
                    dbc.Col(html.Div("Static time series")),
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div("Dynamic time series")),
                        dbc.Col(html.Div("Dynamic time series")),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div("Dynamic time series")),
                        dbc.Col(html.Div("Dynamic time series")),
                    ])
                ]),
            ]
        ),
        ])
    ]
)

# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    # app.run(debug=True)
    app.server.run(debug=True, port=8080, host='127.0.0.1')