
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# # Tâche 0 : création d'une fausse classe

# Einstein (tout bon, mais très lent)
# Forrest Gump (tout aléatoire et très lent)
# Gauss (tout bon, tout rapide)
# Marie Curie (90% bon, 10% pas de réponse, tout rapide)
# Grace Hopper (3 bon, 2 faux, 4 bons, 1 faux), vitesse moyenne
# Macroyen (7 bons (les faciles), 2 faux (les difficiles), 1 sans réponse, vitesse moyen
# Yourcenar : (5 bons, 5 faux, temps : 5 minutes, 1h, 5 minutes, 2h, 5 minutes 3h...)
# Paris Hilton : (tout sur la première réponses = 8 faux, 2 bons, très rapide car pas de clavier tactile)

# MODULE 1 :
# - question 1 : (1, 1) -> facile
# - question 2 : (1, 2) -> facile
# - question 3 : (1, 3) -> facile
# - question 4 : (1, 4) -> facile
# - question 5 : (1, 5) -> difficile
#
# MODULE 2 :
# - question 1 : (2, 1) -> facile
# - question 2 : (2, 2) -> facile
# - question 3 : (2, 3) -> facile
# - question 4 : (2, 4) -> difficile
# - question 5 : (2, 5) -> difficile

# Liste des colonnes dont nous avons besoin :
#
# - id_eleve
# - id_question
# - module
# - question
# - duree
# - correct

