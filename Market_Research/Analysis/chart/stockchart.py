import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def show_close_withadj(df):

    ax = df[["close", "adj_close"]].plot.line(grid='true', figsize=(18,10), title='stock price', 
                                          marker=".", markersize=1, fontsize=18)
    # ax.set_xlabel('', fontsize=18)
    plt.show()

