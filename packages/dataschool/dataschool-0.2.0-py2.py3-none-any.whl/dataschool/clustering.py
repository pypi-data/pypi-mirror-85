import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import math

from matplotlib.pyplot import figure
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


# # Tâche 4 : Clustering des élèves

# Les variables sélectionnées pour le clustering :
# - nombre de questions auxquelles l'élève répond
# - temps moyen de réponse
# - taux de réussite
#
# Peut être remplacer par taux de complétion ?

def niveaux_questions(df, nbr_niveaux):
    liste_questions = df.columns.tolist()
    nbr_questions = len(liste_questions)
    liste_proba = []
    for question in liste_questions :
        liste_proba.append((question, df[df[question] == 1].shape[0]/df.shape[0]))
    liste_proba.sort(key=lambda tup: tup[1], reverse = True)
    index = nbr_questions//nbr_niveaux
    liste_index = [0]
    for i in range(1, nbr_niveaux):
        liste_index.append(index*i)
    liste_index.append(nbr_questions)
    dic_niveaux = {}
    for i in range(len(liste_index)-1):
        L = [e[0] for e in liste_proba[liste_index[i]:liste_index[i+1]]]
        dic_niveaux['niveau ' + str(i + 1)] = L
    return dic_niveaux

def reussite_niveau(eleve, liste_questions, df_rep):
    nbr_reussies = 0
    for question in liste_questions:
        if df_rep.loc[question, eleve] == 1:
            nbr_reussies += 1
    return nbr_reussies / len(liste_questions)

def creation_df_clustering(df_rep, df_dur, nbr_niveaux):
    L = []
    for eleve in list(df_dur.columns):
        l_eleve = []
        #on ajoute le nombre de questions auxquelle l'élève répond
        l_eleve.append(df_rep[df_rep[eleve] != -1].shape[0])
        #on ajoute le temps moyen de réponse
        l_eleve.append(df_dur[df_dur[eleve] != 0][eleve].mean())
        #on ajoute le taux de réussite
        if df_rep[df_rep[eleve] != -1].shape[0] == 0:
            l_eleve.append(0)
        else :
            l_eleve.append(df_rep[df_rep[eleve] == 1].shape[0] / df_rep[df_rep[eleve] != -1].shape[0])
        #On crée le dic des niveaux
        dic_niveaux = niveaux_questions(df_rep.T, nbr_niveaux)
        columns_niveaux = []
        for niveau in dic_niveaux.keys():
            columns_niveaux.append("réussite " + niveau)
            l_eleve.append(reussite_niveau(eleve, dic_niveaux[niveau], df_rep))
        L.append(l_eleve)
    columns = ['nbr_questions', 'temps_moyen', 'taux_reussite'] + columns_niveaux
    dataFrame = pd.DataFrame(L, columns = columns, index = list(df_dur.columns))
    return dataFrame

# maximum absolute scaling du dataframe -> normalisation des données
def maximum_absolute_scaling(df):
    df_scaled = df.copy()
    for column in df_scaled.columns:
        df_scaled[column] = df_scaled[column]  / df_scaled[column].abs().max()
    return df_scaled

def create_cluster_df(nbr_cluster, df_scaled, df_clustering):
    kmeans = KMeans(n_clusters=nbr_cluster).fit(df_scaled)
    df_clusters = df_clustering.copy()
    df_clusters['cluster'] = kmeans.labels_
    return df_clusters

# ### Taux de réponse et taux de réussite moyens par cluster

def taux_reponse_moyen_clusters(df_clusters, nbr_questions):
    nbr_clusters = df_clusters['cluster'].nunique()
    dic_cluster = {}
    for cluster in range(nbr_clusters):
        df_C = df_clusters[df_clusters.cluster == cluster]
        taux_reponse = 0
        taux_reussite = df_C['taux_reussite'].mean()
        for i in range(df_C.shape[0]):
            taux_reponse += df_C.iloc[i]['nbr_questions']/nbr_questions
        taux_reponse = taux_reponse/df_C.shape[0]
        taux = (taux_reponse, taux_reussite)
        key = "cluster " + str(cluster)
        dic_cluster[key] = taux
    dataF = pd.DataFrame({
        'cluster' : list(dic_cluster.keys()),
        'taux_reponse' : list(e[0] for e in dic_cluster.values()),
        'taux_reussite' : list(e[1] for e in dic_cluster.values())
    })
    return dataF

def show_taux_reussite_taux_reponse(data_reponse_clusters):
    res = sns.relplot(data=data_reponse_clusters, x="cluster", y="taux_reussite", height = 6, aspect = 3, s = 150).set(title = "Taux de réussite et taux de réponse par cluster")
    x = res.axes[0,0].get_xticks()
    b = res.axes[0,0].bar(x, data_reponse_clusters['taux_reponse'], width = 0.1, alpha = 0.1)
    res.axes[0,0].legend([b], ['Taux de réponse'], loc = 'upper right')
    res.axes[0,0].set_xticklabels(res.axes[0,0].get_xticklabels(), rotation=30)
    res.set_ylabels("Taux de réussite du cluster")
    plt.show()
    return

