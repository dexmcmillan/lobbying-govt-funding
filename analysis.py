import pandas as pd
import numpy as np

## Run > pip3 install pandas
## Run > pip3 install numpy
## Run > python3 analysis.py
## Watch the magic happen!

## This just sets the format for numbers so it doesn't default to scientific.
pd.options.display.float_format = '${:,.2f}'.format

## Load in files containing raw data from the govt registry, one with govt funding amounts and the other with company names.
records = pd.read_csv("./data.csv")
funding = pd.read_csv("./funding.csv")

## Set the index to be the registration ID, which is unique and maps to funding.
records = records.set_index("REG_ID_ENR")

## Merge the two data sets on REG_ID_ENR.
data = records.merge(right=funding, on="REG_ID_ENR")

## Fill in blank cells in the English name with whatever is in the French name column so we only need one column.
data["EN_CLIENT_ORG_CORP_NM_AN"] = data["EN_CLIENT_ORG_CORP_NM_AN"].fillna(data["FR_CLIENT_ORG_CORP_NM"])

## Drop all columns except for these three: name of company, name of funding agency, and the amount received.
data = data[["EN_CLIENT_ORG_CORP_NM_AN", "INSTITUTION", "AMOUNT_MONTANT"]]

## Reshape and show only the maximum value. The dataset contains multiple records that represent different updates to the registrant.
max = data.groupby(['EN_CLIENT_ORG_CORP_NM_AN', "INSTITUTION"], as_index=False)["AMOUNT_MONTANT"].max()

## Filter for only those that may be COVID-19 funding and sort to show highest first.
max = max[max["INSTITUTION"].str.contains('cra|CEWS|wage subsidy|covid|revenu', regex=True, case=False)]
max = (max.sort_values("AMOUNT_MONTANT", ascending=False).dropna())

## Print to console and copy to clipboard (go CTRL-V somewhere and see what happens...)
print(max)
max.to_clipboard()