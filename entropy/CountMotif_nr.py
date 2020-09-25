#encoding: utf-8
import numpy as np
import csv
import copy
# number of motif

Nm = 8
Ng=5976

def read_adjMatrix(i):  #读取一个图文件，返回matrix和大小
    array = open('./data/graph' + str(i) + '.csv').readlines()
    N = len(array)
    matrix = []
    for line in array:
        line = line.strip('\r\n').split(',')
        line = [int(x) for x in line]
        matrix.append(line)
    matrix = np.array(matrix)
    return matrix,N

def count_Motifs(i):
    # A,nodN=read_adjMatrix(i)
    rd=np.argsort(sum(np.transpose(A)))
    rdA=A[rd]
    rdA[:,]=rdA[:,rd]
    A2=np.array(np.ndarray(A)**2)
    A3=np.array(np.ndarray(A)**3)
    A4=np.array(np.ndarray(A)**4)
    num_triangle=count_triangle(A3,nodN)
    num_quads=count_quads(A2,A4,nodN)
    Nm_1=count_chain(rdA,nodN,2)
    Nm_2=count_chain(rdA,nodN,3)
    Nm_3=count_polygon0(num_triangle,3)
    Nm_4=count_chain(rdA,nodN,4)
    Nm_5=count_star(rdA,nodN,3)
    Nm_6=count_polygon0(num_quads,4)
    Nm_7=count_chain(rdA,nodN,5)
    Nm_8=count_star(rdA,nodN,4)
    num=[Nm_1,Nm_2,Nm_3,Nm_4,Nm_5,Nm_6,Nm_7,Nm_8]
    return num

def count_star(A,N,neiN):
    n=0
    a=copy.copy(A)
    for i in range(N):
        if (np.sum(a[i])>neiN-1):
            n+=1
            for j in range(i):
                a[N-j-1][i]=0
            x=np.nonzero(a[i])
            nei_Index=x[0][:neiN]
            a[i].fill(0)
            for j in nei_Index:
                a[j].fill(0)
                for k in range(N):
                    a[k][j]=0
    return n
def find_next(a,N,i,rest):
    if rest==0:
        a[i].fill(0)
        for j in range(N):
            a[j][i] = 0
        return i
    else:
        if np.sum(a[i])>0:
            for j in range(N):
                a[j][i]=0
            x = np.nonzero(a[i])
            a[i].fill(0)
            next_Index=x[0][0]
            return find_next(a,N,next_Index,rest-1)
        else:
            return -1
def count_chain(A,N,len):
    n=0
    a = copy.copy(A)
    for i in range(N):
        if find_next(a,N,i,len-1)>=0:
            n+=1
    return n
"""
def circle_find_next(a,N,i,rest):
    if rest==0:
        return i
    else:
        if np.sum(a[i])>0:
            for j in range(N):
                a[j][i]=0
            x = np.nonzero(a[i])
            a[i].fill(0)
            next_Index=x[0]
            for k in next_Index:
                return circle_find_next(a,N,k,rest-1)
        else:
            return -1
def count_polygon(A,N,edges):
    n=0
    a=copy.copy(A)
    for i in range(N):
        if circle_find_next(a,N,i,edges)==i:
            n+=1
    return n
"""

def count_quads(A2,A4,N):
    re=0
    n=0
    for i in range(N):
        for j in range(N):
            if j==i:
                re+=A2[i][j]**2
            else: re+=A2[i][j]
        if(A4[i][i]-re)>=2:n+=1
        re=0
    return n
def count_triangle(A3,N):
    n=0
    for i in range(N):
        if A3[i][i]>=2: n+=1
    return n

def count_polygon0(num,edges):
    n=num/edges
    return n
#
# with open("./files/CountMotif_nr1.csv","wb") as fc:
#     csvWriter=csv.writer(fc)
#     for i in range(Ng):
#         csvWriter.writerow(count_Motifs(i+1))
#     fc.close

count_Motifs(10)



