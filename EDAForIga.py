

import pandas as pd
df = pd.read_excel("C:/Users/DELL/PycharmProjects/PythonProject/Tennis/Iga.xlsx")
print(df.isnull().sum())

print(df.describe())

print(df.dtypes)


df[['Outcome', 'Opponent']] = df['Result'].str.split('vs', n=1, expand=True)
print(df[['Result', 'Outcome', 'Opponent']].head())

#df.drop(columns=['Result'], inplace=True)
#df[['FHWPerPtNoAceNoDFs', 'BHWPerPointNoAceNoDFs']] = df[['FHWPerPtNoAceNoDFs', 'BHWPerPointNoAceNoDFs']].transform(lambda x: x.fillna(x.median()))

3print(df.isnull().values.any())  # Returns True if there are any NaNs in the DataFrame
df.to_excel("C:/Users/DELL/PycharmProjects/PythonProject/Tennis/Iga_Cleaned2.xlsx", index=False)
