import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

class TechnicalIndicatorPlotter:
    def __init__(self, symbol: str, start_date: str, end_date: str, range_value: int = 15):
        """
        Инициализация объекта TechnicalIndicatorPlotter.

        :param symbol: Тикер ценной бумаги (например, "AAPL").
        :param start_date: Начальная дата загрузки данных (в формате "YYYY-MM-DD").
        :param end_date: Конечная дата загрузки данных (в формате "YYYY-MM-DD").
        :param range_value: Значение диапазона для идентификации блоков (по умолчанию 15).
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.range_value = range_value
        self.data = None
        self.short_boxes = []
        self.long_boxes = []

    def download_data(self):
        """
        Загрузка данных о ценных бумагах из Yahoo Finance.
        """
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)

    def identify_boxes(self):
        """
        Идентификация блоков на основе данных о ценных бумагах.
        """
        for i in range(1, len(self.data)):
            structure_low = min(self.data['Low'][:i][-self.range_value:])

            if self.data['Low'][i] < structure_low:
                self.short_boxes.append((i - 1, i, self.data['Low'][i], structure_low))
            elif self.short_boxes and self.data['High'][i] > self.short_boxes[-1][3]:
                self.short_boxes[-1] = (self.short_boxes[-1][0], i, self.data['Low'][i], self.short_boxes[-1][3])

            elif self.short_boxes and self.data['Close'][i] > self.short_boxes[-1][2]:
                self.short_boxes.pop()

            if self.short_boxes and self.data['Close'][i] > self.short_boxes[-1][2]:
                self.long_boxes.append((i - 1, i, self.data['Close'][i], structure_low))
            elif self.long_boxes and self.data['Low'][i] < self.long_boxes[-1][3]:
                self.long_boxes[-1] = (self.long_boxes[-1][0], i, self.data['Close'][i], self.long_boxes[-1][3])

            elif self.long_boxes and self.data['Close'][i] < self.long_boxes[-1][2]:
                self.long_boxes.pop()

    def plot_indicator(self):
        """
        Построение графика с указанием блоков.
        """
        fig = go.Figure()

        fig.add_trace(go.Candlestick(x=self.data.index, open=self.data['Open'], high=self.data['High'],
                                     low=self.data['Low'], close=self.data['Close'],
                                     increasing_line_color='lime', decreasing_line_color='red',
                                     name='Candlesticks'))

        for box in self.short_boxes:
            fig.add_trace(go.Candlestick(x=[self.data.index[box[0]]], open=[box[2]], high=[box[2] + 0.1],
                                         low=[box[2]], increasing_line_color='red', decreasing_line_color='red'))

        for box in self.long_boxes:
            fig.add_trace(go.Candlestick(x=[self.data.index[box[0]]], open=[box[2]], high=[box[2] + 0.1],
                                         low=[box[2]], increasing_line_color='green', decreasing_line_color='green'))

        fig.update_layout(title='Order Blocks Indicator', xaxis_title='Date', yaxis_title='Closing Price',
                          template="plotly_dark")

        fig.show()

# Пример использования:
symbol = "AAPL"
start_date = "2022-01-01"
end_date = "2022-12-31"

indicator = TechnicalIndicatorPlotter(symbol, start_date, end_date)
indicator.download_data()
indicator.identify_boxes()
indicator.plot_indicator()
