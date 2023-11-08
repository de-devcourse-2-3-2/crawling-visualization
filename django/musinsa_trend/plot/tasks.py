from plot import Plot
from payload import Payload

def update_chart(self):
    data = Payload.get()
    Plot.chart1(data)