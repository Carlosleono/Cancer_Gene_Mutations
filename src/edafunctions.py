import nltk
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, log_loss
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


sns.set_context("poster")
sns.set(rc={"figure.figsize": (12.,10.)})
sns.set_style("whitegrid")

from nltk.corpus import stopwords
nltk.download('stopwords');


def heatmap(x):
    """
    This function creates a heatmap from a dataframe given
    """
    corr = x.corr()
    mascara = np.triu(np.ones_like(corr, dtype=bool)) # generate mask for superior triangle
    color_map = sns.diverging_palette(0, 10, as_cmap=True) # Color palette
    return sns.heatmap(corr,  
                mask = mascara,
                cmap='viridis',
                square=True, #sea data as squares
                linewidth=0.5, 
                vmax=1,
                cbar_kws={"shrink": .5}, #lateral bar
                annot=True
            )

def unique(feature, df):
    '''
    This functions shows the number of unique values of a feature and show the 10 most frequent ones'''
    unique = df[feature].value_counts()
    print(f'Number of Unique {feature} :', unique.shape[0])

    # Top 10 most frequent genes
    print(unique.head(10))

def hist_and_cumdistr(feature, df):
    '''
    This functions plots histogram and cumulative distribution of a feature
    '''
    unique = df[feature].value_counts()
    s = sum(unique.values)
    h = unique.values/s

    plt.plot(h, label=f"Histrogram of {feature}")
    plt.xlabel(f'Index of a {feature}')
    plt.ylabel('Number of Occurances')
    plt.legend()
    plt.grid()
    plt.show()

    c = np.cumsum(h)
    plt.plot(c,label=f'Cumulative distribution of {feature}')
    plt.grid()
    plt.legend()
    plt.show()

def ua_sgdclassifier(feature, df, test_df, cv_df, y_train, y_cv):
    '''
    This function trains and predict the class feature based on just one feature. It return the log loss for several alpha values
    '''
    vectorizer = CountVectorizer()

    train_feature_onehotCoding = vectorizer.fit_transform(df[feature])
    test_feature_onehotCoding = vectorizer.transform(test_df[feature])
    cv_feature_onehotCoding = vectorizer.transform(cv_df[feature])

    print(f" The shape of {feature} feature:", train_feature_onehotCoding.shape)

    alpha = [10 ** x for x in range(-5, 1)]
    cv_log_error_array=[]
    for i in alpha:
        clf = SGDClassifier(alpha=i, loss='log')
        clf.fit(train_feature_onehotCoding, y_train)
        sig_clf = CalibratedClassifierCV(clf, method="sigmoid")
        sig_clf.fit(train_feature_onehotCoding, y_train)
        predict_y = sig_clf.predict_proba(cv_feature_onehotCoding)
        cv_log_error_array.append(log_loss(y_cv, predict_y))
        print('For values of alpha:', i, "The log loss is:", log_loss(y_cv, predict_y))
    