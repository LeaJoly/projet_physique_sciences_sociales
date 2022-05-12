# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:18:50 2022

@author: ljoly
"""
import numpy as np
import matplotlib.pyplot as plt
import random as rd



N = 100 # nombre d'agents économiques
x = 0.1 # pourcentage de la fortune de l'agent le plus pauvre transféré dans chaque transaction
W = 100000 # richesse totale de l'économie = 100000€

# Répartition aléatoire de la richesse dans l'économie au début de la simulation
v = np.random.rand(N)
normalized_v = v / sum(v)
w = W*normalized_v
w2 = W*normalized_v
w3 = W*normalized_v
w4 = W*normalized_v            # on prend la même distribution de départ pour tous les modèles

X = [m for m in range(1,N+1)]
plt.plot(X,w,'.')
plt.ylabel('richesse')
plt.xlabel('agent n°')
plt.show()                  # on affiche la répartition initiale de la richesse

### Premier modèle naïf sans biais ni redistribution

def echange():
    indices = rd.sample(range(N),2)  # on choisit aléatoirement 2 agents pour un échange
    i,j = indices[0],indices[1]
    m = x*min(w[i],w[j])          # richesse mise en jeu pour cet échange
    if np.random.randint(2):      # tirage au sort pour savoir qui gagne la transaction
        w[i] += m                 # l'agent i remporte l'échange
        w[j] -= m
    else:
        w[j] += m                 # l'agent j remporte l'échange
        w[i] -= m
    return w


def model1():
    for l in range(10):
        for k in range(100000):
            echange()
        plt.plot(X,w,'.')
        plt.ylabel('richesse')
        plt.xlabel('agent n°')
        plt.show()
    
### Second modèle avec biais

def bernoulli(p):
    if rd.random()<=p :
        return 1
    else : 
        return 0
    
def echange2():
    indices = rd.sample(range(N),2)      # on choisit aléatoirement 2 agents différents pour un échange
    i,j = indices[0],indices[1]
    m = x*min(w2[i],w2[j])               # richesse mise en jeu pour cet échange
    d = max(w2[i],w2[j]) - min(w2[i],w2[j])   # on prend la différence de richesse entre les ndvidus pour construire le biais
    p = 0.5 + d/(2*W)                    # d/W < 0.5  on a un paramètre biaisé proportionnellement au différentiel de richesse entre les 2 agents
    if max(w2[i],w2[j])==w2[i]:          # l'agent i est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w2[i] += m                   # l'agent i remporte l'échange
            w2[j] -= m
        else:
            w2[j] += m                   # l'agent j remporte l'échange
            w2[i] -= m
    else:                                # l'agent j est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w2[j] += m                   # l'agent j remporte l'échange
            w2[i] -= m
        else:
            w2[i] += m                   # l'agent i remporte l'échange
            w2[j] -= m


def model2():
    plt.plot(X,w2,'.')
    plt.ylabel('richesse')
    plt.xlabel('agent n°')
    plt.show()
    for l in range(5):
        for k in range(100000):
            echange2()
        plt.plot(X,w2,'.')
        plt.ylabel('richesse')
        plt.xlabel('agent n°')
        plt.show()
        
### Troisième modèle avec un impôt non progressif

t = 0.1 # part prélevée en pourcentage de la richesse de chaque agent pour l'impôt


def echange3():
    indices = rd.sample(range(N),2)      # on choisit aléatoirement 2 agents différents pour un échange
    i,j = indices[0],indices[1]
    m = x*min(w3[i],w3[j])               # richesse mise en jeu pour cet échange
    d = max(w3[i],w3[j]) - min(w3[i],w3[j])   # on prend la différence de richesse entre les indvidus pour construire le biais
    p = 0.5 + d/(2*W)                    # d/W < 0.5  on a un paramètre biaisé proportionnellement au différentiel de richesse entre les 2 agents
    S = t*W                              # somme totale rapportée par l'impôt
    if max(w3[i],w3[j]) == w3[i]:        # l'agent i est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w3[i] += m                   # l'agent i remporte l'échange
            w3[j] -= m
        else:
            w3[j] += m                   # l'agent j remporte l'échange
            w3[i] -= m
    else:                                # l'agent j est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w3[j] += m                   # l'agent j remporte l'échange
            w3[i] -= m
        else:
            w3[i] += m                   # l'agent i remporte l'échange
            w3[j] -= m
    for l in range(len(w3)):
        w3[l] = (1-t)*w3[l] + S/N        # l'impôt n'est pas progressif et est redistribué de manière égalitaire à tous les agents



def model3():
    plt.plot(X,w3,'.')
    plt.ylabel('richesse')
    plt.xlabel('agent n°')
    plt.show()
    for l in range(10):
        for k in range(10):
            echange3()
        plt.plot(X,w3,'.')
        plt.ylabel('richesse')
        plt.xlabel('agent n°')
        plt.show()
        
### Quatrième modèle avec impôt progessif

def impot(x):           # prend en argument une liste conteanant la richesse de chaque agent
    S = 0               # montant total d'impôt prélevé
    for k in range(len(x)):
        if (10000 <= x[k] < 20000) :
            S += 0.1*x[k]
            x[k] *= 0.9             # impôt sur la fortune de 10 %
        elif  20000 <= x[k] < 50000 :
            S += 0.2*x[k]
            x[k] *= 0.8             # impôt sur la fortune de 20 %
        elif x[k] >= 50000 :
            S += 0.3*x[k]
            x[k] *= 0.7             # impôt sur la fortune de 30 %
    for l in range(len(x)):
        x[l] += S/N                 # redistribution égalitaire

def echange4():
    indices = rd.sample(range(N),2)      # on choisit aléatoirement 2 agents différents pour un échange
    i,j = indices[0],indices[1]
    m = x*min(w4[i],w4[j])               # richesse mise en jeu pour cet échange
    d = max(w4[i],w4[j]) - min(w4[i],w4[j])   # on prend la différence de richesse entre les indvidus pour construire le biais
    p = 0.5 + d/(2*W)                    # d/W < 0.5  on a un paramètre biaisé proportionnellement au différentiel de richesse entre les 2 agents
    if max(w4[i],w4[j]) == w4[i]:        # l'agent i est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w4[i] += m                   # l'agent i remporte l'échange
            w4[j] -= m
        else:
            w4[j] += m                   # l'agent j remporte l'échange
            w4[i] -= m
    else:                                # l'agent j est le plus riche 
        if bernoulli(p):                 # tirage au sort biaisé pour savoir qui gagne la transaction
            w4[j] += m                   # l'agent j remporte l'échange
            w4[i] -= m
        else:
            w4[i] += m                   # l'agent i remporte l'échange
            w4[j] -= m
    impot(w4)



def model4():
    plt.plot(X,w4,'.')
    plt.ylabel('richesse')
    plt.xlabel('agent n°')
    plt.show()
    for l in range(10):
        for k in range(5000):
            echange4()
        plt.plot(X,w4,'.')
        plt.ylabel('richesse')
        plt.xlabel('agent n°')
        plt.show()