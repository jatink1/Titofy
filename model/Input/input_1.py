import pandas as pd

import numpy as np
import tensorflow as tf
from tensorflow import keras

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from keras.models import load_model

input = pd.read_csv(r'Playlists_Of_User11.csv')
model = load_model('NN Model.h5')

input.drop_duplicates(subset=['Track_ID'] , inplace = True)

def padding(df_list): 
    
    len1 = len(df_list)
    
    remaining = 500-len1
    
    d = pd.DataFrame(np.zeros((remaining, 21)) , columns = df_list.columns)
    
    df_list = df_list.append(d)
    
    features_only = df_list[['Popularity', 'Danceability','Energy', 'Key', 'Loudness', 'Speechiness',
                               'Acousticness', 'Instrumentalness', 'Liveness', 'Tempo']]
    
    X = np.asarray(features_only)
    
    return X


X = padding(input)

if (len(X.shape) != 3):
    
    X = np.reshape(X, (-1,500,10))

# model = load_model(r'NN Model.h5')

pred = model.predict(X)

pred.shape

labels = np.load('labels.npy',allow_pickle=True)

newX = np.load('Xtransformed.npy',allow_pickle=True)

updateX = np.vstack((newX, pred))

updateX.shape

from sklearn.decomposition import PCA
pca = PCA()
x_pca = pca.fit_transform(updateX)
x_pca = pd.DataFrame(x_pca)

x_pca=x_pca[[0,1]]

from sklearn.cluster import KMeans


kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10)
y_kmeans=kmeans.fit_predict(x_pca)

x_pca['label_Kmeans_PCA'] = kmeans.labels_
x_pca.shape

x_pca.tail()

input_label = x_pca.iloc[2,-1]

print(labels[input_label])
