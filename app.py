import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import os
import networkx as nx

# Load correlation data
correlation_data = pd.read_csv("data/binance/top_10_correlation_matrix.csv", index_col=0)

# Load historical data
folder_path = "data/binance/top_10"
historical_data = {}

for file_name in os.listdir(folder_path):
    if file_name.endswith("_history_last_year.csv"):
        symbol = file_name.split("_")[0]
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)
        if all(col in data.columns for col in ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']):
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms', errors='coerce')
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            data = data.dropna(subset=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            historical_data[symbol] = data

# Build network graph for correlation
G = nx.Graph()
for i, row in correlation_data.iterrows():
    for j, value in row.items():
        if i != j and value > 0.6:  # Filter for strong correlations
            G.add_edge(i, j, weight=value)

pos = nx.spring_layout(G)
edge_x = []
edge_y = []
weights = []
for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    weights.append(edge[2]['weight'])

node_x = []
node_y = []
names = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    names.append(node)

# Initialize Dash app
app = dash.Dash(__name__)

# Get list of all symbols
symbols = list(historical_data.keys())

# Layout
app.layout = html.Div([
    html.H1("Cryptocurrency Analysis Dashboard", style={'text-align': 'center'}),

    # Section 1: Correlation Network
    html.Div([
        html.H2("Réseau de Corrélations des Cryptomonnaies"),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Scatter(x=edge_x, y=edge_y, mode='lines',
                               line=dict(width=2, color='gray'),
                               hoverinfo='none'),
                    go.Scatter(x=node_x, y=node_y, mode='markers+text',
                               marker=dict(size=10, color='blue'),
                               text=names, textposition="top center")
                ],
                layout=go.Layout(
                    title="Réseau des Corrélations",
                    showlegend=False,
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                    height=600
                )
            )
        )
    ]),

    # Section 2: Kline Data with Dropdown and Date Range Picker
    html.Div([
        html.H2("Évolution des Prix (Données Kline)"),
        html.Label("Sélectionnez une cryptomonnaie:"),
        dcc.Dropdown(
            id='currency-dropdown',
            options=[{'label': symbol, 'value': symbol} for symbol in symbols],
            value=symbols[0],  # Default selection
            style={'width': '50%'}
        ),
        html.Label("Sélectionnez une plage de dates:"),
        dcc.DatePickerRange(
            id='date-picker',
            start_date=historical_data[symbols[0]]['Timestamp'].min(),
            end_date=historical_data[symbols[0]]['Timestamp'].max(),
            display_format='YYYY-MM-DD'
        ),
        dcc.Graph(id='kline-chart'),
    ]),

    # Section 3: Individual Historical Data Graphs
    html.Div([
        html.H2("Graphiques Historiques"),
        html.Div([
            dcc.Graph(
                id=f"historical-{symbol}",
                figure=go.Figure(
                    data=[
                        go.Scatter(x=data['Timestamp'], y=data['Open'], name='Open', line=dict(color='blue')),
                        go.Scatter(x=data['Timestamp'], y=data['High'], name='High', line=dict(color='green')),
                        go.Scatter(x=data['Timestamp'], y=data['Low'], name='Low', line=dict(color='red')),
                        go.Scatter(x=data['Timestamp'], y=data['Close'], name='Close', line=dict(color='purple')),
                        go.Bar(x=data['Timestamp'], y=data['Volume'], name='Volume', marker_color='orange', yaxis='y2')
                    ],
                    layout=go.Layout(
                        title=f"{symbol} Open, High, Low, Close & Volume",
                        xaxis_title="Time",
                        yaxis_title="Price",
                        yaxis2=dict(title="Volume", overlaying="y", side="right"),
                        height=600
                    )
                )
            ) for symbol, data in historical_data.items()
        ])
    ])
])

# Callbacks
@app.callback(
    Output('kline-chart', 'figure'),
    [Input('currency-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_kline_chart(selected_currency, start_date, end_date):
    # Filter data for the selected currency and date range
    data = historical_data[selected_currency]
    filtered_data = data[(data['Timestamp'] >= start_date) & (data['Timestamp'] <= end_date)]

    # Generate candlestick chart
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=filtered_data['Timestamp'],
                open=filtered_data['Open'],
                high=filtered_data['High'],
                low=filtered_data['Low'],
                close=filtered_data['Close'],
                name=selected_currency
            )
        ],
        layout=go.Layout(
            title=f"Chandeliers Japonais {selected_currency}",
            xaxis_title="Temps",
            yaxis_title="Prix",
            height=600
        )
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
