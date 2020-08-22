import data as dt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


def fit(features, classifier, data):
    """
    This function is used to train a classifier with a given data's subset of
    features

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
        Trained classifier object
    """
    df, train, test = dt.dataframe(data)
    X = train[features]
    y = train.diabetes
    clf = classifier
    clf.fit(X, y)
    train_pred = clf.predict(test[features])
    acc = accuracy_score(test["diabetes"], train_pred)
    print(
        "Accuracy of {} is  : {:.2%}".format(
            classifier.__class__.__name__, acc
        )
    )
    return clf


if __name__ == "__main__":
    fit(["pregnant", "glucose"], GaussianNB(), "diabetes.csv")
    fit(
        ["pregnant", "glucose"],
        KNeighborsClassifier(n_neighbors=3),
        "diabetes.csv",
    )
    fit(["pregnant", "glucose"], SVC(kernel="linear"), "diabetes.csv")
