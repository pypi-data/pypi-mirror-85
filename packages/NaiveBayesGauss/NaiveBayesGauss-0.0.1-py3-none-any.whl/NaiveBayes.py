import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

class NaiveBayesGauss:

    def __init__(self):
        self.predict_prob = None

    def _get_data(self):
        if not hasattr(self, 'data'):
            return
        else:
            return self.data

    def _get_labels(self):
        if not hasattr(self, 'labels'):
            return
        else:
            return self.labels

    def _get_describe_attributes(self):
        if not hasattr(self, 'describe_attributes'):
            return
        else:
            return self.describe_attributes

    def _get_describe_labels(self):
        if not hasattr(self, 'describe_labels'):
            return
        else:
            return self.describe_labels

    def _get_prior(self, label):
        '''
        Calculates prior (probability) of specified label
        Arguments:
            label: Index value of label whose prior probability to calculate
        Returns prior probability of specified label
        '''
        return self._get_describe_labels()[label]

    def _get_likelihood(self, label, attribute, x):
        '''
        Calculate likelihood (probability) of attribute
        Arguments:
            label: Index value of label whose attribute's gaussian distribution to calculate
            attribute: Index value of attribute whose gaussian distribution to calculate
            x: Real value whose likelihood to estimate
        Returns: A likelihood estimate of the value using a gaussian distribution
        '''

        mean = self._get_describe_attributes()[attribute]['mean'][label]
        std = self._get_describe_attributes()[attribute]['std'][label]
        coefficient = 1 / (std * np.sqrt(2 * np.pi))
        numerator = -1 * (x - mean) ** 2
        denominator = 2 * std ** 2
        euler = np.exp(numerator / denominator)
        F_x = coefficient * euler

        return F_x

    def _get_posterior(self, label, X):
        '''
        Calculate posterior (probability) of label for X values
        Arguments:
            label: Index value of label whose posterior to calculate
            X: List of real values whose posterior to estimate
        Returns: A posterior estimate of the X values
        '''

        # posterior = self._get_prior(label)
        # for i in range(len(X)):
        #     posterior *= self._get_likelihood(label, i, X[i])

        posterior = self._get_prior(label)
        for attribute in X.index:
            posterior *= self._get_likelihood(label, attribute, X[attribute])

        return posterior

    def _get_normalizer(self, X):
        '''
        '''

        normalizer = 0
        for label in self._get_labels():
            normalizer += self._get_posterior(label, X)

        return normalizer

    def predict_prob(self):
        return self.predict_prob

    def fit(self, X, Y):
        '''
        Fits observations data on target data using a Naive Bayes algorithm
        Arguments:
            X: Pandas DataFrame or Series with training data of attributes. It has n samples and m attributes
            Y: Pandas DataFrame or Series with training data of labels. It has n samples
        '''

        # Verify X and Y are a Pandas Series or DataFrame objects
        if not isinstance(X, (pd.Series, pd.DataFrame)) or not isinstance(Y, (pd.Series, pd.DataFrame)):
            raise TypeError(
                f'X and Y must be a Pandas Series or DataFrame object but X is {type(X)} but Y is {type(Y)}')
        # Verify X and Y have identical number of rows
        elif X.shape[0] != Y.shape[0]:
            raise ValueError(
                f'X and Y must have identical number of rows but X has shape {X.shape} and Y has shape {Y.shape}')

        # Concatinate and convert X and Y into dataframe.
        # Last column is target values. The rest are training values.
        self.data = pd.concat([pd.DataFrame(X), pd.DataFrame(Y)], axis=1)

        # List of unique labels in Y target data
        self.labels = self._get_data()[self._get_data().columns[-1]].unique()

        # Dataframe that describes mean and standard deviation of each attribute for each label
        # Dataframe with describe[i][mean/std][j] where i is attribute index value and j is label index value
        self.describe_attributes = self._get_data().groupby(by=self._get_data()[self._get_data().columns[-1]]).describe()\
            .drop(['count', 'min', '25%', '50%', '75%', 'max'], axis=1, level=1)

        # Series that describes percentage of each label in the target values
        self.describe_labels = self._get_data(
        )[self._get_data().columns[-1]].value_counts(normalize=True)

    def predict(self, X, use_normalizer=False):
        '''
        Predicts label based on specified attributes
            X: A 1-D Pandas Series or DataFrame with attribute values used to predict label
            use_normalizer: If True then include normalization in probability calculation
        Returns: Predicted label
        '''

        # Verify X is a Pandas Series or DataFrame objects
        if not isinstance(X, (pd.Series, pd.DataFrame)):
            raise TypeError(
                f'X must be a Pandas Series or DataFrame object but X is {type(X)}')
        # Verify X and training data have identical number of rows
        elif X.shape != (model._get_data().shape[1] - 1, 1) and X.shape != (model._get_data().shape[1] - 1, ):
            raise ValueError(
                f'X must have number of rows identical to number of columns of training data but X has shape {X.shape} and training data has shape {self._get_data().iloc[:,0:-1].shape}')

        if use_normalizer == True:
            normalizer = self._get_normalizer(X)
        predict_prob = {}
        max_label = 0
        max_posterior = 0

        # Iterate through each label in fitted data
        for label in self._get_labels():
            # Calculate label's posterior and assign probability value to predict_prob with label as key
            if use_normalizer == True:
                predict_prob[label] = self._get_posterior(
                    label, X) / normalizer
            else:
                predict_prob[label] = self._get_posterior(label, X)
            # Select highest posterior
            if predict_prob[label] > max_posterior:
                max_posterior = predict_prob[label]
                max_label = label

        # Save predict_prob for future reference
        self.predict_prob = predict_prob

        return max_label

    def predict_accuracy(self, X, Y, use_normalizer=False, confusion_matrix=False):
        '''
        Uses a pre-fit model to predict a label for each observation in X verifies it against its correct label in Y
            X: Pandas DataFrame or Series with training data of attributes. It has n samples and m attributes
            Y: Pandas DataFrame or Series with training data of labels. It has n samples
            use_normalizer: If True then include normalization in probability calculation
            confusion_matrix: If True then also generates a confusion matrix
        Returns total predictions accuracy
        '''

        # Verify model has been previously fit
        if not hasattr(self, 'predict_prob'):
            raise AttributeError('Model has not yet been fit')
        # Verify X and Y are a Pandas Series or DataFrame objects
        if not isinstance(X, (pd.Series, pd.DataFrame)) or not isinstance(Y, (pd.Series, pd.DataFrame)):
            raise TypeError(
                f'X and Y must be a Pandas Series or DataFrame object but X is {type(X)} but Y is {type(Y)}')
        # Verify X and Y have identical number of rows
        elif X.shape[0] != Y.shape[0]:
            raise ValueError(
                f'X and Y must have identical number of rows but X has shape {X.shape} and Y has shape {Y.shape}')

        predictions = []
        hit_rate = 0

        if confusion_matrix == True:
            values_matrix = pd.DataFrame(
                index=Y.unique(), columns=Y.unique()).fillna(0)

        # Iterate through X and perform model prediction on each vector of values
        for i in range(len(X)):
            prediction = self.predict(X.iloc[i], use_normalizer=use_normalizer)
            actual = Y.iloc[i]
            if prediction == actual:
                hit_rate += 1
            if confusion_matrix == True:
                values_matrix[actual][prediction] += 1
            predictions.append(prediction)

        print(f"The fitted model's prediction accuracy is {hit_rate/len(X)}")

        if confusion_matrix == True:
            # Necessary in case function is run in a jupyter notebook
            def enable_plotly_in_cell():
                import IPython
                from plotly.offline import init_notebook_mode
                display(IPython.core.display.HTML(
                    '''<script src="/static/components/requirejs/require.js"></script>'''))
                init_notebook_mode(connected=False)
            enable_plotly_in_cell()

            fig = ff.create_annotated_heatmap(x=list(Y.unique()),
                                              y=list(Y.unique()),
                                              z=values_matrix.values,
                                              colorscale='Viridis')
            fig.update_layout(title_text='Naive Bayes Gaussian Model Confusion Matrix',
                              title_x=0.5,
                              width=400, height=400)
            fig.show()

    def plot_heatmap(self, X, Y, attributes, predict_label, h=0.1):
        '''
        Plots heatmap of naive bayes probabilities for data with two attributes:
            X: Pandas DataFrame or Series with training data of attributes. It has n samples and m attributes
            Y: Pandas DataFrame or Series with training data of labels. It has n samples
            attributes: A list of length 2 with whose elements are columns in training data
            predict_label: Label whose prediction probability to display in heatmap
            h: # Step size in the mesh
        '''

        # Verify X and Y are a Pandas Series or DataFrame objects
        if not isinstance(X, (pd.Series, pd.DataFrame)) or not isinstance(Y, (pd.Series, pd.DataFrame)):
            raise TypeError(
                f'X and Y must be a Pandas Series or DataFrame object but X is {type(X)} but Y is {type(Y)}')
        # Verify X and Y have identical number of rows
        elif X.shape[0] != Y.shape[0]:
            raise ValueError(
                f'X and Y must have identical number of rows but X has shape {X.shape} and Y has shape {Y.shape}')
        # Verify attribute is a list with correct length
        elif type(attributes) != list:
            raise TypeError(
                f'attributes must be a list but is a {type(attributes)}')
        elif len(attributes) != 2:
            raise TypeError(
                f'attributes must be a list of length 2 but has length {len(attributes)}')
        # Verify h is of float type
        elif type(h) == 'float64':
            raise TypeError(f'h should be float data type but it is {type(h)}')

        print("This may time some time. Decrease size of X and Y or h arguments to increase processing time.")

        # Minimum and maximum values of x and y coordinates in mesh grid
        x_min, x_max = X.loc[:, attributes[0]].min(
        ) - 1, X.loc[:, attributes[0]].max() + 1
        y_min, y_max = X.loc[:, attributes[1]].min(
        ) - 1, X.loc[:, attributes[1]].max() + 1

        # Range of values for x and y coordinates in mesh grid
        x_range = np.arange(x_min, x_max, h)
        y_range = np.arange(y_min, y_max, h)

        # Set of x and y coordinates in mesh grid
        x_coord, y_coord = np.meshgrid(x_range, y_range)
        coords = np.c_[x_coord.ravel(), y_coord.ravel()]

        y_ = np.arange(y_min, y_max, h)

        self.fit(X[attributes], Y)

        # Generate probability predictions for all coordinates in mesh grid
        predictions = []
        count = 0
        for index, coord in pd.DataFrame(coords, columns=attributes).iterrows():
            # prediction = self.predict(coord)
            # predictions.append(self.predict_prob[prediction])
            self.predict(coord)
            predictions.append(self.predict_prob[predict_label])
            if count % 1000 == 0:
                print(f'Calculated {count}/{len(coords)} predictions...')
            count += 1
        Z = np.array(predictions).reshape(x_coord.shape)

        # Necessary in case function is run in a jupyter notebook
        def enable_plotly_in_cell():
            import IPython
            from plotly.offline import init_notebook_mode
            display(IPython.core.display.HTML(
                '''<script src="/static/components/requirejs/require.js"></script>'''))
            init_notebook_mode(connected=False)
        enable_plotly_in_cell()

        # Generate heat map and scatterplot
        trace1 = go.Heatmap(x=x_coord[0],
                            y=y_,
                            z=Z,
                            colorscale='Jet',
                            showscale=False,
                            zsmooth='best',
                            hoverinfo='skip')
        trace2 = go.Scatter(x=X[attributes[0]],
                            y=X[attributes[1]],
                            mode='markers',
                            hoverinfo="text",
                            text=Y.values,
                            marker=dict(size=10,
                                        color=pd.factorize(Y)[0],
                                        colorscale='Jet',
                                        reversescale=True,
                                        line=dict(color='black', width=1))
                            )
        layout = go.Layout(title_text=f'{predict_label} surface probability',
                           title_x=0.5,
                           hovermode='closest',
                           showlegend=False,
                           width=500, height=500,
                           xaxis_title=attributes[0],
                           yaxis_title=attributes[1])

        data = [trace1, trace2]
        fig = go.Figure(data=data, layout=layout)
        fig.show()
