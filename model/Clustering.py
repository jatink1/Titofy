import numpy as np
from tensorflow.keras.models import load_model

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

pca = PCA()

x_pca = pca.fit_transform(newX)
x_pca = pd.DataFrame(x_pca)

x_pca=x_pca[[0,1]]


kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, n_init=10)
y_kmeans=kmeans.fit_predict(x_pca)

x_pca['label_Kmeans_PCA'] = kmeans.labels_

dict1 = {}
count =  0
for i in x_pca['label_Kmeans_PCA']:
    dict1[count] = i
    
    count += 1