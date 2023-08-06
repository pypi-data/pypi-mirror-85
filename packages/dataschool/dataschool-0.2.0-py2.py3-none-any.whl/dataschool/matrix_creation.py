import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# # Tâche 1 : transformer les données de façon à avoir deux matrices

# ### Matrice élève / question / bonne réponse (ou pas de réponse)  (ligne / colonne / valeur)
def matrice_reponse(df):
    liste_eleves = list(df['id_eleve'].unique())
    liste_questions = list(df['id_question'].unique())
    L = []
    for eleve in liste_eleves:
        l = []
        data = df[df.id_eleve == eleve]
        for question in liste_questions:
            data_q = data[data.id_question == question]
            if data_q.shape[0] == 0:
                l.append(-1)
            else :
                if data_q.iloc[0]['correct'] == True:
                    l.append(1)
                else:
                    l.append(0)
        L.append(l)
    dataFrame = pd.DataFrame(L, columns = liste_questions, index = liste_eleves)
    return dataFrame

# ### Matrice élève / question / temps mis à répondre (durée)  (ligne / colonne / valeur)
def matrice_duree(df):
    liste_eleves = list(df['id_eleve'].unique())
    liste_questions = list(df['id_question'].unique())
    L = []
    for eleve in liste_eleves:
        l = []
        data = df[df.id_eleve == eleve]
        for question in liste_questions:
            data_q = data[data.id_question == question]
            if data_q.shape[0] == 0:
                l.append(0)
            else :
                l.append(data_q.iloc[0]['duree'])
        L.append(l)
    dataFrame = pd.DataFrame(L, columns = liste_questions, index = liste_eleves)
    return dataFrame