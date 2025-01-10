import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# Load the trading pairs information file
data_path = "data/binance/top_50_usdt_pairs_by_price_volume.csv"
data = pd.read_csv(data_path)

# Ensure numeric columns
data['Min Price'] = pd.to_numeric(data['Min Price'], errors='coerce')
data['Max Qty'] = pd.to_numeric(data['Max Qty'], errors='coerce')
data['Score'] = pd.to_numeric(data['Score'], errors='coerce')

# Initialize the Dash app
app = Dash(__name__)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Top 50 USDT Trading Pairs Dashboard", style={"textAlign": "center"}),

    # Filters
    html.Div([
        html.Label("Filter by Min Price:"),
        dcc.RangeSlider(
            id='price-slider',
            min=data['Min Price'].min(),
            max=data['Min Price'].max(),
            step=0.01,
            marks={int(val): str(int(val)) for val in data['Min Price'].unique()[::10]},
            value=[data['Min Price'].min(), data['Min Price'].max()]
        ),

        html.Label("Filter by Max Quantity:"),
        dcc.RangeSlider(
            id='volume-slider',
            min=data['Max Qty'].min(),
            max=data['Max Qty'].max(),
            step=1000,
            marks={int(val): str(int(val)) for val in data['Max Qty'].unique()[::10]},
            value=[data['Max Qty'].min(), data['Max Qty'].max()]
        ),
    ], style={"margin": "20px"}),

    # Data table
    dash_table.DataTable(
        id='trading-pairs-table',
        columns=[
            {"name": col, "id": col} for col in data.columns
        ],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
        style_header={"backgroundColor": "#f2f2f2", "fontWeight": "bold"}
    ),

    # Visualization
    dcc.Graph(id='scatter-plot')
])

# Callbacks for interactivity
@app.callback(
    [
        Output('trading-pairs-table', 'data'),
        Output('scatter-plot', 'figure')
    ],
    [
        Input('price-slider', 'value'),
        Input('volume-slider', 'value')
    ]
)
def update_dashboard(price_range, volume_range):
    # Filter data based on sliders
    filtered_data = data[
        (data['Min Price'] >= price_range[0]) &
        (data['Min Price'] <= price_range[1]) &
        (data['Max Qty'] >= volume_range[0]) &
        (data['Max Qty'] <= volume_range[1])
    ]

    # Scatter plot for visualization
    scatter_fig = px.scatter(
        filtered_data,
        x='Min Price',
        y='Max Qty',
        size='Score',
        color='Symbol',
        hover_name='Symbol',
        title="Scatter Plot of Min Price vs Max Quantity",
        labels={"Min Price": "Minimum Price", "Max Qty": "Maximum Quantity"}
    )

    return filtered_data.to_dict('records'), scatter_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
