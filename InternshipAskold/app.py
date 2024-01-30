import yfinance as yf
import plotly.graph_objects as go

class StockChart:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.data = yf.download(symbol, start=start_date, end=end_date)
        self.fig = go.Figure()
        self.increasing_color = 'rgba(0, 255, 255, 1)'
        self.decreasing_color = 'rgba(255, 99, 71, 1)'
        self.candle_height = self.data['Open'] - self.data['Close']
        self.threshold = 0.03
        self.height_increase = 0
        self.add_candlestick()
        self.add_rapid_growth_indicator()

    def add_candlestick(self):
        self.fig.add_trace(go.Candlestick(x=self.data.index,
                            open=self.data['Open'],
                            high=self.data['High'],
                            low=self.data['Low'],
                            close=self.data['Close'],
                            increasing_line_color=self.increasing_color,
                            decreasing_line_color=self.decreasing_color,
                            increasing_line_width=4,
                            decreasing_line_width=4,
                            showlegend=False))

    def add_rapid_growth_indicator(self):
        rapid_growth_indicator = go.layout.Shape(
            type="line",
            x0=self.data.index[0],
            x1=self.data.index[-1],
            y0=0,
            y1=0,
            line=dict(color="rgba(0, 200, 0, 0.3)", width=45, dash='solid'),
        )

        for i in range(1, len(self.data)):
            price_change_percentage = (self.data['Close'][i] - self.data['Close'][i - 1]) / self.data['Close'][i - 1]
            if price_change_percentage > self.threshold:
                rapid_growth_indicator['x0'] = self.data.index[i - 1]
                rapid_growth_indicator['x1'] = self.data.index[-1]
                rapid_growth_indicator['y0'] = (self.data['Low'][i - 1] + self.data['High'][i - 1]) / 2
                rapid_growth_indicator['y1'] = rapid_growth_indicator['y0'] - self.height_increase
                self.fig.add_shape(go.layout.Shape(rapid_growth_indicator, opacity=0.7))

    def update_layout(self):
        self.fig.update_layout(title=f"{self.symbol} Stock Price with Custom Indicator",
                          xaxis_title="Date",
                          yaxis_title="Stock Price",
                          xaxis_rangeslider_visible=False,
                          paper_bgcolor='black',
                          plot_bgcolor='black',
                          xaxis=dict(showgrid=True, gridwidth=1, gridcolor='grey'))

    def show_chart(self):
        self.fig.show()

symbol = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-28"

stock_chart = StockChart(symbol, start_date, end_date)
stock_chart.update_layout()
stock_chart.show_chart()
