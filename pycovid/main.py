#!/usr/bin/python

import getopt, sys
from datetime import datetime
import pandas as pd
import json

argumentList = sys.argv[1:]

# options
options = ""

# long options
long_options = ["country=", "date="]

# filters
search_country = ""
search_date = ""

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
    
    # checking each argument
    for currentArgument, currentValue in arguments:
        
        if currentArgument in ("--country"):
            search_country = currentValue
             
        elif currentArgument in ("--date"):
            try:
                search_date = datetime.strptime(currentValue, "%d/%m/%Y").strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                print("--invalid date format (dd/mm/yyyy)")
                sys.exit(2)
            
    if not search_country:
        print("--country was not given")
        sys.exit(2)
    
    if not search_date:
        print("--date was not given")
        sys.exit(2)
        
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
except (ValueError, TypeError):
    print ("Error inesperado")
    
# Read dataframe from file 'covid-cases.csv'
df = pd.read_csv("covid-cases.csv")
#print(df.head(100))

# fix date format column to "dd/mm/yyyy"
df["date"] = pd.to_datetime(df.date)
df["date"] = df["date"].dt.strftime("%d/%m/%Y")
#print(df.head(100))

# search by date & country
df_result = df.loc[(df["date"] == search_date) & (df["country"] == search_country)]
#print(df_result)

# parse data result to default panda json schema
#json_result = df_result.to_json(orient="records")
#print(json_result)

# parse data result to custom json schema
json_result = json.dumps([{"country": row["country"], "date": row["date"], "report": {"cases": row["cases"], "deaths": row["deaths"]}} for i, row in df_result.iterrows()])
print(json_result)
