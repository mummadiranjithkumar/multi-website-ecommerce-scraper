import pandas as pd
import re

def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates(subset=['product_name', 'url'])

    # Convert price to numeric
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')

    # Handle missing values
    df = df.dropna(subset=['product_name', 'price'])

    # Standardize product names: lowercase, remove extra spaces
    df['product_name'] = df['product_name'].str.lower().str.strip()
    df['product_name'] = df['product_name'].apply(lambda x: re.sub(r'\s+', ' ', x))

    return df