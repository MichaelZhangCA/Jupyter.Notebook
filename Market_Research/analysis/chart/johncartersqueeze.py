import plotly
import plotly.plotly as py
import plotly.graph_objs as go

def drawchart(symbol, df):
    
    style_bollingerbands_middle = dict( color = ('rgb(22, 96, 167)'), width = 1, dash = 'dot')
    style_bollingerbands_upper = dict( color = ('rgb(22, 96, 167)'), width = 1, dash = 'line')
    style_bollingerbands_lower = dict( color = ('rgb(91, 154, 255)'), width = 1, dash = 'line')

    style_kc_middle = dict( color = ('rgb(247, 94, 39)'), width = 1, dash = 'dot')
    style_kc2_upper = dict( color = ('rgb(247, 94, 39)'), width = 1, dash = 'line')
    style_kc2_lower = dict( color = ('rgb(244, 118, 73)'), width = 1, dash = 'line')

    '''
    style_kc3_upper = dict( color = ('rgb(46, 155, 53)'), width = 1, dash = 'line')
    style_kc3_lower = dict( color = ('rgb(68, 206, 77)'), width = 1, dash = 'line')

    style_kc1_upper = dict( color = ('rgb(244, 78, 66)'), width = 1, dash = 'line')
    style_kc1_lower = dict( color = ('rgb(198, 70, 61)'), width = 1, dash = 'line')
    '''
    # OHLC chart for stock price, hide hover info to make UI more readable
    trace_ohlc = go.Ohlc(x=df.index, open=df.adj_open, high=df.adj_high, low=df.adj_low, close=df.adj_close, 
                         showlegend=False, name='close price',
                         increasing=dict(line=dict(color= '#b1e2b6')),
                         decreasing=dict(line=dict(color= '#51150e')),
                         hoverinfo='none'
                        )
    
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
    trace_kc_2atr_upper = go.Scatter(x=df.index, y=df.kc_2_upper, name='KC 2ATR Upper', legendgroup='Keltner Channels 2ATR',
                                     line = style_kc2_upper
                                    )
    trace_kc_2atr_lower = go.Scatter(x=df.index, y=df.kc_2_lower, name='KC 2ATR Lower', legendgroup='Keltner Channels 2ATR',
                                     line = style_kc2_lower
                                    )
    '''
    # create volume bar chart on the bottom
    tarce_volume = go.Bar(x=df.index, y=df.adj_volume, name='volume', showlegend=False, marker=dict(color='rgb(87, 91, 130)'),
                          yaxis = 'y2'
                         )
    '''

    # color dict for MACD
    macd_colordict = []
    for index, row in df.iterrows():

        color =  '#029107' if (row['macd']>=0 and row['macd_up']==True) else \
                ('#0599b7' if (row['macd']>=0 and row['macd_up']==False) else \
                ('#871001' if (row['macd']<0 and row['macd_up']==False) else '#d35004' ))
        macd_colordict.append(color)

    trace_macd = go.Bar(x=df.index, y=df.macd, name='MACD(12/26/9)', showlegend=False, 
                        marker=dict(color=macd_colordict),
                        yaxis = 'y3'
                       )

    trace_wave_a = go.Bar(x=df.index, y=df.wave_a, name='WAVE A(8/34/34)', showlegend=False, 
                    marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.wave_a]),
                    yaxis = 'y4'
                   )

    trace_wave_b = go.Bar(x=df.index, y=df.wave_b, name='WAVE B(8/89/89)', showlegend=False, 
                marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.wave_b]),
                yaxis = 'y5'
               )
    trace_wave_c = go.Bar(x=df.index, y=df.wave_c, name='WAVE C(8/144/144)', showlegend=False, 
                    marker=dict(color=['#029107' if val>=0 else '#871001' for val in df.wave_c]),
                    yaxis = 'y6'
                   )

    # collect all traces show on the chart
    data = [trace_ohlc, trace_bb_middle, trace_kc_middle,
            trace_bb_upper, trace_bb_lower, trace_kc_2atr_upper, trace_kc_2atr_lower, 
            #tarce_volume, 
            trace_macd, trace_wave_a, trace_wave_b, trace_wave_c]
    
    # define xaxis template to shorten layout
    axis_template = dict(showgrid=True, zeroline=True, showline=True, rangeslider=dict(visible=False), fixedrange=True)
    layout = go.Layout(
        title = '{} - John Carter TTM Squeeze'.format(symbol),
        # put legend in left/top coner
        legend = dict(x=0.05, y=1.0),
        height=800,
        margin = go.Margin(l=80,r=30,t=50,b=100),
        paper_bgcolor='#000', plot_bgcolor='#000',

        xaxis = axis_template,

        # all yaxis domains (leave gap between y and below to show the x axis labels
        yaxis = dict(domain=[0.45,1]),
        # yaxis2 = dict(domain=[0.4,0.5], visible=False),
        yaxis3 = dict(domain=[0.3,0.4], title='MACD'),
        yaxis4 = dict(domain=[0.2,0.3], visible=True, title="WAVEA"),
        yaxis5 = dict(domain=[0.1,0.2], visible=True, title="WAVEB"),
        yaxis6 = dict(domain=[0,0.1], visible=True, title="WAVEC")
    )

    fig = go.Figure(data=data, layout=layout)
    # standalone chart
    plotly.offline.plot(fig, filename="{} - John Carter Squeeze Chart.html".format(symbol))

