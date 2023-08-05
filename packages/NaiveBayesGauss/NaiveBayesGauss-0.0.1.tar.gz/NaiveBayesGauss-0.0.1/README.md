# A Custom Implementation of the Naive Bayes Gaussian Algorithm

![](https://miro.medium.com/max/702/0*3_J7YH5beFVmpxBg.png)

## Description

This package is an application of the Naive Bayes Gaussian algorithm that is commonly used to classify objects whose attributes are continuous data.

Please click [here](https://ilyanovak.medium.com/a-custom-implementation-of-the-naive-bayes-gaussian-algorithm-699b3cdda494) to read my brief introduction to Bayesian statistics and a use case of my custom implementation of the Naive Bayes Gaussian algorithm.

## Dependencies

This package uses the following libraries.
* Python 3.8
* pandas
* numpy
* plotly

## Installing and Executing program

1. Pip install the package
    ```
    pip install NaiveBayesGauss
    ```
2. Import the model
   ```
   from NaiveBayes import NaiveBayesGauss
   ```
3. Instantiate the model
    ```
    model = NaiveBayesGauss()
    ```
4. Fit the training data
    ```
    model.fit(X_train, Y_train)
    ```
5. Use the fitted model to predict a class using a single observation of attributes
    ```
    model.predict(X_target.iloc[10], use_normalizer=True)
    ```
6. Obtain the preceeding prediction's complete prediction probability values
    ```
    model.predict_prob
    ```
7. Calculate the model's prediction accuracy on fitted data and plot a confusion matrix
    ```
    model.predict_accuracy(X_target, Y_target, user_normalizer=True, confusion_matrix=True)
    ```
8. Calculate the model's prediction accuracy on fitted data and plot the results on a heat map
    ```
    model.plot_heatmap(X_train, Y_train, attributes['SepalLengthCm', 'PetalLengthCm'], predict_label='Iris-setosa', h=0.1)
    ```
## Authors

Ilya Novak [@NovakIlya](https://www.twitter.com/NovakIlya)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* Lectures by [Victor Lavrenko](https://www.youtube.com/watch?v=os-NaA0ldGs&list=PLBv09BD7ez_6CxkuiFTbL3jsn2Qd1IU7B) were very helpful in understanding the Naive Bayes Gauss algorithm
* The Iris dataset used to validate the model accuracy was obtained from [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/iris)
* The model accuracy was tested against the [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html) implementation
* The code for the heat map was obtained from [Arthur Tok](https://www.kaggle.com/arthurtok/decision-boundaries-visualised-via-python-plotly)
