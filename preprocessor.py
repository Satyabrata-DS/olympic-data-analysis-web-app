
import pandas as pd
import numpy as np

def preprocess(file_path):  # Accept file_path as a parameter
    df = pd.read_csv(file_path)  # Read the CSV file
    df['Medal'] = df['Medal'].replace('No medal', np.nan)  # Replace 'No medal' with NaN
    df.drop_duplicates(inplace=True)  # Remove duplicates
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)  # One-hot encoding
    return df

