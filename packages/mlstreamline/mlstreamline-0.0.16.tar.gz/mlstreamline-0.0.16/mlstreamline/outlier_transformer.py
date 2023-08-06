#Custom transformer we wrote to engineer features ( bathrooms per bedroom and/or how old the house is in 2019  )
#passed as boolen arguements to its constructor
class OutlierTransformer(BaseEstimator, TransformerMixin):
    #Class Constructor
    def __init__( self, feature_names):
        self.feature_names = feature_names

    def replace_outliers(self, value, upper, lower):
        if value > upper:
            return upper
        elif value < lower:
            return lower
        else:
            return value

    # Return self, nothing else to do here
    def fit(self, X, y = None ):
        return self

    # Custom transform method we wrote that creates aformentioned features and drops redundant ones
    def transform(self, X, y=None):
        for feature_name in self.feature_names:
            column_data = X.loc[:, 'feature_name'].copy()
            q25, q75 = np.percentile(column_data, 25), np.percentile(column_data, 75)
            iqr = q75 - q25
            # calculate the outlier cutoff
            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off
            X.loc[:, 'feature_name'] = X.loc[:, 'feature_name'].apply(self.replace_outliers, args=(upper, lower))

        # returns a numpy array
        return X.values