def class_test():
    # Création de l'élève Einstein
    liste_einstein_q11 = ["Einstein", "(1, 1)", 1, 1, 65, True]
    liste_einstein_q12 = ["Einstein", "(1, 2)", 1, 2, 62, True]
    liste_einstein_q13 = ["Einstein", "(1, 3)", 1, 3, 66, True]
    liste_einstein_q14 = ["Einstein", "(1, 4)", 1, 4, 69, True]
    liste_einstein_q15 = ["Einstein", "(1, 5)", 1, 5, 65, True]
    liste_einstein_q21 = ["Einstein", "(2, 1)", 2, 1, 71, True]
    liste_einstein_q22 = ["Einstein", "(2, 2)", 2, 2, 69, True]
    liste_einstein_q23 = ["Einstein", "(2, 3)", 2, 3, 67, True]
    liste_einstein_q24 = ["Einstein", "(2, 4)", 2, 4, 68, True]
    liste_einstein_q25 = ["Einstein", "(2, 5)", 2, 5, 65, True]

    # Création de l'élève Forrest Gump
    liste_gump_q11 = ["Forrest Gump", "(1, 1)", 1, 1, 67, True]
    liste_gump_q12 = ["Forrest Gump", "(1, 2)", 1, 2, 62, False]
    liste_gump_q13 = ["Forrest Gump", "(1, 3)", 1, 3, 66, False]
    liste_gump_q14 = ["Forrest Gump", "(1, 4)", 1, 4, 71, True]
    liste_gump_q15 = ["Forrest Gump", "(1, 5)", 1, 5, 72, False]
    liste_gump_q21 = ["Forrest Gump", "(2, 1)", 2, 1, 68, True]
    liste_gump_q22 = ["Forrest Gump", "(2, 2)", 2, 2, 67, True]
    liste_gump_q23 = ["Forrest Gump", "(2, 3)", 2, 3, 70, False]
    liste_gump_q24 = ["Forrest Gump", "(2, 4)", 2, 4, 64, True]
    liste_gump_q25 = ["Forrest Gump", "(2, 5)", 2, 5, 69, False]

    # Création de l'élève Gauss
    liste_gauss_q11 = ["Gauss", "(1, 1)", 1, 1, 27, True]
    liste_gauss_q12 = ["Gauss", "(1, 2)", 1, 2, 26, True]
    liste_gauss_q13 = ["Gauss", "(1, 3)", 1, 3, 28, True]
    liste_gauss_q14 = ["Gauss", "(1, 4)", 1, 4, 28, True]
    liste_gauss_q15 = ["Gauss", "(1, 5)", 1, 5, 25, True]
    liste_gauss_q21 = ["Gauss", "(2, 1)", 2, 1, 26, True]
    liste_gauss_q22 = ["Gauss", "(2, 2)", 2, 2, 27, True]
    liste_gauss_q23 = ["Gauss", "(2, 3)", 2, 3, 26, True]
    liste_gauss_q24 = ["Gauss", "(2, 4)", 2, 4, 29, True]
    liste_gauss_q25 = ["Gauss", "(2, 5)", 2, 5, 27, True]

    # Création de l'élève Marie Curie
    liste_curie_q11 = ["Marie Curie", "(1, 1)", 1, 1, 24, True]
    liste_curie_q12 = ["Marie Curie", "(1, 2)", 1, 2, 28, True]
    liste_curie_q13 = ["Marie Curie", "(1, 3)", 1, 3, 25, True]
    liste_curie_q14 = ["Marie Curie", "(1, 4)", 1, 4, 27, True]
    liste_curie_q15 = ["Marie Curie", "(1, 5)", 1, 5, 28, True]
    liste_curie_q21 = ["Marie Curie", "(2, 1)", 2, 1, 26, True]
    liste_curie_q22 = ["Marie Curie", "(2, 2)", 2, 2, 27, True]
    liste_curie_q23 = ["Marie Curie", "(2, 3)", 2, 3, 35, True]

    # Création de l'élève Grace Hopper
    liste_hopper_q11 = ["Grace Hopper", "(1, 1)", 1, 1, 46, True]
    liste_hopper_q12 = ["Grace Hopper", "(1, 2)", 1, 2, 43, True]
    liste_hopper_q13 = ["Grace Hopper", "(1, 3)", 1, 3, 44, False]
    liste_hopper_q14 = ["Grace Hopper", "(1, 4)", 1, 4, 43, True]
    liste_hopper_q15 = ["Grace Hopper", "(1, 5)", 1, 5, 45, False]
    liste_hopper_q21 = ["Grace Hopper", "(2, 1)", 2, 1, 45, True]
    liste_hopper_q22 = ["Grace Hopper", "(2, 2)", 2, 2, 46, True]
    liste_hopper_q23 = ["Grace Hopper", "(2, 3)", 2, 3, 42, True]
    liste_hopper_q24 = ["Grace Hopper", "(2, 4)", 2, 4, 44, False]
    liste_hopper_q25 = ["Grace Hopper", "(2, 5)", 2, 5, 45, True]

    # Création de l'élève Macroyen
    liste_mantroyen_q11 = ["Mantroyen", "(1, 1)", 1, 1, 45, True]
    liste_mantroyen_q12 = ["Mantroyen", "(1, 2)", 1, 2, 44, True]
    liste_mantroyen_q13 = ["Mantroyen", "(1, 3)", 1, 3, 42, True]
    liste_mantroyen_q14 = ["Mantroyen", "(1, 4)", 1, 4, 44, True]
    liste_mantroyen_q15 = ["Mantroyen", "(1, 5)", 1, 5, 46, False]
    liste_mantroyen_q21 = ["Mantroyen", "(2, 1)", 2, 1, 44, True]
    liste_mantroyen_q22 = ["Mantroyen", "(2, 2)", 2, 2, 45, True]
    liste_mantroyen_q23 = ["Mantroyen", "(2, 3)", 2, 3, 44, True]
    liste_mantroyen_q24 = ["Mantroyen", "(2, 4)", 2, 4, 43, False]

    # Création de l'élève Yourcenar
    liste_yourcenar_q11 = ["Yourcenar", "(1, 1)", 1, 1, 51, True]
    liste_yourcenar_q12 = ["Yourcenar", "(1, 2)", 1, 2, 1800, True]
    liste_yourcenar_q13 = ["Yourcenar", "(1, 3)", 1, 3, 59, False]
    liste_yourcenar_q14 = ["Yourcenar", "(1, 4)", 1, 4, 1750, True]
    liste_yourcenar_q15 = ["Yourcenar", "(1, 5)", 1, 5, 1680, False]
    liste_yourcenar_q21 = ["Yourcenar", "(2, 1)", 2, 1, 54, False]
    liste_yourcenar_q22 = ["Yourcenar", "(2, 2)", 2, 2, 1500, True]
    liste_yourcenar_q23 = ["Yourcenar", "(2, 3)", 2, 3, 1524, False]
    liste_yourcenar_q24 = ["Yourcenar", "(2, 4)", 2, 4, 60, True]
    liste_yourcenar_q25 = ["Yourcenar", "(2, 5)", 2, 5, 1300, False]

    # Création de l'élève Paris Hilton
    liste_hilton_q11 = ["Paris Hilton", "(1, 1)", 1, 1, 19, False]
    liste_hilton_q12 = ["Paris Hilton", "(1, 2)", 1, 2, 20, True]
    liste_hilton_q13 = ["Paris Hilton", "(1, 3)", 1, 3, 18, False]
    liste_hilton_q14 = ["Paris Hilton", "(1, 4)", 1, 4, 19, False]
    liste_hilton_q15 = ["Paris Hilton", "(1, 5)", 1, 5, 19, False]
    liste_hilton_q21 = ["Paris Hilton", "(2, 1)", 2, 1, 17, False]
    liste_hilton_q22 = ["Paris Hilton", "(2, 2)", 2, 2, 16, False]
    liste_hilton_q23 = ["Paris Hilton", "(2, 3)", 2, 3, 18, True]
    liste_hilton_q24 = ["Paris Hilton", "(2, 4)", 2, 4, 21, False]
    liste_hilton_q25 = ["Paris Hilton", "(2, 5)", 2, 5, 18, False]

    data = [liste_einstein_q11, liste_einstein_q12, liste_einstein_q13, liste_einstein_q14, liste_einstein_q15,
            liste_einstein_q21, liste_einstein_q22, liste_einstein_q23, liste_einstein_q24, liste_einstein_q25,
            liste_gump_q11, liste_gump_q12, liste_gump_q13, liste_gump_q14, liste_gump_q15,
            liste_gump_q21, liste_gump_q22, liste_gump_q23, liste_gump_q24, liste_gump_q25,
            liste_gauss_q11, liste_gauss_q12, liste_gauss_q13, liste_gauss_q14, liste_gauss_q15,
            liste_gauss_q21, liste_gauss_q22, liste_gauss_q23, liste_gauss_q24, liste_gauss_q25,
            liste_curie_q11, liste_curie_q12, liste_curie_q13, liste_curie_q14, liste_curie_q15,
            liste_curie_q21, liste_curie_q22, liste_curie_q23,
            liste_hopper_q11, liste_hopper_q12, liste_hopper_q13, liste_hopper_q14, liste_hopper_q15,
            liste_hopper_q21, liste_hopper_q22, liste_hopper_q23, liste_hopper_q24, liste_hopper_q25,
            liste_mantroyen_q11, liste_mantroyen_q12, liste_mantroyen_q13, liste_mantroyen_q14, liste_mantroyen_q15,
            liste_mantroyen_q21, liste_mantroyen_q22, liste_mantroyen_q23, liste_mantroyen_q24,
            liste_yourcenar_q11, liste_yourcenar_q12, liste_yourcenar_q13, liste_yourcenar_q14, liste_yourcenar_q15,
            liste_yourcenar_q21, liste_yourcenar_q22, liste_yourcenar_q23, liste_yourcenar_q24, liste_yourcenar_q25,
            liste_hilton_q11, liste_hilton_q12, liste_hilton_q13, liste_hilton_q14, liste_hilton_q15,
            liste_hilton_q21, liste_hilton_q22, liste_hilton_q23, liste_hilton_q24, liste_hilton_q25]

    columns = ['id_eleve', 'id_question', 'module', 'question', 'duree', 'correct']
    df_simul = pd.DataFrame(data, columns = columns)
    return df_simul

if __name__ == "__main__":
    class_test()
    pass