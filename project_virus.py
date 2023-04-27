import pandas as pd
import numpy as np
import re

# line 46 has the title of hours
df_meta = pd.read_csv("GSE73072_series_matrix.txt",
                     skiprows=45,
                     nrows=81-46,
                     sep='\t',
                     header=None
                     )
df = pd.read_csv("GSE73072_series_matrix.txt", sep = "\t", skiprows = 82)
df = df.drop(12023)
df = df.drop(['ID_REF'], axis = 1)
df = df.T

# the storage of all the times for the experiments found within the meta data
times_str = df_meta.iloc[0,:]
times_str = times_str.drop(0)
# an array that will take only the time values from the array as integers
times_int = np.zeros(len(times_str))

# creating a loop that finds the time values from the times array
for i in range(len(times_str)):
    k = i+1
    info = times_str[k]
    pattern = re.compile("[a-zA-z0-9\ \,]* Hour (-?[0-9]*)")
    m = re.match(pattern, info)
    times_int[i] = m.group(1)

times_int = pd.DataFrame(times_int, columns = ['Time'], index = df.index)
# creating a loop that will take the virus names and store them
virus_name = []

for j in range(len(times_str)):
    c = j+1
    name = times_str[c]
    pattern1 = re.compile("(^[A-Z0-9]*)")
    m1 = re.match(pattern1, name)
    virus_name.append(m1.group(1))

virus_name = pd.DataFrame(virus_name, columns = ['Virus'], index = df.index)
  
### 
# Combine the new columns into the original data frame

# new data frame that combines the virus names and times
df_info = pd.concat([virus_name,times_int], axis = 1)

# combine both dataframes
df1 = pd.concat([df_info,df],axis = 1)
