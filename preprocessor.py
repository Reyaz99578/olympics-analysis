import pandas as pd


def preprocess(df, region_df):
    df = df[df['Season'] == 'Summer']
    df = df.merge(region_df, on='NOC', how='left')
    df = df.drop_duplicates()
    medals = pd.get_dummies(df['Medal'], dtype=int)
    medals = medals.reindex(columns=['Gold', 'Silver', 'Bronze'], fill_value=0)
    df = pd.concat([df, medals], axis=1)
    return df
