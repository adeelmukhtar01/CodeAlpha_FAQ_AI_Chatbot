import pandas as pd

df = pd.read_excel("faq_data.xlsx", engine="openpyxl")

print(df)