# Order Blocks Indicator

This Python script utilizes Yahoo Finance data and Plotly to visualize order blocks on candlestick charts.

## Installation

To use this script, you need to have Python installed on your machine. Install the required libraries by running:

```bash
pip install -r requirements.txt

Open the app.py file and set the desired parameters such as symbol, start_date, and end_date.

Run the script:
python app.py

The script will download historical data, identify order blocks, and generate a candlestick chart with order block indicators.

Class: TechnicalIndicatorPlotter
Initialization
python
Copy code
indicator = TechnicalIndicatorPlotter(symbol: str, start_date: str, end_date: str, range_value: int = 15)
Methods
download_data()
Downloads historical data from Yahoo Finance.

identify_boxes()
Identifies order blocks based on historical data.

plot_indicator()
Generates and displays a candlestick chart with order block indicators.

Example
python
Copy code
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2022-12-31"

indicator = TechnicalIndicatorPlotter(symbol, start_date, end_date)
indicator.download_data()
indicator.identify_boxes()
indicator.plot_indicator()


Author
Askold Onishchenko

