import chart_studio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from main import init_df

def show_file_mods(df):
    # Create YearMonthDay field for ease of reporting and visualization
    df['YearMonthDay'] = df['ModDate'].map(lambda date: 10000*date.year + 100*date.month + date.day)
    df_grouped = df.groupby('YearMonthDay')['Project'].nunique().reset_index(name='Frequency')

    plt.plot(df_grouped['YearMonthDay'], df_grouped['Frequency'])
    plt.title('File Access Frequencies Across Time')
    plt.xlabel('YearMonthDay')

    # Changes domain
    # plt.xlim(2.020e7, 2.0202e7)
    plt.ylabel('Frequency')
    plt.show()
    print(df_grouped)


if __name__ == "__main__":
    df = init_df()
    show_file_mods(df)
