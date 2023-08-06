
"""
Datatlas: Data Atlas
* Predicting missing values

Author: Mei Yong
Updated date: 2019-10-30

WIP Ideas
    * numerical values - done
    * categorical values - not started
    * hyperparameter tuning - but that would take awhile so maybe only run it if the optional is switched on?

"""

# Import libraries
import pandas as pd
import numpy as np


# Helper function for one-hot encoding of categorical features
def one_hot_encode(df):
    # Identify only categorical features
    categorical_features = df.select_dtypes(include='object').columns.tolist()
    # Loop through categorical features
    for col in categorical_features:
        dummies = pd.get_dummies(df[col], prefix=col, dummy_na=False) # Create dummy features
        df = df.drop(col,1) # Drop the original features
        df = pd.concat([df, dummies], axis=1) # Add the dummy features to the input df to replace the original features
    return df
    

# Main function for imputing missing values
def predict_missing_values(df, impute_column, datatype, impute_model=True, impute_stats=True, console_messages=True):
    '''
    Input(s):
        1) df: Dataframe of all columns including the column with missing values
        2) impute_column (string): Name of the column containing missing values that you want to predict and impute using machine learning
        3) datatype (string): Choose one of the following - numeric, categoric
        4) impute_model (boolean): Default True. See outputs docstring below for more info
        4) stats (boolean): Default True. See outputs docstring below for more info
        5) console_messages (boolean): Default True. Outputs status messages in the console to indicate progress of the model training and predictions
    Output(s):
        1) Dataframe where the nulls in the column to impute are replaced with their predicted values
        2) impute_model (Sklearn estimator object) (optional): The trained model that was used to predict the missing values that can be later used to predict missing values of new live data
        3) impute_stats (dictionary) (optional): A dictionary containing stats about the impute column before and after the predictions. Also includes rmse (for numeric) or accuracy (for categoric) model performance evaluation metrics
    '''
    
    # Keep a copy of the original df to be returned at the end with imputed values
    original_df = df.copy()
    
    # Cleanse the train set - dropping high nulls, zeroes, cardinality
    rowcount = df.shape[0]
    null_profile = {column : round(df[column].isnull().sum() / rowcount * 100, 2) for column in df}
    zeroes_profile = {column : round((df[column]==0).sum() / rowcount * 100, 2) \
                         for column in df if df[column].dtype in ['int64','float64'] }
    cardinality_profile = {column: round(df[column].value_counts().count() / rowcount * 100 , 2) \
                         for column in df if df[column].dtype in ['object'] }
    dq_check = pd.DataFrame([null_profile, zeroes_profile, cardinality_profile]\
                            ,index=['nulls','zeroes','cardinality'])
    dq_check = dq_check.fillna(0)
    del rowcount, null_profile, zeroes_profile, cardinality_profile
    
    del_cols = []
    for col in dq_check:
        if dq_check.loc['nulls',col]>25 \
        or dq_check.loc['zeroes',col]>25 \
        or dq_check.loc['cardinality',col]>50:
            del_cols.append(col)
    
    # If the column to be imputed is in the list of columns to drop, remove it
    if impute_column in del_cols:
        del_cols.remove(impute_column)
    
    # Drop all of the bad quality columns
    df = df.drop(del_cols, axis=1)
    
    # Drop rows if any columns other than the target one has nulls
    target_col = df.pop(impute_column)
    df = df.dropna(axis=0, how='any')
    df = df.merge(target_col, left_index=True, right_index=True)
    
    # One hot encode the categorical columns
    target_col = df.pop(impute_column) # pop out the impute column
    df = one_hot_encode(df) # perform one hot encoding
    df[impute_column] = target_col # stick the impute column back on


    if datatype == 'numeric':
        
        # Replace all zeroes in the target column with nulls
        df[impute_column] = df[impute_column].replace(0, np.nan)
        
        # Calculate the percentage of nulls in the column to be imputed and print in console
        null_n = sum(df[impute_column].isnull())
        null_p = sum(df[impute_column].isnull()) / df[impute_column].shape[0] * 100
        
        if console_messages == True:
            print(f"Datatlas: {round(null_p,2)}% of the target column is null and will be predicted")
        
        # Split the set into train where the impute column is not null and pred where it is null
        train = df[ df[impute_column].isnull()==False ]
        pred = df[ df[impute_column].isnull()==True ]
        
        # Split the train and pred sets into X and y
        y_train, X_train = train.pop(impute_column), train.copy()
        y_pred, X_pred = pred.pop(impute_column), pred.copy()
        
        # Train a regression model using the train set
        if console_messages == True:
            print("Datatlas: Training a Stochastic Gradient Descent regression model to predict the missing numerical values")
               
        from sklearn.linear_model import SGDRegressor
        sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)
        sgd_reg.fit(X_train, y_train)
        
        # Get predictions using the trained model
        if console_messages == True:
            print("Datatlas: Predicting the missing numerical values")
        y_pred = sgd_reg.predict(X_pred)
        y_pred = pd.Series(y_pred, index=X_pred.index)
        
        # Replace the nulls and zeroes in the original df with the imputed/predicted values
        original_df[impute_column] = original_df[impute_column].replace(0, np.nan)
        original_df[impute_column] = original_df[impute_column].fillna(value=y_pred)
        
        
        # Different objects get returned based on the parameters inputted into the function
        
        if impute_stats == False:
            
            if impute_model == False:
                return original_df # No stats, no model
            elif impute_model == True:
                return original_df, sgd_reg # No stats, yes model
        
        # If the impute stats option is turned on, perform calculations for the dictionary and then return different objects depending on whether optional trained impute model is also turned on
        if impute_stats == True:
            
            # Get performance stats using cross val on the train set
            if console_messages == True:
                print("Datatlas: Getting model performance stats. Please be patient - this step uses cross validation with 3 folds")
            from sklearn.model_selection import cross_val_predict
            from sklearn.metrics import mean_squared_error
            from math import sqrt
            y_train_pred = cross_val_predict(sgd_reg, X_train, y_train, cv=3)
            
            impute_stats_dict = {'imputed_column': impute_column
                                ,'rmse': sqrt(mean_squared_error(y_train, y_train_pred))
                                ,'min_value': min(df[impute_column].dropna())
                                ,'max_value': max(df[impute_column].dropna())
                                ,'mean_value': df[impute_column].mean()
                                ,'original_nulls_num': null_n
                                ,'original_nulls_p': null_p
                                ,'remaining_nulls_num': sum(original_df[impute_column].isnull())
                                ,'remaining_nulls_p': sum(original_df[impute_column].isnull()) / original_df[impute_column].shape[0] * 100
                        }
            
            if impute_model == False:
                return original_df, impute_stats_dict # Yes stats, no model
            elif impute_model == True:
                return original_df, sgd_reg, impute_stats_dict # Yes stats, yes model
        
        
    if datatype == 'categoric':
        import sys
        sys.exit("Datatlas: Sorry, functionality to predict categoric values is still a work in progress")





###################################################################################################

### To enable this module to be called from another Python file
    
if __name__ == '__main__':
    predict_missing_values()






