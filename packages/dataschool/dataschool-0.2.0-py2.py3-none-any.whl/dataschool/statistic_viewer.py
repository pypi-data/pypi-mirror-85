import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import math

def csv_to_df(path_to_csv):
    df = pd.read_csv(path_to_csv)
    index = list(df['Unnamed: 0'])
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.set_index(pd.Index(index))
    return df

def taux_reponse_moyen_eleve(df):
    liste_eleves = df.index.tolist()
    liste_questions = df.columns.tolist()
    nbr_questions = len(liste_questions)
    dic_eleve = {}
    for eleve in liste_eleves:
        nbr_pas_repondu = 0
        nbr_juste = 0
        for question in liste_questions:
            x = df.loc[eleve, question]
            if x == - 1:
                nbr_pas_repondu += 1
            elif x == 1:
                nbr_juste += 1
        taux = ((nbr_questions - nbr_pas_repondu)/nbr_questions, nbr_juste/(nbr_questions - nbr_pas_repondu))
        dic_eleve[eleve] = taux
    dataF = pd.DataFrame({
        'id_eleve' : list(dic_eleve.keys()),
        'taux_reponse' : list(e[0] for e in dic_eleve.values()),
        'taux_reussite' : list(e[1] for e in dic_eleve.values())
    })
    return dataF

def show_taux_reponse_moyen_eleve(df_reponse):
    data_reponse_eleve = taux_reponse_moyen_eleve(df_reponse)
    data_reponse_eleve = data_reponse_eleve.sort_values('taux_reussite', ascending = False)
    res = sns.relplot(data=data_reponse_eleve, x="id_eleve", y="taux_reussite", height = 6, aspect = 3, s = 150).set(title = "Taux de réussite et taux de réponse par élève")
    x = res.axes[0,0].get_xticks()
    b = res.axes[0,0].bar(x, data_reponse_eleve['taux_reponse'], width = 0.2, alpha = 0.1)
    res.axes[0,0].legend([b], ['Taux de réponse'], loc = 'upper right')
    res.axes[0,0].set_xticklabels(res.axes[0,0].get_xticklabels(), rotation=30)
    res.set_ylabels("Taux de réussite de l'élève")
    plt.show()
    return

# ### Taux de réponse réponse / taux de bonne réponse PAR QUESTI
def taux_reponse_moyen_question(df):
    liste_eleves = df.index.tolist()
    liste_questions = df.columns.tolist()
    nbr_eleves = len(liste_eleves)
    dic_question = {}
    for question in liste_questions:
        nbr_pas_repondu = 0
        nbr_juste = 0
        for eleve in liste_eleves:
            x = df.loc[eleve, question]
            if x == - 1:
                nbr_pas_repondu += 1
            elif x == 1:
                nbr_juste += 1
        taux = ((nbr_eleves - nbr_pas_repondu)/nbr_eleves, nbr_juste/(nbr_eleves - nbr_pas_repondu))
        dic_question[question] = taux
    dataF = pd.DataFrame({
        'id_question' : list(dic_question.keys()),
        'taux_reponse' : list(e[0] for e in dic_question.values()),
        'taux_reussite' : list(e[1] for e in dic_question.values())
    })
    return dataF

def show_taux_reponse_moyen_question(df_reponse):
    data_reponse_question = taux_reponse_moyen_question(df_reponse)
    data_reponse_question = data_reponse_question.sort_values('taux_reussite', ascending = False)
    res_q = sns.relplot(data=data_reponse_question, x="id_question", y="taux_reussite", height = 6, aspect = 3, s = 150).set(title = "Taux de réussite et taux de réponse par question")
    x = res_q.axes[0,0].get_xticks()
    b = res_q.axes[0,0].bar(x, data_reponse_question['taux_reponse'], width = 0.2, alpha = 0.1)
    res_q.axes[0,0].legend([b], ['Taux de réponse'], loc = 'upper right')
    res_q.axes[0,0].set_xticklabels(res_q.axes[0,0].get_xticklabels(), rotation=30)
    res_q.set_ylabels("Taux de réussite par question")
    plt.show()
    return

