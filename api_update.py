import requests
import time
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(
    Output("graph", "figure"),
    Input('interval-component', 'n_intervals'))
def display_candlestick(value):
    resolution = 15
    start_time = int(time.time()) - resolution * 240
    end_time = int(time.time())
    response = requests.get(
        f'https://ftx.com/api/markets/BTC-PERP/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}').json()['result']

    fig = go.Figure(data=[go.Candlestick(
                    x=list(e['startTime'] for e in response),
                    open=list(e['open'] for e in response),
                    high=list(e['high'] for e in response),
                    low=list(e['low'] for e in response),
                    close=list(e['close'] for e in response),
                    )])

    fig.update_layout(
        title='BTC-PERP ' + str(datetime.fromtimestamp(int(time.time()))),
        yaxis_title='Stock Price ($)',
        height=800,
    )

    fig.add_shape(
        type="line",
        x0=response[0]['startTime'], y0=response[-1]['close'], x1=response[-1]['startTime'], y1=response[-1]['close'],
        line=dict(
            color="blueviolet",
            width=1,
            dash="dashdot",
        )
    )

    fig.add_annotation(
        x=response[-1]['startTime'],
        y=response[-1]['close'],
        text=str(response[-1]['close']),
        showarrow=False,
        xshift=40,
        font=dict(
            color="blueviolet"
        ),
        bordercolor="blueviolet",
        borderwidth=1,
        borderpad=4,
    )

    return fig


app.run_server(debug=True)
