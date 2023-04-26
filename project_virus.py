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

swine_flu = df.drop(df.iloc[:,864:2887], axis = 1)

# the storage of all the times for the experiments found within the meta data
times_str = df_meta.iloc[0,:]
times_str = times_str.drop(0)
# an array that will take only the time values from the array as integers
times_int = np.zeros(len(times_str))

# creating a loop that finds the time values from the times array
for i in range(1, len(times_str)):
    info = times_str[i]
    pattern = re.compile("[a-zA-z0-9\ \,]* Hour (-?[0-9]*)")
    m = re.match(pattern, info)
    times_int[i] = m.group(1)

times_int = np.array(times_int, dtype =  int)
times_int = np.delete(times_int, 0)

# with the times stored in an array we can now find the pre 
# infection columns from the blood samples

# taking our data frame and removing the column with the protein tags so as to
# just work with the numbers

df_noprotein = df

# making a data frame that will only contain the values of pre infection patients
pre_inf = df_noprotein.pop('ID_REF')
pre_inf = pd.DataFrame(pre_inf)
b = np.zeros(len(times_int))

for j in range(len(times_int)):
    print(j)
    print(times_int[j])
    if times_int[j] <= 0:
        pre_inf = pd.concat([pre_inf, df_noprotein.iloc[:,j]], axis = 1)

