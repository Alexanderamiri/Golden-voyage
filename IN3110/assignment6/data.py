import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def dataframe(file):
    """
    This function will read a file and delete lines with NAN, it will create
    a training set and a test set that can be used in machine learning

    Arguments
    ----------
    file : String
        File to read
    Returns
    -------
    tuple
        pandas list of the whole data set, 80% of the data, 20% of the data
    """
    data = pd.read_csv(file, sep=",")
    data = data[
        [
            "pregnant",
            "glucose",
            "pressure",
            "triceps",
            "insulin",
            "mass",
            "pedigree",
            "age",
            "diabetes",
        ]
    ]
    data = data.dropna()
    data = data.reset_index(drop=True)
    data = data.replace("neg", 0)
    data = data.replace("pos", 1)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    return data, train, test


def scatter_plot(n1, n2, data):
    p = dataframe(data)[0][[n1, n2, "diabetes"]]
    col = p.diabetes.map({0: "b", 1: "r"})
    return p.plot.scatter(x=n1, y=n2, c="diabetes", marker="o", cmap="seismic")


if __name__ == "__main__":
    scatter_plot("pregnant", "glucose", "diabetes.csv")
    plt.show()
