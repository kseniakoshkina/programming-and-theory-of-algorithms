import pandas as pd
import numpy as np
import copy
import fasttext
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_excel('trips_data_for_ML.xlsx', index_col=0)  #пробный датафрейм


class DFWrapper():

    def __init__(self, new_df, name_of_target, vectorizer_to_choose):
        self.new_df = new_df.copy().dropna(how='all')
        self.name_of_target = name_of_target
        self.new_df = self.new_df.drop(self.name_of_target, axis=1)
        self.vectorizer_to_choose = vectorizer_to_choose

    @property
    def features(self):
        features = self.new_df.loc[:, self.new_df.columns]
        type_of_features = features.dtypes.to_dict()
        for column in type_of_features:
            if type_of_features[column] == 'object':
                if type(self.new_df[column][0]) == list or
                type(self.new_df[column][0]) == dict or
                type(self.new_df[column][0]) == set or
                type(self.new_df[column][0]) == tuple:
                    self.new_df = self.new_df.loc[:, self.new_df.columns != column]
                elif len(self.new_df[column].unique()) <=
                0.1 * self.new_df.shape[0]:
                    new_df_2 = pd.get_dummies(self.new_df[column], prefix=column)
                    self.new_df = self.new_df.drop(columns=[column])
                    second_df = pd.concat([self.new_df, new_df_2], axis=1)
                    self.new_df = second_df
                else:
                    fasttext_model = fasttext.load_model('cc.ru.300.bin')
                    for i in self.new_df[column].tolist():
                        self.new_df[column] = ft.get_sentence_vector(i)
        return self.new_df.loc[:, self.new_df.columns != self.name_of_target]

    def fit(self, model_skl):
        features = self.features.to_numpy()
        model = eval(model_skl + "()")
        model_finished = model.fit(features, self.new_df[self.name_of_target])
        return model_finished


k = DFWrapper(df,'target','fasttext')
k.features





