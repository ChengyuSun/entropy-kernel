# encoding:utf-8
import numpy as np
import csv
import tslearn.metrics as metrics
from scipy.spatial.distance import pdist, squareform


# gamma: a free parameter for the RBF kernel
# k : the number of components to be returned

def sq_dist():

    names = locals()
    for k in range(1, 5977):
        names['matrix%s'%k] = np.loadtxt(open("./d_sto/graph_" + str(k) + ".csv"), delimiter=",")
        print(k)
    # for i in range(5976):
    #     Matirx = "matrix" + str(i)
    #     Matrix = np.loadtxt(open("./d_sto/graph_" + str(i + 1) + ".csv"), delimiter=",")
    sq_dist = np.zeros((5976*(5976-1)/2), dtype=np.float32)
    zz = 0
    for i in range(1, 5976):
        for j in range(i+1, 5977):
            sq_dist[zz] = metrics.gak(names['matrix'+str(i)], names['matrix'+str(j)], sigma=2)
            zz = zz + 1
            print(zz)
    return sq_dist


def rbf_kpca(gamma, k):
    # Calculating the squared Euclidean distances for every pair of points


    # sq_dist = np.zeros((X.shape[0]*(X.shape[0]-1)/2), dtype=np.float32)
    # zz = 0
    # for i in range(X.shape[0]-1):
    #     for j in range(i+1, X.shape[0]):
    #         sq_dist[zz] = metrics.gak(X[i], X[j], sigma=2.1)
    #         zz = zz + 1



    # # in the M*N dimensional dataset
    # sq_dist = pdist(X, metric='gak')
    # # N = X.shape[0]
    # # sq_dist.shape = N*(N-1)/2


    # Converting the pairwise distances into a symmetric M*M matirx
    mat_sq_dist = squareform(sq_dist())
    # mat_sq_dist.shape = (N, N)


    # Computing the M*M kernel matrix
    # step 1
    K = np.exp(-gamma * mat_sq_dist)

    # Computing the symmetric N*N kernel matrix
    # step 2
    N = 5976
    one_N = np.ones((N, N)) / N
    K = K - one_N.dot(K) - K.dot(one_N) + one_N.dot(K).dot(one_N)

    # step 3
    Lambda, Q = np.linalg.eig(K)
    Lambda = np.real(Lambda)
    Q = np.real(Q)
    print(Lambda)
    eigen_pairs = [(Lambda[i], Q[:, i]) for i in range(len(Lambda))]
    eigen_pairs = sorted(eigen_pairs, reverse=True, key=lambda k: k[0])
    return np.column_stack((eigen_pairs[i][1] for i in range(k)))


def loadDataSet(filename):
    Entropy = []
    f = open(filename, 'r')  # num=count_Motifs(i)
    for line in f.readlines():
        line = line.strip('\r\n').split(',')
        line = [float(x) for x in line]
        Entropy.append(line)
    Entropy = np.array(Entropy)
    return Entropy


"""
for i in range(3):
    E = loadDataSet('M'+str(i+2)+'E.csv')
    E_kpca = rbf_kpca(E, gamma=15, k=3)
    with open('kPCA_M'+str(i+2)+'E.csv',"wb") as fc:
        csvWriter=csv.writer(fc)
        for i in range(len(E_kpca)):
            csvWriter.writerow(E_kpca[i])
        fc.close()
"""

# E = loadDataSet('directed-motif-entropy.csv')
E_kpca = rbf_kpca(gamma=15, k=15)
with open('./GAK/GAK_kernel-directed_sigma2.csv',"wb") as fc:
    csvWriter=csv.writer(fc)
    for i in range(len(E_kpca)):
        csvWriter.writerow(E_kpca[i])
    fc.close()



