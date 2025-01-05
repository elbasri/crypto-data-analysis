# Cryptocurrency Data Analysis and Visualization Dashboard

This repository contains a comprehensive project for analyzing and visualizing cryptocurrency market data. The project leverages data from Binance API and CoinGecko API to explore trends, correlations, and market dynamics for the top 10 USDT trading pairs. 

## Features

1. **Data Sources**:
   - **Binance API**: Provides comprehensive market data, including historical data, real-time data, and trading statistics.
   - **CoinGecko API**: Initially used for data collection but later limited due to free tier restrictions.

2. **Technologies Used**:
   - **Dash + Plotly**: Interactive dashboards and visualizations.
   - **NetworkX**: Correlation network graph construction.
   - **Seaborn**: Heatmap visualizations of correlations.
   - **Matplotlib**: Static charts for detailed insights.
   - **Pandas**: Data manipulation and preprocessing.

3. **Interactive Dashboard**:
   - Dynamic dropdowns to select cryptocurrencies and date ranges.
   - Candlestick charts, volume histograms, and correlation networks.
   - Real-time updates and interactivity.

4. **Visualizations**:
   - Candlestick charts for price movements (OHLC).
   - Correlation networks among cryptocurrencies.
   - Time-series analysis of volume and price trends.
   - Historical data analysis for multiple trading pairs.

## Installation

### Prerequisites
- Python 3.8 or higher
- Libraries:
  - `dash`
  - `plotly`
  - `pandas`
  - `networkx`
  - `seaborn`
  - `matplotlib`

Install dependencies using pip:
```bash
pip install dash plotly pandas networkx seaborn matplotlib
```

### Running the Dashboard
1. Clone the repository:
   ```bash
   git clone https://github.com/elbasri/crypto-data-analysis.git
   cd crypto-data-analysis
   ```
2. Run the main dashboard script:
   ```bash
   python app.py
   ```
3. Open the dashboard in your browser at `http://127.0.0.1:8050`.

## File Structure
```
.
├── data/
│   ├── binance/
│   │   ├── top_10/  # Historical trade data for the top 10 pairs
│   │   ├── top_10_correlation_matrix.csv
│   │   ├── top_10_fees.csv
│   │   ├── ...
├── crypto_analysis_notebook.ipynb  # Full Notebook
├── app.py  # Main dashboard script
├── README.md
└── config.py  # for binance api keys
```

## API Usage

- **Binance API**: Requires account verification and a minimum deposit of 25 USDT for full access.
- **CoinGecko API**: Free tier allows limited data collection.

## Author

**Abdennacer Elbasri**  
[LinkedIn](https://www.linkedin.com/in/elbasri)

Feel free to connect and share feedback!

---

This repository showcases the integration of advanced Python libraries and APIs for cryptocurrency market analysis and visualization.