# ### Temps moyen par réponse / nombre de réponses PAR ELEVE
def temps_moyen_eleve(df):
    liste_eleves = df.index.tolist()
    liste_questions = df.columns.tolist()
    dic_eleve = {}
    for eleve in liste_eleves:
        nbr_repondu = 0
        duree = 0
        for question in liste_questions :
            x = df.loc[eleve, question]
            if x != 0:
                nbr_repondu += 1
                duree += x
        dic_eleve[eleve] = (duree/nbr_repondu, nbr_repondu)
    dataF = pd.DataFrame({
        'id_eleve' : list(dic_eleve.keys()),
        'temps_moyen' : list(e[0] for e in dic_eleve.values()),
        'nombre_reponses' : list(e[1] for e in dic_eleve.values())
    })
    return dataF

def show_temps_moyen_eleve(df_duree):
    df_tempsmoyen_eleve = temps_moyen_eleve(df_duree)
    df_tempsmoyen_eleve = df_tempsmoyen_eleve.sort_values('temps_moyen', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    x_de = ax.get_xticks()
    compteur = 0
    for i, j in zip(x_de, df_tempsmoyen_eleve['temps_moyen']):
        ax.text(x = i - 0.04, y = j+10, s = str(df_tempsmoyen_eleve.loc[compteur, 'nombre_reponses']))
        ax.text(x = i - 0.08, y = 1.5, s = str(df_tempsmoyen_eleve.loc[compteur, 'temps_moyen']), color = 'white')
        compteur += 1
    ax.set_ylabel("Temps moyen par question par élève")
    ax.set_title("Temps moyen passé par question par élève")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return

# ### Temps moyen par réponse / nombre de réponses PAR QUESTION
def temps_moyen_question(df):
    liste_eleves = df.index.tolist()
    liste_questions = df.columns.tolist()
    dic_question = {}
    for question in liste_questions:
        nbr_repondu = 0
        duree = 0
        for eleve in liste_eleves :
            x = df.loc[eleve, question]
            if x != 0:
                nbr_repondu += 1
                duree += x
        dic_question[question] = (duree/nbr_repondu, nbr_repondu)
    dataF = pd.DataFrame({
        'id_question' : list(dic_question.keys()),
        'temps_moyen' : list(e[0] for e in dic_question.values()),
        'nombre_reponses' : list(e[1] for e in dic_question.values())
    })
    return dataF

def show_temps_moyen_question(df_duree):
    df_tempsmoyen_question = temps_moyen_question(df_duree)
    df_tempsmoyen_question = df_tempsmoyen_question.sort_values('temps_moyen', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    x_dq = ax.get_xticks()
    compteur = 0
    for i, j in zip(x_dq, df_tempsmoyen_question['temps_moyen']):
        ax.text(x = i - 0.04, y = j+4, s = str(df_tempsmoyen_question.loc[compteur, 'nombre_reponses']))
        ax.text(x = i - 0.1, y = 1.5, s = str(df_tempsmoyen_question.loc[compteur, 'temps_moyen']), color = 'white')
        compteur += 1
    ax.set_ylabel("Temps moyen passé par élève")
    ax.set_title("Temps moyen passé par élève par question")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return

# ### Temps min max PAR ELEVE
def temps_maxmin_eleve(df):
    liste_eleves = df.index.tolist()
    dic_eleve = {}
    for eleve in liste_eleves:
        ser = df.loc[eleve]
        ser = ser[ser != 0]
        dic_eleve[eleve] = (ser.min(), ser.max())
    dataF = pd.DataFrame({
        'id_eleve' : list(dic_eleve.keys()),
        'temps_min' : list(e[0] for e in dic_eleve.values()),
        'temps_max' : list(e[1] for e in dic_eleve.values())
     })
    return dataF

# Graphique avec l'axe des y limité
def show_maxmin_eleve_y_limited(df_duree):
    df_minmax_eleve = temps_maxmin_eleve(df_duree)
    df_minmax_eleve = df_minmax_eleve.sort_values('temps_max', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    ax.set_ylim(df_minmax_eleve['temps_max'].quantile(0.87))
    ax.invert_yaxis()
    bar_dq = ax.bar(df_minmax_eleve['id_eleve'], df_minmax_eleve['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(df_minmax_eleve['id_eleve'], df_minmax_eleve['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max de l'élève sur une question", "Durée min de l'élève sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par question par élève")
    ax.set_title("Durée min et durée max passées sur une question par élève")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return

# Graphe avec échelle logarithmique
def show_maxmin_eleve_logarithmic_scale(df_duree):
    df_minmax_eleve = temps_maxmin_eleve(df_duree)
    df_minmax_eleve = df_minmax_eleve.sort_values('temps_max', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    #ax.set_ylim(df_minmax_eleve['temps_max'].quantile(0.87))
    #ax.invert_yaxis()
    bar_dq = ax.bar(df_minmax_eleve['id_eleve'], df_minmax_eleve['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(df_minmax_eleve['id_eleve'], df_minmax_eleve['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max de l'élève sur une question", "Durée min de l'élève sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par question par élève")
    ax.set_yscale("log")
    ax.set_title("Durée min et durée max passées sur une question par élève (échelle logarithmique)")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return

# ### Temps min max PAR QUESTION
def temps_maxmin_question(df):
    liste_questions = df.columns.tolist()
    dic_question = {}
    for question in liste_questions:
        ser = df[[question]]
        ser = ser[ser != 0]
        dic_question[question] = (ser.min()[0], ser.max()[0], ser.idxmin()[0], ser.idxmax()[0])
    dataF = pd.DataFrame({
        'id_question' : list(dic_question.keys()),
        'temps_min' : list(e[0] for e in dic_question.values()),
        'eleve_min' : list(e[2] for e in dic_question.values()),
        'temps_max' : list(e[1] for e in dic_question.values()),
        'eleve_max' : list(e[3] for e in dic_question.values())
     })
    return dataF

def show_time_maxmin_question(df_duree):
    df_minmax_question = temps_maxmin_question(df_duree)
    df_minmax_question = df_minmax_question.sort_values('temps_max', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    ax.set_ylim(df_minmax_question['temps_max'].quantile(0.4))
    ax.invert_yaxis()
    bar_dq = ax.bar(x = df_minmax_question['id_question'], height = df_minmax_question['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(x = df_minmax_question['id_question'], height = df_minmax_question['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max d'un élève sur une question", "Durée min d'un élève sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par élève par question")
    ax.set_title("Durée min et durée max passées par un élève par question")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return

def show_time_maxmin_question_logarithmic_scale(df_duree):
    df_minmax_question = temps_maxmin_question(df_duree)
    df_minmax_question = df_minmax_question.sort_values('temps_max', ascending = False)
    _, ax = plt.subplots(figsize=(21, 7))
    ax.set_yscale("log")
    bar_dq = ax.bar(x = df_minmax_question['id_question'], height = df_minmax_question['temps_max'], width = 0.2, alpha = 0.5)
    bar_dqm = ax.bar(x = df_minmax_question['id_question'], height = df_minmax_question['temps_min'], width = 0.2, alpha = 0.7, color = 'orange')
    ax.legend([bar_dq, bar_dqm], ["Durée max d'un élève sur une question", "Durée min d'un élève sur une question"], loc = 'upper left')
    ax.set_ylabel("Temps par élève par question")
    ax.set_title("Durée min et durée max passées par un élève par question (échelle logarithmique)")
    ax.tick_params(axis='x', labelrotation=30)
    plt.show()
    return