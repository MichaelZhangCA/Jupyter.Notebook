import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
from datetime import timedelta

def drawchart(symbol, df):

    # find the last 6 month as x axis range
    range_enddate = df.index.max()
    range_startdate = range_enddate + timedelta(weeks=-36)

    # only keep recent 3 years rows
    df = df.drop(df[df.index < range_enddate + timedelta(weeks=-160) ].index)
    
    # enrich the data - macd up/down, bb_low > kc_low, bb_high < kc_high
    df['macd_up'] = df.macd > df.macd.shift(-1)
    df['squeeze_value'] = 0                                                             # squeeze value set to 0 to show the marker on zero line
    df['is_squeeze'] = (df.bb_lower >= df.kc_lower) & (df.bb_upper <= df.kc_upper)     # squeeze indicator for color
    df['squeeze_line'] = (df.is_squeeze == False) & (df.is_squeeze.shift(1) == True)
    
    style_bollingerbands_middle = dict( color = ('rgb(22, 96, 167)'), width = 1, dash = 'dot')
    style_bollingerbands_upper = dict( color = ('rgb(22, 96, 167)'), width = 1, dash = 'line')
    style_bollingerbands_lower = dict( color = ('rgb(91, 154, 255)'), width = 1, dash = 'line')

    style_kc_middle = dict( color = ('rgb(247, 94, 39)'), width = 1, dash = 'dot')
    style_kc_upper = dict( color = ('rgb(247, 94, 39)'), width = 1, dash = 'line')
    style_kc_lower = dict( color = ('rgb(244, 118, 73)'), width = 1, dash = 'line')

    trace_candle = go.Candlestick(x=df.index, open=df.adj_open, high=df.adj_high, low=df.adj_low, close=df.adj_close, 
                        showlegend=False, name='close price',
                        increasing=dict(line=dict(color= '#586b59')), #b1e2b6
                        decreasing=dict(line=dict(color= '#51150e'))
                        ,hoverinfo='y'
                    )

    '''
    # OHLC chart for stock price, hide hover info to make UI more readable
    trace_ohlc = go.Ohlc(x=df.index, open=df.adj_open, high=df.adj_high, low=df.adj_low, close=df.adj_close, 
                         showlegend=False, name='close price',
                         increasing=dict(line=dict(color= '#b1e2b6')),
                         decreasing=dict(line=dict(color= '#51150e')),
                         hoverinfo='none'
                        )
    '''

    trace_bb_middle = go.Scatter(x=df.index, y=df.bb_middle, name='BB Middle', legendgroup='Bollinger Bands',
                                 showlegend=False, opacity=0.5, hoverinfo='none',
                                 line = style_bollingerbands_middle
                                )
    trace_bb_upper = go.Scatter(x=df.index, y=df.bb_upper, name='BB Upper', legendgroup='Bollinger Bands',
                                line = style_bollingerbands_upper
                               )
    trace_bb_lower = go.Scatter(x=df.index, y=df.bb_lower, name='BB Lower', legendgroup='Bollinger Bands',
                                line = style_bollingerbands_lower
                               )
    
    trace_kc_middle = go.Scatter(x=df.index, y=df.kc_middle, name='KC Middle', legendgroup='Keltner Channels 2ATR',
                                 showlegend=False, opacity=0.5, hoverinfo='none',
                                 line = style_kc_middle
                                )
    trace_kc_upper = go.Scatter(x=df.index, y=df.kc_upper, name='KC 2ATR Upper', legendgroup='Keltner Channels 2ATR',
                                     line = style_kc_upper
                                    )
    trace_kc_lower = go.Scatter(x=df.index, y=df.kc_lower, name='KC 2ATR Lower', legendgroup='Keltner Channels 2ATR',
                                     line = style_kc_lower
                                    )
    '''
    # create volume bar chart on the bottom
    tarce_volume = go.Bar(x=df.index, y=df.adj_volume, name='volume', showlegend=False, marker=dict(color='rgb(87, 91, 130)'),
                          yaxis = 'y2'
                         )
    '''

    # color dict for MACD
    macd_colordict = []
    squeeze_colordict = []
    for index, row in df.iterrows():
        # MACD
        color_macd = '#029107' if (row['macd']>=0 and row['macd_up']==True) else \
                    ('#0599b7' if (row['macd']>=0 and row['macd_up']==False) else \
                    ('#871001' if (row['macd']<0 and row['macd_up']==False) else '#d35004' ))
        macd_colordict.append(color_macd)
        # squeeze
        color_squeeze = '#022ff7' if row['is_squeeze'] else '#404241'  #f21104 for red
        squeeze_colordict.append(color_squeeze)


    trace_macd = go.Bar(x=df.index, y=df.macd, name='MACD(12/26/9)', showlegend=False, 
                        marker=dict(color=macd_colordict),
                        yaxis = 'y3'
                       )

    trace_squeeze = go.Scatter(x=df.index, y=df.squeeze_value, name='', showlegend=False, 
                               mode = 'markers', marker=dict(size=6, color=squeeze_colordict), hoverinfo='none',
                               yaxis = 'y3'
                               )

    trace_wave_a = go.Bar(x=df.index, y=df.wavea, name='WAVE A(8/34/34)', showlegend=False, 
                    marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.wavea]),
                    yaxis = 'y4'
                   )

    trace_wave_b = go.Bar(x=df.index, y=df.waveb, name='WAVE B(8/89/89)', showlegend=False, 
                marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.waveb]),
                yaxis = 'y5'
               )
    trace_wave_c = go.Bar(x=df.index, y=df.wavec, name='WAVE C(8/144/144)', showlegend=False, 
                    marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.wavec]),
                    yaxis = 'y6'
                   )

    # collect all traces show on the chart
    data = [trace_candle, trace_bb_middle, trace_kc_middle,
            trace_bb_upper, trace_bb_lower, trace_kc_upper, trace_kc_lower, 
            #tarce_volume, 
            trace_macd, trace_squeeze, trace_wave_a, trace_wave_b, trace_wave_c]
    

    # find the min & max in the range
    y_range_high = int(df[df.index > range_startdate].adj_close.max() / 10 +1 ) * 10
    y_range_low = int( df[df.index > range_startdate].adj_close.min() / 10 ) * 10

    # print(y_range_high, y_range_low)

    # fixrange=True, cannot zoom in, useful for y axis for the small indicators
    # fixrange=Fasle with range setting, used in the main chart so it could be zoomed in
    # define xaxis template to shorten layout
    xaxis_template = dict(type="date", showgrid=True, zeroline=True, showline=True, 
                          rangeslider=dict(visible=False), fixedrange=False,
                          range = [range_startdate, range_enddate]
                     )

    # generate shapes for squeeze line
    squeezeline_style = {'color':'rgb(30,60,30)', 'width':1, 'dash':'dot'}
    
    squeezelines = []
    dflines = df[df.squeeze_line==True]
    for idx, row in dflines.iterrows():
        squeezeline = {'type':'line', 'y0':0, 'y1':1, 'xref':'x', 'yref':'paper', 'line':squeezeline_style}
        squeezeline['x0'] = squeezeline['x1'] = idx.strftime('%Y-%m-%d')
        squeezelines.append(squeezeline)
    
    layout = go.Layout(
        title = '{} - John Carter TTM Squeeze'.format(symbol),
        # put legend in left/top coner
        legend = dict(x=0.05, y=1.0),
        height=1050,
        margin = go.Margin(l=80,r=30,t=50,b=100),
        paper_bgcolor='#000', plot_bgcolor='#000',

        xaxis = xaxis_template,

        # all yaxis domains (leave gap between y and below to show the x axis labels
        yaxis = dict(domain=[0.35,1], autorange=False, fixedrange=False, range=[y_range_low, y_range_high]),
        # yaxis2 = dict(domain=[0.5,0.5], visible=False),
        yaxis3 = dict(domain=[0.225,0.325], fixedrange=True, title='MACD'),
        yaxis4 = dict(domain=[0.15,0.225], fixedrange=True, visible=True, title="WAVEA"),
        yaxis5 = dict(domain=[0.075,0.15], fixedrange=True, visible=True, title="WAVEB"),
        yaxis6 = dict(domain=[0,0.075], fixedrange=True, visible=True, title="WAVEC"),
        
        shapes = squeezelines
    )

    # control model bar    
    config = {'showLink':False, 'modeBarButtonsToRemove': ['sendDataToCloud','zoom2d','select2d','lasso2d']}
    
    fig = go.Figure(data=data, layout=layout )
    # standalone chart
    plotly.offline.plot(fig, filename="{} - John Carter Squeeze Chart.html".format(symbol), config=config)


