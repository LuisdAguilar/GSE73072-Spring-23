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
df_tags = df.pop('ID_REF')
df = df.T

# the storage for the meta data of the experiment
meta = df_meta.iloc[0,:]
meta = meta.drop(0)

# storage for the times which the samples were taken
times = np.zeros(len(meta))

# storage for the names of the specific virus 
virus_name = []

# storage for the subject number
subjects = []

# creating a loop that finds the time, virus name, and subject name 
# from the meta data and adds them to the previously created arrays
for i in range(len(meta)):
    k = i+1
    # accesing the data and storing it into a new variable 
    info = meta[k]
    # first pattern for finding the times when the samples were taken
    pattern = re.compile("[a-zA-z0-9\ \,]* Hour (-?[0-9]*)")
    # second pattern for finding the virus name
    pattern1 = re.compile("(^[A-Z0-9]*)")
    # third pattern for finding the subject ID
    pattern2 = re.compile("^[A-Z0-9]* ([a-zA-Z0-9\ ]*)")
    # storing the matches from every pattern into variables
    m = re.match(pattern, info)
    m1 = re.match(pattern1, info)
    m2 = re.match(pattern2, info)
    # adding into our storage arrays the relevant data found from the matches
    times[i] = m.group(1)
    virus_name.append(m1.group(1))
    subjects.append(m2.group(1))

# turning all of our storage into data frames with the purpose of adding them
# into the main data frame
times = pd.DataFrame(times, columns = ['Time'], index = df.index)
virus_name = pd.DataFrame(virus_name, columns = ['Virus'], index = df.index)
subjects = pd.DataFrame(subjects, columns = ['Subject'], index = df.index)

### 

# Combine=ing the new information found from the meta data into the original 
# data frame

# first adding the virus name and subject name into a new data frame
df_info = pd.concat([virus_name,subjects], axis = 1)
# then adding in the times into the new data frame
df_info = pd.concat([df_info,times], axis = 1)

# adding in the meta data to the original data frame
df1 = pd.concat([df_info,df],axis = 1)

###

# Masking and creating data frames for specific criteria

# creating a data frame for only the pre infection data points
pre_inf = df1
pre_inf = pre_inf[pre_inf.Time <=0]

# creating a data frame containing only the H1N1 subjects
swine_flu = df1
swine_flu = swine_flu[swine_flu.Virus == 'H1N1']
