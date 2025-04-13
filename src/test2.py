import pandas as pd
import numpy as np

from typing import List
from matplotlib import pyplot as plt
from numpy.testing import assert_almost_equal, assert_equal
import sys


def main(data_filename):
    print(data_filename)
    df = pd.read_csv(data_filename, sep=',')
    df_selected = df[["date", "close_price"]]
    print(df_selected.shape)
    df_selected.plot(kind='line', figsize=(8, 4), title='In-sample data')
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1])