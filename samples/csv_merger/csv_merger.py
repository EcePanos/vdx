import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from pathlib import Path
import service_redis as service

service.create_algorithm("simple", collation='nearest_neighbor', error=0.05, bootstrapping=True)

# change this so it returns the file names
def validate(prefix, idx, filenames):
    
    Path("result").mkdir(parents=True, exist_ok=True)
    filenames.sort()
    n = len(filenames)
    dfs = []
    for filename in filenames:
        df_temp = pd.read_csv(filename)
        dfs.append(df_temp)
    #get all unique idx values from all dataframes in dfs
    idxs = []
    for df in dfs:
        idx_temp = df[idx].unique()
        #print(idx_temp)
        for item in idx_temp:
            if item not in idxs:
                idxs.append(item)
    #print(idxs)
    # for each idx value, get the row from each dataframe
    result = []
   # print(result)
    for value in idxs:
        result_row = [value]
        rows = []
        for df in dfs:
            row = df.loc[df[idx] == value]
            rows.append(row)
        print(rows)
        #print('-'*50)
        for column in rows[0].columns:
            mean = None
            temp = []
            for row in rows:
                try:
                    temp.append(row[column].values[0])
                except:
                    pass
            candidates = temp
            for i in range(len(temp)):
                service.create_candidate(temp[i])
            if column != idx and is_numeric_dtype(rows[0][column]):
                mean, history, weights = service.vote_num('simple', candidates, temp)
                result_row.append(mean)
                #print(mean)
            elif column != idx and not is_numeric_dtype(rows[0][column]):
                #majority vote between the values in temp
                mean, history = service.vote_alpha('simple', candidates, temp)
                result_row.append(mean)
                #print(mean)
        result.append(result_row)
    df = pd.DataFrame(result, columns= dfs[0].columns.tolist())
    print(df)
    df.to_csv(f'result/{prefix}_merged.csv', index=False)

validate('diffs', 'e1', ['voter/diffs.csv', 'voter/diffs2.csv', 'voter/diffs3.csv'])

        




   