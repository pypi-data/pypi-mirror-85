import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import networkx as nx
import math

from matplotlib.pyplot import figure
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# # Tâche 3 :  Corrélation entre questions

#On crée un dictionnaire qui stocke tous les élèves qui ont tenté la question

def create_dic_eleves(df):
    dic = {}
    liste_questions = list(df.columns)
    for question in liste_questions :
        dic[question] = set(df[df[question] != -1].index.tolist())
    return dic

#On crée un dictionnaire qui stocke tous les élèves qui ont réussi la question

def create_reussite_eleves(df):
    dic = {}
    liste_questions = list(df.columns)
    for question in liste_questions:
        dic[question] = set(df[df[question] == 1].index.tolist())
    return dic

def intersection(set1, set2):
    return len(set1 & set2)

# P(réussir q2 sachant qu'on a réussi q1) = (nombre de personnes qui ont fait juste à q1 et q2)/(nombre de personnes qui ont fait juste à q1 et qui ont répondu à q2)

def create_matrice_proba(df):
    dic_eleves_tenter = create_dic_eleves(df)
    dic_eleves_reussite = create_reussite_eleves(df)
    dic_proba = {}
    liste_questions = list(df.columns)
    for q1 in liste_questions:
        dic_key = {}
        for q2 in liste_questions:
            if q2 == q1:
                dic_key[q2] = 0
            else:
                if intersection(dic_eleves_reussite[q1], dic_eleves_tenter[q2]) == 0:
                    dic_key[q2] = 0
                else:
                    dic_key[q2] = intersection(dic_eleves_reussite[q1], dic_eleves_reussite[q2])/intersection(dic_eleves_reussite[q1], dic_eleves_tenter[q2])
        dic_proba[q1] = dic_key
    dataF = pd.DataFrame(dic_proba)
    dataF = dataF.T
    return dataF

def show_matrice_proba(proba_matrix):
    g = sns.clustermap(proba_matrix, cmap = "mako")
    g.fig.suptitle("Probabilité de réussir une question sachant qu'on en a réussi une autre")
    #g.ax_heatmap.set_title('lalal')
    plt.show()
    return

def create_matrice_adjacence(proba_matrix, seuil): #seuil = 0.8
    liste_questions = list(proba_matrix.columns)
    dic_adjacence = {}
    for q1 in liste_questions :
        dic_key = {}
        for q2 in liste_questions:
            if proba_matrix.loc[q1, q2] >= seuil and proba_matrix.loc[q2, q1] >= seuil :
                dic_key[q2] = 1
            else :
                dic_key[q2] = 0
        dic_adjacence[q1] = dic_key
    daF = pd.DataFrame(dic_adjacence)
    return

def create_mapping(df):
    mapping = {}
    for i, column in enumerate(df.columns):
        mapping[i] = column
    return mapping

def show_adjacence(adjacence_matrix, mapping):
    mat = adjacence_matrix.to_numpy()
    G = nx.from_numpy_matrix(mat)
    figure(figsize=(10, 8))
    G = nx.relabel_nodes(G, mapping)
    nx.draw_shell(G, with_labels=True, node_size = 1400)
    plt.title('Corrélation entre les questions')
    plt.show()
    return

# # Clustering des questions

def question_clustering(df_reponse, nb_cluster):
    kmeans = KMeans(n_clusters=nb_cluster).fit(df_reponse.T)
    df_cluster = df_reponse.T
    df_cluster['cluster'] = kmeans.labels_
    return df_cluster

def show_clustering_PCA(df_cluster, df_reponse, nbr_clusters):
    featuresPCA = df_reponse.T
    featuresPCA = StandardScaler().fit_transform(featuresPCA)
# Projection PCA en 2D
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(featuresPCA)
    principalDf = pd.DataFrame(data = principalComponents
                , columns = ['principal component 1', 'principal component 2'], index = list(df_reponse.columns))
    finalDf = pd.concat([principalDf, df_cluster[['cluster']]], axis = 1)
# Visualisation de la projection 2D PCA
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 Component PCA', fontsize = 20)
    targets = np.empty(nbr_clusters, dtype=int)
    for i in range(nbr_clusters):
        targets[i] = i
    colors_to_choose = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'peachpuff', 'lightseagreen', 'peru', 'sandybrown', 'seashell', 'turquoise', 'aquamarine', 'lightcyan']
    colors = colors_to_choose[:nbr_clusters]
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf['cluster'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                , finalDf.loc[indicesToKeep, 'principal component 2']
                , c = color
                , s = 50)
    ax.legend(targets)
    ax.grid()
    plt.show()
    return