import pandas as pd
url = 'https://raw.githubusercontent.com/tsdata/pandas-data-analysis/refs/heads/main/part7/data/wolesale_customers.csv'
df = pd.read_csv(url)
print(df.head())