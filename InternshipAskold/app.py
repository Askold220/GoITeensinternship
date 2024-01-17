import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

class OrderBlocksIndicatorPlotter:
    def __init__(self, symbol: str, start_date: str, end_date: str, range_value: int = 15):
        """
        Инициализация объекта OrderBlocksIndicatorPlotter.

        Параметры:
        - symbol (str): Тикер акции или инструмента.
        - start_date (str): Начальная дата для загрузки данных (в формате 'YYYY-MM-DD').
        - end_date (str): Конечная дата для загрузки данных (в формате 'YYYY-MM-DD').
        - range_value (int): Значение для расчета структурного минимума.
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.range_value = range_value
        self.data = None
        self.short_boxes = []  # Список коротких (красных) блоков
        self.long_boxes = []   # Список длинных (зеленых) блоков

    def download_data(self):
        """
        Загрузка данных с Yahoo Finance в заданном временном диапазоне.
        """
        self.data = yf.download(self.symbol, start=self.start_date, end=pd.to_datetime('today'))

    def identify_boxes(self):
        """
        Идентификация блоков на основе структурного минимума и максимума.
        """
        structure_low = min(self.data['Low'][:self.range_value])

        for i in range(self.range_value, len(self.data)):
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
        Построение графика с использованием библиотеки Plotly.
        """
        fig = go.Figure()

        # Свечи
        fig.add_trace(go.Candlestick(x=self.data.index, open=self.data['Open'], high=self.data['High'],
                                     low=self.data['Low'], close=self.data['Close'],
                                     increasing_line_color='rgba(0, 255, 255, 1)',
                                     decreasing_line_color='rgba(255, 99, 71, 1)',
                                     name='Candlesticks'))

        # Красные блоки
        for box in self.short_boxes:
            fig.add_trace(go.Candlestick(x=[self.data.index[box[0]], self.data.index[box[1]]],
                                         open=[box[2], box[2]], high=[box[2] + 0.1, box[2] + 0.1],
                                         low=[box[2], box[2]],
                                         increasing_line_color='rgba(255, 99, 71, 1)',
                                         decreasing_line_color='rgba(255, 99, 71, 1)'))

        # Зеленые блоки
        for box in self.long_boxes:
            fig.add_trace(go.Candlestick(x=[self.data.index[box[0]], self.data.index[box[1]]],
                                         open=[box[2], box[2]], high=[box[2] + 0.1, box[2] + 0.1],
                                         low=[box[2], box[2]],
                                         increasing_line_color='rgba(0, 255, 255, 1)',
                                         decreasing_line_color='rgba(0, 255, 255, 1)'))

        # Идентификация центра
        center_y = (self.data['High'].max() + self.data['Low'].min()) / 2

        # Добавление двух горизонтальных линий
        fig.add_shape(type="line", x0=self.data.index[0], x1=self.data.index[-1],
                      y0=center_y - 15, y1=center_y - 15,
                      line=dict(color="blue", width=1),
                      visible='legendonly',  # Линии видны только при наведении
                      opacity=0.7)

        fig.add_shape(type="line", x0=self.data.index[0], x1=self.data.index[-1],
                      y0=center_y + 15, y1=center_y + 15,
                      line=dict(color="blue", width=1),
                      visible='legendonly',  # Линии видны только при наведении
                      opacity=0.7)

        # Настройка макета
        fig.update_layout(title='Order Blocks Indicator', xaxis_title='Date', yaxis_title='Closing Price',
                          template="plotly_dark", height=800, hovermode="x unified")

        # Центрирование правого конца диаграммы
        fig.update_xaxes(rangeslider_visible=False, rangebreaks=[dict(bounds=["sat", "mon"])])  # Центрирование правого конца диаграммы

        fig.show()

# Пример использования:
symbol = "MSFT"
start_date = "2023-01-01"
end_date = "2024-01-16"

indicator = OrderBlocksIndicatorPlotter(symbol, start_date, end_date)
indicator.download_data()
indicator.identify_boxes()
indicator.plot_indicator()
