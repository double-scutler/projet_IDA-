import time
t1 = time.time()

class color:
    b = '\033[94m' # bleu
    y = '\033[93m' # jaune
    r = '\033[91m' # rouge
    n = '\033[0m' #normal
#la fonction afficherEtat permet de representer un état pour qu'il soit plus comprehensible visuellement.
#le param : tab en forme de [[X,X,X,X],[X,X,X,X],[X,X,X,X]] seul 3 case sont vides les autres remplis de 1 à 9 sans doublons, 0 est une case vide
#on ne peut avoir un numéro au dessus d'une case vide.
def afficherEtat(tab):
    for i in range(3):
        for k in range(4):
            if tab[i][k] == 0:
                print(" ", end="   |   ")
            else:
                if tab[i][k] <= 3:
                    print(color.r+str(tab[i][k])+color.n, end="   |   ")
                elif tab[i][k] <= 6:
                    print(color.b + str(tab[i][k])+color.n, end="   |   ")
                else:
                    print(color.y + str(tab[i][k])+color.n, end="   |   ")
        print("\n")
def trouverDestinations(e, pi):
    premiere_ligne = e[0]
    liste = []
    for i in range(4):
        if premiere_ligne[i] == 0 and pi != i+1:
            liste.append(i+1)
    return liste

def sommet(e, p):
    c = 0
    for i in range(3):
        if e[i][p-1]==0:
            c+=1
        else:
            return c
    return 0

def deplacer(e, p1, p2):
    e1 = list(e)
    e1[sommet(e1, p1)][p1-1], e1[sommet(e1, p2)-1][p2-1] = 0, e1[sommet(e1, p1)][p1-1]
    return e1
def egal(e, but):
    return e==but

def operations_possibles(e):
    operation = []
    for i in range(4):
        operation.append(trouverDestinations(e, i+1))
    return operation

def opPos(e2):
    operation = operations_possibles(e2)
    etatsFils = []
    nombre = 0
    e1=[[0,0,0,0], [0,0,0,0],[0,0,0,0]]
    for k in range(4):
        for l in operation[k]:
            e1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            for i in range(3):
                for j in range(4):
                    e1[i][j] = e2[i][j]
            #print(k+1, l)
            #afficherEtat(deplacer(e, k+1, l))
            etatsFils.append(deplacer(e1, k+1, l))
            #afficherEtat(etatsFils[nombre])
            #print("----------------------------------")
            #print("\n")

            nombre += 1
    return(operation, etatsFils, nombre)

#afficherEtat([[0,0,4,7], [2,0,5,8],[3,1,6,9]])
#print(trouverDestinations([[0,0,4,7], [2,0,5,8],[3,1,6,9]], 3))
#print(sommet(e, 1))
#afficherEtat(deplacer(e, 1, 2))
#print(egal(e,e))
#print(opPos(e))
#print(operations_possibles(e))

def poids(element):
    if element==0:
        return 0
    elif element<=3:
        return 1
    elif element <=6:
        return 2
    else:
        return 3


def heuristique1(e,But):
    c=0
    for i in range(3):
        for j in range(4):
            if e[i][j]!=0:
                c+=(e[i][j]!=But[i][j])*poids(e[i][j])
    return c


def profondeur(e,x):
    for i in range(3):
        for j in range(4):
            if e[i][j]==x:
                return i


def heuristique2(e,But):
    c=0
    for i in range(3):
        for j in range(4):
            if But[i][j]!=e[i][j] and (e[i][j]!=0):
                c+=profondeur(e,e[i][j])+poids(e[i][j])
    return c


node_dev=[]
liste_node_dev=[]
node_created =[]
liste_node_created=[]
def search(path,g,bound,But):
    global node_created
    global node_dev
    node = path[-1]
    f = g + heuristique3(node,But)
    if f > bound:
        return f
    if egal( node , But) :
        return 'FOUND'
    min = float("inf")
    node_dev.append(node)
    node_created += opPos(path[-1])[1]
    for succ in opPos(path[-1])[1]:
        if not (succ in path) :
            path.append(succ)
            t = search(path,g+cost(node, succ),bound,But)
            if t == 'FOUND' :
                #[(nombre de noeud dev, nombre de noeud cree), (nombre de noeud dev, )
                return 'FOUND'
            if t < min :
                min = t
            path.pop()
    return min

