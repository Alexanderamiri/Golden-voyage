import data as dt
import fitting as ft
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def visualize(features, classifer, data):
    """
    Visualizes a classifiers boundaries after training

    Arguments
    ----------
    features : list
        list of strings of which features to train with
    classifier : Object
        Classifier object that contains the algorithm to train
    data : Pandas object
        Pandas data frame of all the data

    Returns
    -------
        None
    """
    if len(features) == 2:
        df, train, test = dt.dataframe(data)
        X = train[features]
        y = train.diabetes
        X0, X1 = X[features[0]], X[features[1]]
        x_min, x_max = X0.min() - 1, X0.max() + 1
        y_min, y_max = X1.min() - 1, X1.max() + 1
        stepsize = 0.8
        xx, yy = np.meshgrid(
            np.arange(x_min, x_max, stepsize),
            np.arange(y_min, y_max, stepsize),
        )
        Z = classifer.predict(np.c_[xx.ravel(), yy.ravel()])
        train_pred = classifer.predict(test[features])
        acc = accuracy_score(test["diabetes"], train_pred)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        title = "Decision surface of {}, Accuracy {:.2%}".format(
            classifer.__class__.__name__, acc
        )
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
        ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors="k")
        ax.set_ylabel(features[1])
        ax.set_xlabel(features[0])
        ax.set_title(title)
        return fig
    else:
        print("Cant scatter plot unless there is two features")
        return None


if __name__ == "__main__":
    feaut = ["insulin", "glucose"]
    clf = ft.fit(feaut, eval("SVC(kernel='linear')"), "diabetes.csv")
    visualize(feaut, clf, "diabetes.csv")
    plt.show()
