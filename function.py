# Lecture de fichier CSV 
# Remplissage du tableau
import csv
from numpy import matrix, random
import pandas as pd
import requests
from ast import literal_eval
import numpy as np
from itertools import permutations
import math
import copy




def remplissageMatrice(file_path):
    i=0
    j=0
    rows, cols = (6, 6)
    matrix = [[0 for i in range(cols)] for j in range(rows)]
    with open(file_path, 'r') as file:
        csvreader = csv.reader(file)
        matrix[0][0]='Villes'
        for row in csvreader:
            i+=1
            matrix[i][0]=row[0]

    with open(file_path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            j+=1
            matrix[0][j]=row[0]
    return matrix


#seconde code
# Remplissage de la table avec les distance entre les villes




def matriceDistance(file_path):
    i=0
    j=0
    matrix = remplissageMatrice(file_path)
    with open(file_path, 'r') as file :
        csvreader = csv.reader(file)
        for row in csvreader:
            file1 = open(file_path)
            csvreader1 = csv.reader(file1)
            i+=1
            j=0
            for row1 in csvreader1:
                j+=1
                x = requests.get(f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={row[1]}/{row[2]}&destinations={row1[1]}/{row1[2]}&key=IVdsiVNXao4d2Wp22OKKUlnMVaXiq')
                data = literal_eval(x.text)
                data= data.get('rows')[0].get('elements')[0].get('distance').get('text')
                if data.split()[1] != 'm':
                    matrix[i][j]=float(data.split()[0])
                else:
                    matrix[i][j]=0
    return matrix
#data_df = pd.DataFrame(matrix)
#data_df


#---------------------Clarke and Wright---------------------#

def matriceEconomies(file_path):
    matrix = matriceDistance(file_path)
    rows, cols = (5, 5)
    economies = [[0 for i in range(cols)] for j in range(rows)]
    for i in range(1,6):
        for j in range(1,6):
            economies[i-1][j-1] = matrix[i][1] + matrix[1][j] - matrix[i][j]
    return economies
 

#data_eco = pd.DataFrame(economies)
#print(data_eco)

def matrixInf(file_path):
    economies = matriceEconomies(file_path)
    for i in range(1,len(economies)):
        for j in range(1,len(economies)): 
            if((i==j)|(economies[i][j]==economies[j][i])):
                economies[j][i]=0
    return economies

#print('___________')
#print(economies)



def clarkeAndWright(file_path):
    economies = matrixInf(file_path)
    T = [1,1]
    w, h = 5, 5
    mat_null = [[0] * w for i in range(h)]
    for i in range(1,len(economies)):
        for j in range(1,len(economies)):   
            if((economies[i][j]==np.max(economies))):
                if ((i+1 not in T) & (j+1 not in T)): 
                    T.insert(1,i+1)
                    T.insert(2,j+1)
                    economies[i][j]=0
                    break
    while economies != mat_null:
        for i in range(1,len(economies)):
            for j in range(1,len(economies)):   
                if((economies[i][j]==np.max(economies))):
                    #print ( i+1 , " ", j+1)
                    #print(T)
                    if ((i+1 in T) & (j+1 in T)): 
                        economies[i][j]=0 
                    elif ((i+1 not in T) & (j+1 not in T)): 
                        economies[i][j]=0 
                    elif((i+1==T[1]) & (j+1 not in T)):
                        T.insert(1,j+1)
                        economies[i][j]=0 
                    elif((i+1==T[len(T)-2]) & (j+1 not in T)):
                        T.insert(len(T)-1,j+1) 
                        economies[i][j]=0
                    elif((j+1==T[1]) & (i+1 not in T)):
                        T.insert(1,i+1)
                        economies[i][j]=0 
                    elif((j+1==T[len(T)-2]) & (i+1 not in T)):
                        T.insert(len(T)-1,i+1) 
                        economies[i][j]=0 
                    else:
                        economies[i][j]=0  
    return T

def tourneeVille(file_path,T):
    tournee_Ville = []
    matrix = remplissageMatrice(file_path)
    for i in range(len(T)):
        tournee_Ville.insert(i,matrix[T[i]][0])
    return tournee_Ville



#---------------------Branch and Bound---------------------

NB_TOWNS = 5
starting_town = [None] * NB_TOWNS
ending_town = [None] * NB_TOWNS
best_solution = [1] * NB_TOWNS
best_eval = -1.0
count = 0
coord = np.empty((NB_TOWNS, 2))
dist = np.zeros((NB_TOWNS,NB_TOWNS))

#Evaluation function (total distance)
def evaluation_solution(sol):
    eval = 0.0
    for i in range(NB_TOWNS-1):
        eval += dist[sol[i]-1][sol[i+1]-1]
    eval += dist[sol[NB_TOWNS-1]-1][sol[0]-1]
    return eval


#Builds final solution
def build_solution():
    global best_eval
    solution = [None] * NB_TOWNS
    currentIndex = 0
    currentNode = 0
    while currentIndex < NB_TOWNS:
        solution[currentIndex] = currentNode
        #Test if cycle is hamiltonien
        for i in range(currentIndex):
            if solution[i] == currentNode:
                #print("Cycle non-hamiltonien")
                return
        #Recherche de la ville suivante
        found = False
        i = 0
        while ((not found) and i < NB_TOWNS):
            if starting_town[i] == currentNode:
                found = True
                currentNode = ending_town[i]
            i += 1
        currentIndex += 1
    eval = evaluation_solution(solution)
    if best_eval < 0 or eval < best_eval:
        best_eval = eval
        for i in range(NB_TOWNS):
            best_solution[i] = solution[i]

    return
    


def branch_and_bound(dist, iteration, evalParentNode):
    #Number of total iterations
    global count
    count += 1
    if (iteration == NB_TOWNS):
        build_solution()
        return
    #Creation of a copy of the distance matrix
    m = copy.deepcopy(dist)
    evalChildNode = evalParentNode
    #Substracting min value of rows 
    minValueRow = np.amin(m, 1)
    for i in range(NB_TOWNS): 
        if not 0 in m[i,:] and minValueRow[i] != math.inf:
            m[i] -= minValueRow[i]
            evalChildNode += minValueRow[i] #Updating the current lower bound

    #Substracting min value of columns 
    minValueColumn = np.amin(m, 0,)
    for i in range(NB_TOWNS):
        if not 0 in m[:,i] and minValueColumn[i] != math.inf:
            m[:,i] -= minValueColumn[i]
            evalChildNode += minValueColumn[i] #Updating the current lower bound

    #Cut : stop the exploration of this node
    if (best_eval >= 0 and evalChildNode >= best_eval):
        return 
    #Calculating penalties (for zeros)
    minValueRow = np.amin(m, 1)
    minValueColumn = np.amin(m, 0,)
    listZeros = []
    #Count number of zeros on each row and column
    nbZerosR = NB_TOWNS - np.count_nonzero(m, 0)
    nbZerosC = NB_TOWNS - np.count_nonzero(m, 1)
    maxZero = (-1,0,0)
    for i in range(NB_TOWNS):
        for j in range(NB_TOWNS):
            if m[i,j] == 0:
                minR = 0 if nbZerosR[i] > 1 else min([value for value in m[i] if value != 0])
                minC = 0 if nbZerosC[j] > 1 else min([value for value in m[:,j] if value!=0])
                if minR == math.inf:
                    minR = 0
                if minC == math.inf:
                    minC = 0
                v = minR + minC
                listZeros.append((v, i, j))
                if (maxZero[0] < v):
                    maxZero = (v,i,j)
    if listZeros == []:
        return
    #Updates paths
    starting_town[iteration] = maxZero[1]
    ending_town[iteration] = maxZero[2]
    #Creating a copy of current distance matrix for left exploration (choice)
    m2 = copy.deepcopy(m)
    #Modifying new distance matrix
    m2[maxZero[2], maxZero[1]] = math.inf  #Set inf value
    m2[maxZero[1],:] = math.inf
    m2[:,maxZero[2]] = math.inf
    #Explore left branch of tree (choice)
    branch_and_bound(m2, iteration + 1, evalChildNode)
    #Creating a copy of current distance matrix for right exploration (non-choice)
    m3 = copy.deepcopy(m)
    #Modifying new distance matrix
    m3[maxZero[2], maxZero[1]] = math.inf  #Set inf value
    m3[maxZero[1], maxZero[2]] = math.inf  #Set inf value
    #Explore right branch of tree (non-choice)
    branch_and_bound(m3, iteration , evalChildNode)

def branchAndBound(path_file):
    matrci = matriceDistance(path_file)
    matrci.pop(0)
    for i in range(len(matrci)):
        matrci[i].pop(0)
    dist = np.array(matrci)
    iteration = 0
    lowerbound = 0.0
    np.fill_diagonal(dist, math.inf)
    branch_and_bound(dist, iteration, lowerbound)
    return best_solution
    



#---------------------VNS---------------------
def allPermutations(aleatoire_tournee):
    fixed_index= 0 # "Depot"
    fixed_element= aleatoire_tournee[fixed_index]
    newList = []
    rest_elements= aleatoire_tournee[:fixed_index] + aleatoire_tournee[fixed_index+1:]
    for permutation in permutations(rest_elements):
        newList.append((fixed_element,) + permutation)
    return newList

#print(newList)
def methodeVNS(file_path,newList):
    matrix=matriceDistance(file_path)
    distances = []
    for i in range(len(newList)):
        distance = 0
        for j in range(len(newList[i])-1):
            distance += float(matrix[newList[i][j]][newList[i][j+1]])
        distances.append(distance)
    t_VNS = newList[distances.index(min(distances))]
    return t_VNS




#---------------------NN---------------------

def distance(df, A, c):
    cities = list(df.columns.values)[1:]
    ind_A = cities.index(A) +1
    ind_c = cities.index(c)+1
    dist = df.iat[ind_A, ind_c]
    return dist

def first(collection):
    "Start iterating over collection, and return the first element."
    return next(iter(collection))


def nn_tsp(df):
    cities = list(df.columns.values)[1:]
    start = first(cities)
    tour = [start]
    unvisited = set(set(cities) - {start})
    while unvisited:
        C = nearest_neighbor(df, tour[-1], unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour

def nearest_neighbor(df, A, cities):
    return min(cities, key=lambda c: distance(df, c, A))







#----------------------------Test----------------------------#


# print('---------------------Clarke and Wright---------------------') 
# path_file = "C:/Users/merye/Desktop/INPT/INE3/S5/P1/Gestion des opérartions de transport/Projet_TMS/Villes.csv"
# tournee = clarkeAndWright(path_file)
# tounee_Ville = tourneeVille(path_file,tournee)
# print(tournee)
# print(tounee_Ville)


# print('---------------------VNS---------------------') 


# aleatoire_tournee = [1, 3, 5, 4, 2]
# T_VNS = methodeVNS(path_file,allPermutations(aleatoire_tournee))
# tounee_Ville_VNS = tourneeVille(path_file,T_VNS)
# print(T_VNS)
# print(tounee_Ville_VNS)
# path_file = "C:/Users/merye/Desktop/INPT/INE3/S5/P1/Gestion des opérartions de transport/Projet_TMS/Villes.csv"
# # # tournee = clarkeAndWright(path_file)
# # df = pd.read_csv(path_file)
# # nn_tsp(df)
# best_solution = branchAndBound(path_file)
# print("Best solution:", best_solution)

# matrix = matriceDistance(path_file)
# df = matrix[0]
# print(df)
#nn_tsp(df)

