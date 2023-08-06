import sys
import unittest
import os
import pandas as pds
import numpy as np
import dataschool.class_test_gen as ctg
import dataschool.matrix_creation as mc
import dataschool.statistic_viewer as sv
import dataschool.question_correlation as qc

class Test_class_gen(unittest.TestCase):
    def test_class(self):
        checker = False
        df = ctg.class_test()
        if {'id_eleve', 'id_question', 'module',
        'question', 'duree', 'correct'}.issubset(df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(77, len(df))

class Test_matrix_creation(unittest.TestCase):
    def test_matrix_reponse(self):
        df = pds.read_csv("./data/df_simul.csv")
        matrice_reponse = mc.matrice_reponse(df)
        result_m = pds.read_csv('./data/reponse_df.csv')
        matrice_reponse = np.array(matrice_reponse)
        result_m = result_m.drop('Unnamed: 0', axis=1)
        result_m = np.array(result_m)
        self.assertSequenceEqual(matrice_reponse.tolist(), result_m.tolist())

    def test_matrix_duree(self):
        df = pds.read_csv("./data/df_simul.csv")
        matrice_duree = mc.matrice_duree(df)
        result_m = pds.read_csv('./data/duree_df.csv')
        matrice_duree = np.array(matrice_duree)
        result_m = result_m.drop('Unnamed: 0', axis=1)
        result_m = np.array(result_m)
        self.assertSequenceEqual(matrice_duree.tolist(), result_m.tolist())

class Test_statistic_viewer(unittest.TestCase): #Mais pas les graphs car intestables
    def test_taux_reponse_moyen_eleve(self):
        checker = False
        df = sv.csv_to_df('./data/reponse_df.csv')
        new_df = sv.taux_reponse_moyen_eleve(df)
        if {'id_eleve', 'taux_reponse', 'taux_reussite'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(8, len(new_df))

    def test_taux_reponse_moyen_question(self):
        checker = False
        df = sv.csv_to_df('./data/reponse_df.csv')
        new_df = sv.taux_reponse_moyen_question(df)
        if {'id_question', 'taux_reponse', 'taux_reussite'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(10, len(new_df))

    def test_csv_to_df(self):
        new_df = sv.csv_to_df('./data/reponse_df.csv')
        checker = False
        if {'(1, 1)', '(1, 2)', '(1, 3)', '(1, 4)', '(1, 5)',
        '(2, 1)', '(2, 2)', '(2, 3)', '(2, 4)', '(2, 5)'}.issubset(new_df.columns):
            checker = True
        index_list = list(new_df.index)
        expected_list = list(['Einstein', 'Forrest Gump', 'Gauss', 'Marie Curie', 'Grace Hopper',
       'Macroyen', 'Youcernar', 'Paris Hilton'])
        self.assertEqual(True, checker)
        self.assertSequenceEqual(index_list, expected_list)

    def test_temps_moyen_eleve(self):
        checker = False
        df = sv.csv_to_df('./data/duree_df.csv')
        new_df = sv.temps_moyen_eleve(df)
        if {'id_eleve', 'temps_moyen', 'nombre_reponses'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(8, len(new_df))

    def test_temps_moyen_question(self):
        checker = False
        df = sv.csv_to_df('./data/duree_df.csv')
        new_df = sv.temps_moyen_question(df)
        if {'id_question', 'temps_moyen', 'nombre_reponses'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(10, len(new_df))

    def test_temps_maxmin_eleve(self):
        checker = False
        df = sv.csv_to_df('./data/duree_df.csv')
        new_df = sv.temps_maxmin_eleve(df)
        if {'id_eleve', 'temps_min', 'temps_max'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(8, len(new_df))

    def test_temps_maxmin_question(self):
        checker = False
        df = sv.csv_to_df('./data/duree_df.csv')
        new_df = sv.temps_maxmin_question(df)
        if {'id_question', 'temps_min', 'temps_max', 'eleve_min', 'eleve_max'}.issubset(new_df.columns):
            checker = True
        self.assertEqual(True, checker)
        self.assertEqual(10, len(new_df))

class Test_question_correlation(unittest.TestCase):
    def test_dic_eleve(self):
        df = sv.csv_to_df('./data/reponse_df.csv')
        dic = qc.create_dic_eleves(df)
        expected_dict = {'(1, 1)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(1, 2)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(1, 3)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(1, 4)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(1, 5)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(2, 1)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(2, 2)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(2, 3)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Marie Curie', 'Youcernar', 'Paris Hilton'},
                        '(2, 4)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Macroyen', 'Youcernar', 'Paris Hilton'},
                        '(2, 5)': {'Einstein', 'Forrest Gump', 'Grace Hopper', 'Gauss', 'Youcernar', 'Paris Hilton'}}
        self.assertSequenceEqual(dic, expected_dict)

    def test_dic_reussite_eleve(self):
        df = sv.csv_to_df('./data/reponse_df.csv')
        dic = qc.create_reussite_eleves(df)
        expected_dict = {'(1, 1)': {'Einstein', 'Youcernar', 'Forrest Gump', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(1, 2)': {'Einstein', 'Youcernar', 'Paris Hilton', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(1, 3)': {'Macroyen', 'Einstein', 'Gauss', 'Marie Curie'},
                        '(1, 4)': {'Einstein', 'Youcernar', 'Forrest Gump', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(1, 5)': {'Einstein', 'Gauss', 'Marie Curie'},
                        '(2, 1)': {'Einstein', 'Forrest Gump', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(2, 2)': {'Einstein', 'Youcernar', 'Forrest Gump', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(2, 3)': {'Einstein', 'Paris Hilton', 'Macroyen', 'Gauss', 'Grace Hopper', 'Marie Curie'},
                        '(2, 4)': {'Einstein', 'Forrest Gump', 'Gauss', 'Youcernar'},
                        '(2, 5)': {'Einstein', 'Gauss', 'Grace Hopper'}}
        self.assertSequenceEqual(dic, expected_dict)

    def test_matrice_proba(self):
        df = sv.csv_to_df('./data/reponse_df.csv')
        df_proba = qc.create_matrice_proba(df)
        df_proba = np.array(df_proba)
        self.assertTrue(df_proba.any() >= 0)
        self.assertTrue(df_proba.all() <= 1)

    def test_matrice_adjacence(self):
        df = sv.csv_to_df('./data/reponse_df.csv')
        df_proba = qc.create_matrice_proba(df)
        df_adja = qc.create_matrice_adjacence(df_proba, 0.8)
        df_adja = np.array(df_adja)
        self.assertTrue(df_adja.all() >= 0)
        self.assertTrue(df_adja.all() <= 1)

    def test_question_clustering(self):
        df = sv.csv_to_df('./data/reponse_df.csv')
        clust_df = qc.question_clustering(df, 3)
        clust_array = clust_df['cluster'].to_numpy()
        self.assertTrue(clust_array.all() >= 0)
        self.assertTrue(clust_array.all() <= 3)

#class Test_clustering(unittest.TestCase):
#    def test_niveaux_question(self):