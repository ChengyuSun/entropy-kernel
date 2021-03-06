path='../lib/libsvm-3.24/python'
import sys
sys.path.append(path)
sys.path.append('../')
from svmutil import *
from graphlet.count_graphlet import dataset_reps
from utils.util import read_graph_label,acc_calculator
import numpy as np
import random
from sklearn import svm
from utils.kPCA import js_kernel_process,select_level,GAK_process,dtw_process


def n_cross(n,index,nodN,random_idx):

    test_start=index*(nodN//n)
    test_end=test_start+(nodN//n)
    train_idx = random_idx[:test_start]+random_idx[test_end:]
    test_idx = random_idx[test_start:test_end]

    #print('test_idx from {} to {}'.format(test_start,test_end))
    return np.array(train_idx),np.array(test_idx)


def kernel_svm(kernel_values,labels,train_idx,test_idx):
    prob = svm_problem(labels[train_idx].tolist(), kernel_values[train_idx].tolist(), isKernel=True)
    param = svm_parameter('-t 4 -c 4 -b 1')
    model = svm_train(prob, param)
    p_label, p_acc, p_val = svm_predict(labels[test_idx].tolist(), kernel_values[test_idx].tolist(), model)
    return p_acc[0]

def normal_svm(features,labels,train_idx,test_idx):
    model = svm_train(labels[train_idx].tolist(), features[train_idx].tolist(), '-c 4')
    print("result:")
    p_label, p_acc, p_val = svm_predict(labels[test_idx].tolist(), features[test_idx].tolist(), model)
    return p_acc[0]

def sklearn_svm(features,labels,train_idx,test_idx):
    #print('starting training and testing sklearn_svm')
    clf_linear = svm.SVC(kernel='linear')
    #print('train_idx: ',train_idx)
    #print('features[train]: ',features[train_idx])
    #print('labels[train_idx]',labels[train_idx])
    clf_linear.fit(features[train_idx], labels[train_idx])
    score_linear = clf_linear.score(features[test_idx], labels[test_idx])
    #print("The score of linear is : %f" % score_linear)
    return score_linear*100


#
# max_level=0
# max_acc=0
# random_idx = [i for i in range(nodN)]
# random.shuffle(random_idx)
# for level in range(1,9):
#     select_level_features=select_level(original_features,level)
#     #kernel_features = dtw_process(select_level_features)
#     accs=[]
#     for i in range(10):
#         train_idx_temp, test_idx_temp = n_cross(10,i, nodN, random_idx)
#         accs.append(sklearn_svm(select_level_features,original_labels,train_idx_temp,test_idx_temp))
#         #accs.append(kernel_svm(kernel_features,original_labels,train_idx_temp,test_idx_temp))
#     avg=acc_calculator(accs)
#     if avg>max_acc:
#         max_level=level
#         max_acc=avg
# print('\n\n\n\ndataset: {}   acc: {}  best_level: {}'.format(dataset,max_acc,max_level))
# print('\n\n\n\n\n')



def ten_ten_svm(l):
    accs = []
    #
    #
    #
    features=select_level(original_features,l)
    #kernel_features=dtw_process(features)

    #
    #
    #

    for k in range(10):
        temp_accs = []
        random_idx = [i for i in range(nodN)]
        random.shuffle(random_idx)
        for i in range(10):
            train_idx_temp, test_idx_temp = n_cross(10, i, nodN, random_idx)
            print('ready for {}:{}'.format(k,i))
            temp_score=sklearn_svm(features,original_labels,train_idx_temp,test_idx_temp)
            print('{}:{}  score is {}'.format(k,i,temp_score))
            temp_accs.append(temp_score)
            #temp_accs.append(kernel_svm(kernel_features, original_labels,train_idx_temp, test_idx_temp))
        temp_res=acc_calculator(temp_accs)
        print('\n------temp_res: {} -------\n'.format(format(temp_res,'.2f')))
        accs.append(temp_res)

    print('\n\n\n--------------------------\n'
          '--------------------------\n'
          '----------result------------\n'
          '---------------------------\n'
          '---------------------------\n')
    print('dataset: ',dataset)
    acc_calculator(accs)




dataset='IMDB-BINARY'
is_server=True
original_features=dataset_reps(dataset,is_server)
original_labels=read_graph_label(dataset,is_server)
nodN=len(original_labels.tolist())

ten_ten_svm(8)