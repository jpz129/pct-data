import pandas as pd

df = pd.read_csv('data/hiking_trends.csv', parse_dates=['Month'])
df = df.groupby(df.Month.dt.year).agg(['mean', 'std']).reset_index()
df.columns = df.columns.to_flat_index()
df.columns = ['year', 'hiking_mean', 'hiking_std']
df['year'] = df['year'] - 1

pct = pd.read_csv('data/pct_permits.csv')
df = pct.merge(df)
df.to_csv('data/pct_permits_hiking.csv', index=False)