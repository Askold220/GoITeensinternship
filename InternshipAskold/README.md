Stock Chart Analysis
This Python project leverages Yahoo Finance data and Plotly to analyze stock price trends, showcasing candlestick charts with custom indicators.

Installation
libraries:

pip install -r requirements.txt
Run the script:

python app.py

The script downloads historical data, identifies rapid price growth, and generates a candlestick chart with indicators.

Class: StockChart
Initialization
from stock_chart_analysis import StockChart

symbol = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-28"

stock_chart = StockChart(symbol, start_date, end_date)
Methods
update_layout()
stock_chart.update_layout()
Configures the layout of the chart.

show_chart()
stock_chart.show_chart()
Displays the candlestick chart with custom indicators.

Example
symbol = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-28"

stock_chart = StockChart(symbol, start_date, end_date)
stock_chart.update_layout()
stock_chart.show_chart()

Author
askold onishchenko
