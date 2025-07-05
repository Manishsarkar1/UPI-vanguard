import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(filepath):
    #load the CSV file
    df = pd.read_csv(filepath)

    #Save original copy of the dataframe (for debugging purpose)
    df_raw = df.copy()

    #Encode categorial columns
    label_cols = ["device", "city", "transaction_type", "status"]
    encoder = {} #store encoders if needed later 

    for col in label_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoder[col] = le

    #Drop non-feature columns for ML
    x = df.drop(columns = ["transaction_id", "timestamp"])
    
    return x, encoder