# ### Temps moyen par réponse, nombre de réponses par cluster

def temps_moyen_cluster(df):
    nbr_clusters = df['cluster'].nunique()
    dic_cluster = {}
    for cluster in range(nbr_clusters):
        df_C = df[df.cluster == cluster]
        key = "cluster " + str(cluster)
        dic_cluster[key] = (df_C['temps_moyen'].mean(), df_C['nbr_questions'].mean())
    dataF = pd.DataFrame({
        'cluster' : list(dic_cluster.keys()),
        'temps_moyen' : list(e[0] for e in dic_cluster.values()),
        'nombre_reponses' : list(e[1] for e in dic_cluster.values())
    })
    return dataF

def show_temps_moyen_cluster(dataframe_temps_moyen):
    _, ax = plt.subplots(figsize=(21, 7))
    x_de = ax.get_xticks()
    compteur = 0
    for i, j in zip(x_de, dataframe_temps_moyen['temps_moyen']):
        ax.text(x = i - 0.025, y = j+10, s = str(dataframe_temps_moyen.loc[compteur, 'nombre_reponses']))
        ax.text(x = i - 0.025, y = 1.5, s = str(dataframe_temps_moyen.loc[compteur, 'temps_moyen']), color = 'white')
        compteur += 1
    ax.set_ylabel("Temps moyen par question par cluster")
    ax.set_title("Temps moyen passé par question par cluster")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()

# ### Durée min max par cluster

def temps_minmax_cluster(df_duree, df_clust):
    nbr_clusters = df_clust['cluster'].nunique()
    dic_cluster = {}
    for cluster in range(nbr_clusters):
        min_clust = 0
        max_clust = 0
        key = "cluster " + str(cluster)
        liste_eleves = list(df_clust[df_clust.cluster == cluster].index)
        for eleve in liste_eleves:
            ser = df_duree.loc[eleve]
            ser = ser[ser != 0]
            min_clust += ser.min()
            max_clust += ser.max()
        dic_cluster[key] = (min_clust/len(liste_eleves), max_clust/len(liste_eleves))
    dataF = pd.DataFrame({
        'cluster' : list(dic_cluster.keys()),
        'temps_min' : list(e[0] for e in dic_cluster.values()),
        'temps_max' : list(e[1] for e in dic_cluster.values())
     })
    return dataF

def show_temps_minmax_cluster(df_temps_minmax):
    _, ax = plt.subplots(figsize=(21, 7))
    ax.set_ylim(df_temps_minmax['temps_max'].quantile(0.7))
    ax.invert_yaxis()
    bar_dq = ax.bar(df_temps_minmax['cluster'], df_temps_minmax['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(df_temps_minmax['cluster'], df_temps_minmax['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max moyenne du cluster sur une question", "Durée min moyenne du cluster sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par question par cluster")
    ax.set_title("Durée min et durée max passées sur une question par cluster")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()

def show_temps_minmax_cluster_log(df_temps_minmax):
    _, ax = plt.subplots(figsize=(21, 7))
    bar_dq = ax.bar(df_temps_minmax['cluster'], df_temps_minmax['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(df_temps_minmax['cluster'], df_temps_minmax['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max moyenne du cluster sur une question", "Durée min moyenne du cluster sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par question par cluster")
    ax.set_yscale("log")
    ax.set_title("Durée min et durée max passées sur une question par cluster")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()

def create_pca(df_scaled, df_reponse, df_cluster):
    featuresPCA_eleve = df_scaled.copy()
    featuresPCA_eleve = StandardScaler().fit_transform(featuresPCA_eleve)
    pca_eleve = PCA(n_components=2)
    principalComponents_eleve = pca_eleve.fit_transform(featuresPCA_eleve)
    principalDf_eleve = pd.DataFrame(data = principalComponents_eleve, columns = ['principal component 1', 'principal component 2'], index = list(df_reponse.index))
    pca_eleve_df = pd.concat([principalDf_eleve, df_cluster[['cluster']]], axis = 1)
    return pca_eleve_df

def show_pca(pca_eleve_df, nbr_clusters):
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
    for target, color in zip(targets,colors):
        indicesToKeep = pca_eleve_df['cluster'] == target
        ax.scatter(pca_eleve_df.loc[indicesToKeep, 'principal component 1']
                , pca_eleve_df.loc[indicesToKeep, 'principal component 2']
                , c = color
                , s = 50)
    ax.legend(targets)
    ax.grid()
    plt.show()
    return