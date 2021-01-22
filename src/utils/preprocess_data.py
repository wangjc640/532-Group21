import pandas as pd

#designed to be run from the root folder of the project

# read in raw datasets
df = pd.read_csv("data/raw/world-data-gapminder_raw.csv")
country_ids = pd.read_csv("data/raw/country-ids.csv")

#calculate education ratio
df["education_ratio"] = df.years_in_school_men / df.years_in_school_women

# filter years to start at 1950
df = df.loc[df['year'] >= 1950]

# merge country id's to gapminder data
df_merged = pd.merge(df, country_ids, how='left',
                    left_on='country', right_on='name')

# write df to disk
df_merged.to_csv("data/processed/gapminder_processed.csv")