def IDA_star(e,But):
    bound = heuristique3(e,But)   #heuristique h
    path = [e]    #enattente()
    global liste_node_created
    global node_dev
    global liste_node_dev
    global node_created
    liste_node_dev = []
    count_iter_ida = 1
    while(True):
        t = search(path,0,bound,But)
        if t == 'FOUND':
            liste_node_created.append(node_created)
            liste_node_dev.append(node_dev)
            return(path,bound, count_iter_ida)
        if t == float("inf") :
            return 'not FOUND'
        liste_node_created.append(node_created)
        liste_node_dev.append(node_dev)
        node_dev = []
        node_created = []
        count_iter_ida += 1
        bound = t

def poids_cube_A_Degager(e,i,j) :
    if i == 0 :
        return 0
    elif i==1:
        if e[0][j]==0:
            return 0
        else:
            return poids(e[i][j])
    else:
        if e[0][j]==e[1][j]==0:
            return 0
        elif e[1][j]!=0 and e[0][j]==0:
            return poids(e[i][j])
        else:
            return poids(e[i][j])+poids(e[i-1][j])

def position(e,n):
    for i in range(3):
        for j in range(4):
            if e[i][j]==n:
                return i,j


def heuristique3(e,But):
    c = 0
    for i in range(3):
        for j in range(4):
            if e[i][j] != 0 and e[i][j] != But[i][j]:
                c += poids_cube_A_Degager(e, i, j)+poids_cube_A_Degager(e, position(But, e[i][j])[0], position(But, e[i][j])[1])+poids(e[i][j])
    return c

def plan_solution(resultat):
    total_noeud_dev = 0
    total_noeud_cree = 0
    for i in range(len(resultat[0])):
        afficherEtat(resultat[0][i])
        print("-----------------------------")
    print(len(resultat[0]))
    for i in range(len(liste_node_dev)):
        total_noeud_dev+=len(liste_node_dev[i])
        total_noeud_cree+=len(liste_node_created[i])
        print("le nombre de noeuds developpées à l'itération : ", i+1 ,"est : " ,len(liste_node_dev[i]))
        print("le nombre de noeuds crées à l'itération : ", i + 1, "est : ", len(liste_node_created[i]))
        print("\n")
    print("TOTAL NOEUD DEVELOPPEES : ", total_noeud_dev)
    print("TOTAL NOEUD CREES : ", total_noeud_cree)

def moved(node, succ):
    for i in range(3):
        for j in range(4):
            if node[i][j]!=succ[i][j] and node[i][j]!=0:
                return node[i][j]

def cost(node, succ):
    if moved(node,succ)<=3:
        return 1
    elif moved(node, succ)<=6:
        return 2
    else:
        return 3


e1 = [[0,0,4,7],[2,0,5,8],[3,1,6,9]]

but1 = [[1,0,4,7],[2,0,5,8],[3,0,6,9]]

but2 = [[1,9,4,0],[2,8,5,0],[3,7,6,0]]

but3 = [[7,8,1,0],[2,4,5,0],[3,6,9,0]]

but4 = [[2,5,8,0],[1,4,7,0],[3,6,9,0]]

but5 = [[8,0,5,0],[2,4,7,0],[3,6,9,1]]


e2 = [[1, 4, 7, 0], [2, 5, 8, 0], [3, 6, 9, 0]]
but6 = [[1, 2, 3, 0], [4, 5, 6, 0], [7, 8, 9, 0]]



etat = int(input("Entrez 1 ou 2 pour choisir l'état initial : "))
but = int(input("Entrez 1,2,3,4,5 ou 6 pour choisir l'état but : "))

if etat == 1:
    etat = e1

if etat == 2:
    etat = e2

if but==1:
    but = but1
elif but==2:
    but = but2
elif but == 3:
    but = but3
elif but==4:
    but = but4
elif but==5:
    but = but5
else:
    but = but6
t1 = time.time()

plan_solution(resultat=IDA_star(etat, but))
t2 = time.time()
print(t2-t1)

