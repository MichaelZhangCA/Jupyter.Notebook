from chart import johncarter_squeeze_chart as jcchart
import johncarter_squeeze as jcdata
from codetimer import CodeTimer

def johncarter_study(symbol):
   
    with CodeTimer('Prepare JC Squeeze data') as ct:
        df = jcdata.process_jcsqueeze(symbol)

    # draw chart
    jcchart.drawchart(symbol, df)
    

if (__name__ == '__main__'):
    show_stockchart()