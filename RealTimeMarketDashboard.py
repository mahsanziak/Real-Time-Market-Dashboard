import dash
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objs as go


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Real-Time Market Data Dashboard"), width={'size': 6, 'offset': 3}, 
                className="text-center mt-5 mb-5")
    ),
    

    dbc.Row([
        dbc.Col([
            dcc.Input(
                id='stock-input',
                type='text',
                value='AAPL',  # Default ticker
                style={'width': '100%'},
            )
        ], width=6)
    ], justify="center"),


    dbc.Row([
        dbc.Col(dcc.Graph(id='live-stock-chart'), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.Div(id='stock-stats'), width={'size': 6, 'offset': 3}, 
                className="text-center")
    ]),

    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Interval at 60 sec
        n_intervals=0
    )
])

@app.callback(
    [Output('live-stock-chart', 'figure'),
     Output('stock-stats', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('stock-input', 'value')])
def update_graph_live(n, stock_ticker):
    stock = yf.Ticker(stock_ticker)
    df = stock.history(period="1d", interval="1m")

    if df.empty:
        return go.Figure(), "No data!"

    figure = go.Figure(data=[go.Candlestick(x=df.index,
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'],
                                            name='Candlestick')])
    figure.update_layout(title=f"Real-Time Stock Data for {stock_ticker}", 
                        xaxis_title='Time', 
                        yaxis_title='Price')

    stats = html.Div([
        html.P(f"Open: {df['Open'].iloc[-1]}", className="lead"),
        html.P(f"High: {df['High'].max()}", className="lead"),
        html.P(f"Low: {df['Low'].min()}", className="lead"),
        html.P(f"Close: {df['Close'].iloc[-1]}", className="lead")
    ])

    return figure, stats

if __name__ == '__main__':
    app.run_server(debug=True)
