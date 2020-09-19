import pandas as pd
import numpy as np

import glob
import os
import pandas as pd

from sklearn.preprocessing import MinMaxScaler


def features1(df):
    
    features = []
    
    user_mean = get_mean(df)

    for i in range(0, len(user_mean)):
    
        if (user_mean[i] > avg_mean[i]):
        
            features.append(1)
    
        elif (user_mean[i] == avg_mean[i]):
        
            features.append(1)
        
        elif (user_mean[i] < avg_mean[i]):
        
            features.append(0)
            
    return features


def get_features_all(dataframe_combined):
    
    s1 = []
    
    usernames = list(dataframe_combined['Username'].unique())
    
    s = []
    
    for i in usernames:
        
        df_username = dataframe_combined[dataframe_combined['Username'] == i]
        
        s = features1(df_username)
        
        s1.append(s)  
    
    return s1


def get_mean(df):

    scaler = MinMaxScaler()

    data = df[['Popularity', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
       'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']]

    df[['Popularity', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
       'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']] = scaler.fit_transform(df[['Popularity', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
       'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']])

    list1 = list(df.mean(axis=0))
    
    avg_features_df = pd.DataFrame(data = list1 , index = ['Duration_ms','Popularity','Explicit', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
       'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo','Time_Signature'])
    
    
    
    avg_features_df = avg_features_df.transpose()

    avg_features_df.drop(['Duration_ms','Explicit','Time_Signature'] , axis = 1,inplace = True)
    
    elements = [0,2,12]
    
    for ele in sorted(elements, reverse = True):  
        del list1[ele] 
        
    return list1





dataframe_combined = pd.read_csv(r'C:\Users\ROSHAN\Titofy\Combined.csv' , encoding= 'unicode_escape')
average = pd.read_csv(r'C:\Users\ROSHAN\Titofy\Average.csv', encoding= 'unicode_escape')

avg_mean = average.iloc[0]
avg_mean = list(avg_mean)


all_features = get_features_all(dataframe_combined)  
all_features = np.asarray(all_features)


folder_name = r"C:\Users\ROSHAN\Titofy\Data"
file_type = 'csv'
seperator =','
filenames = os.listdir(folder_name)
print(filenames)

df_list = []
for f in glob.glob(folder_name + "/*."+file_type):
    dd = pd.read_csv(f, sep=seperator,encoding= 'unicode_escape') 
    df_list.append(dd)


    
def remove_error(df_list):
    
    df_list_new = []
    
    for i in df_list:
        
        i = i[i["Popularity"] != "Popularity"]
        
        df_list_new.append(i)
        
    return df_list_new

df_list = remove_error(df_list)



def padding(df_list):
    
    dataframe_list = []

    for i in df_list:

        len1 = len(i)

        remaining = 500-len1

        #print(remaining)

        d = pd.DataFrame(np.zeros((remaining, 21)) , columns = i.columns)

        i = i.append(d)

        dataframe_list.append(i)

    X = []
    
    for i in dataframe_list:

        features_only = i[['Popularity', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
                               'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']]

        X.append(features_only.values)


    X = np.asarray(X)
    
    return X


X = padding(df_list)

print(all_features, X)

print(all_features.shape , X.shape)