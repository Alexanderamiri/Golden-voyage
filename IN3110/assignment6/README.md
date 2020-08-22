# For visualizing datasets 

## data.py
data.py reads and outputs the data in readable ways such that it can be passed into a machine learning algorithm
### Usage
To run simply give dataframe() a file to read or use scatterplot(features1, feature2) and give it two features\
```python
    scatter_plot('pregnant', 'glucose', 'diabetes.csv')
    plt.show()
```

## fitting.py
fits the data produced by data.py to a machinelearning algorithm 
### Usage
Run the functions by fit(list_of_features, classifier_youd_like, file_of_data) along the lines of :
```python
    fit(['pregnant', 'glucose'], GaussianNB(), 'diabetes.csv')
    fit(['pregnant', 'glucose'], KNeighborsClassifier(n_neighbors=3), 'diabetes.csv')
    fit(['pregnant', 'glucose'], SVC(kernel='linear'), 'diabetes.csv')
```

## visualize.py
Visualize makes a scatterplot if you choose two features to train with
### Usage
To run you'll need to send in a list of features and a trained classifier as well as a file
```python
    feaut = ['insulin', 'glucose']
    clf = ft.fit(feaut, eval("SVC(kernel='linear')"), 'diabetes.csv')
    visualize(feaut, clf, 'diabetes.csv')
    plt.show()
```

