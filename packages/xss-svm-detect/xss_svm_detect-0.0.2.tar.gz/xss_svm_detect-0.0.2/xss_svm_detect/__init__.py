import sys
import urllib
from urllib.parse import urlparse
import re
from hmmlearn import hmm
import numpy as np
import html
from html.parser import HTMLParser
import nltk
import pickle
from sklearn.model_selection import train_test_split
from DataProcessing.DataProcessor import DataProcessor
from sklearn.svm import LinearSVC


def train(X_train,y_train):

    clf = LinearSVC()  # create svc linear mode
    clf.fit(X_train, y_train)  # train the mode
    resnum = 0
    with open("svm-xss-train.pkl", 'wb') as file:
        pickle.dump(clf, file)
    return clf


def test(X_test,y_test):
    resnum = 0
    with open("svm-xss-train.pkl", 'rb') as file:
        clf = pickle.load(file)
    for i in range(len(X_test)):
        result = clf.predict([X_test[i]])  # get the prediction
        print('predict result vs label：', result[0], y_test[i])
        a = str(result[0]).strip()
        b = str(y_test[i]).strip()
        if a == b:
            resnum += 1
    print("final result:")
    print("total hits")
    print(resnum)
    print("total test sample")
    print(len(X_test))
    print("accuracy:")
    print(resnum / len(X_test))


def init_process():
    print("xss module start!")
    dataProcessor = DataProcessor(5)
    # svm process

    # clf = create_xss_svc('./xssfile.txt' , './normalinput.txt')
    # data process from source xss and white sample file
    X, Y = dataProcessor.dataProcessingForSVM("./DataProcessing/xss-20000.txt",
                                              "./DataProcessing/labeled_data.csv")  # For SVM
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

    return[X_train, X_test, y_train, y_test]


if __name__ == '__main__':
    res_list = init_process()

    #train(res_list[0],res_list[2])

    test(res_list[1],res_list[3])
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
