import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy import stats


def remove_selected_columns(df, columns_remove):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    return result_df.drop(columns=columns_remove)

# Create a function to remove rows with missing values in specific columns
def remove_rows_with_missing_data(df, columns):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    if columns:
        result_df = result_df.dropna(subset=columns)
    return result_df

# Create a function to fill missing data with mean, median, or mode (for numerical columns)
def fill_missing_data(df, columns, method):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    for column in columns:
        if method == 'mean':
            result_df[column] = result_df[column].fillna(result_df[column].mean())
        elif method == 'median':
            result_df[column] = result_df[column].fillna(result_df[column].median())
        elif method == 'mode':
            mode_val = result_df[column].mode().iloc[0]
            result_df[column] = result_df[column].fillna(mode_val)
    return result_df


def one_hot_encode(df, columns):
    # Create one-hot encoded dataframe
    result_df = pd.get_dummies(df, columns=columns, prefix=columns, drop_first=False)
    return result_df


def label_encode(df, columns):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    label_encoder = LabelEncoder()
    for col in columns:
        result_df[col] = label_encoder.fit_transform(result_df[col])
    return result_df



def standard_scale(df, columns):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    scaler = StandardScaler()
    result_df[columns] = scaler.fit_transform(result_df[columns])
    return result_df

def min_max_scale(df, columns, feature_range=(0, 1)):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    scaler = MinMaxScaler(feature_range=feature_range)
    result_df[columns] = scaler.fit_transform(result_df[columns])
    return result_df

def detect_outliers_iqr(df, column_name):
    data = df[column_name]
    q25, q50, q75 = np.percentile(data, [25, 50, 75])
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    outlier_indices = [i for i in range(len(data)) if data.iloc[i] < lower_bound or data.iloc[i] > upper_bound]
    return outlier_indices



# Function to detect outliers using z-score
def detect_outliers_zscore(df, column_name):
    data = df[column_name]
    z_scores = np.abs(stats.zscore(data))
    threshold = 3  # Define a threshold (e.g., 3 is commonly used)
    outlier_indices = [i for i in range(len(data)) if z_scores[i] > threshold]
    return outlier_indices


def remove_outliers(df, column_name, outlier_indices):
    return df.drop(index=df.index[outlier_indices]).reset_index(drop=True)

def transform_outliers(df, column_name, outlier_indices):
    # Create a copy to avoid modifying the original
    result_df = df.copy()
    if outlier_indices:
        # Calculate median from non-outlier values
        non_outlier_mask = ~result_df.index.isin(outlier_indices)
        median_value = result_df.loc[non_outlier_mask, column_name].median()
        # Replace outliers with median
        result_df.iloc[outlier_indices, result_df.columns.get_loc(column_name)] = median_value
    return result_df
