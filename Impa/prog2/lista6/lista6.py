from collections import deque
import math
# -------------------- Problema 1 --------------------
'''
	Implementação usando uma queue, simulada por uma deque de collections
 
	O paradigma entendido é que os vértices tem números inteiros positivos, e a posição 0 de adj guarda os valores dos vértices, usado no problema 2, por mais que não interfira nada nesse código.
'''
def bfs(adj: list[list[int]], start):
    #Lista de visitados, criação da fila e colocação do início nela:
	visited = [False]*len(adj)
	nexts = deque()
	verts = []
 
	visited[start] = True
	nexts.append(start)
	verts.append(start)
 
	while len(nexts) > 0: #A cada termo, visita e coloca os vizinhos não visitados na fila para iterar
		v = nexts.popleft()
  
		for u in adj[v]:
			if not visited[u]:
				visited[u] = True
				nexts.append(u)
				verts.append(u)

	return verts

# -------------------- Problema 2 --------------------
'''
Assume-se que as propriedades obedeçam: valor de v -> adj[0][v]

Não importei a classe grafo usada da lista anterior pois não foi necessáriamente um requisito, mas seria também uma forma de lidar com as "propriedades"

Para retornar um nó, apenas retornarei o id dele. Se não existir, retorno None
'''

def busca_propriedade(adj: list[list[int]], prop):
	visited = [False]*len(adj)
	nexts = deque()
	verts = []
 
	visited[1] = True
	if adj[0][1] == prop:
		return 1
	nexts.append(1)
	verts.append(1)
 
	while len(nexts) > 0: #A cada termo, visita e coloca os vizinhos não visitados na fila para iterar
		v = nexts.popleft()
  
		for u in adj[v]:
			if not visited[u]:
				visited[u] = True
				if adj[0][u] == prop:
					return u
				nexts.append(u)
				verts.append(u)
	return None

# -------------------- Problema 3 --------------------

'''
Problema análogo: https://cses.fi/problemset/task/1192/

Implementei basicamente uma dfs para encontrar a ilha de cada quadradinho "1" e iterei sobre a matriz toda, encontrando todas as ilhas.
'''

def dfs(i, j, mat, vis, n, m):
	vis[i][j] = True
	adj = [[i+1,j],[i,j-1],[i,j+1],[i-1,j],[i-1,j-1],[i-1,j+1],[i+1,j-1],[i+1,j+1]]
	for a,b in adj:
		if a < 0 or b < 0 or a >= n or b >= m:
			continue
		if not vis[a][b] and mat[a][b] == '1':
			dfs(a,b,mat,vis,n,m)

def get_islands_number(path = 'new_map.txt'):
	mat = []
	with open(path, 'rt') as f:
		mat = [list(line.strip()) for line in f]
	
	n = len(mat) #Linhas
	m = len(mat[0]) #Colunas
	vis = [[False] * m for _ in range(n)]
 
	qtIlhas = 0
	for i in range(n):
		for j in range(m):
			if not vis[i][j] and mat[i][j] == '1': #Acha qual ilha ela pertence
				qtIlhas += 1
				dfs(i, j, mat, vis, n, m)
	return qtIlhas

# -------------------- Problema 4 --------------------
'''
Apenas atualizarei a função dfs para calcular isso. O centróide pode ser definido como a média das coordenadas x e y, ainda, considerarei a coordenada do canto superior esquerdo como [0,0].

Será retornado uma lista com [quantidade de ilhas, [coordenda X do centroide da maior ilha, coordenada y ...], [coordenada X do centroide da menor ilha, coordenada y ...]]
'''

def dfs_2(i, j, mat, vis, n, m):
	vis[i][j] = True
	adj = [[i+1,j],[i,j-1],[i,j+1],[i-1,j],[i-1,j-1],[i-1,j+1],[i+1,j-1],[i+1,j+1]]
 
	qtVis = 1; sumX = i; sumY = j
	for a,b in adj:
		if a < 0 or b < 0 or a >= n or b >= m:
			continue
		if not vis[a][b] and mat[a][b] == '1':
			res = dfs_2(a,b,mat,vis,n,m) #Acumula coordenadas x,y e quantidade de tiles visitados
			qtVis += res[0]
			sumX += res[1]
			sumY += res[2]
	return [qtVis, sumX, sumY]
   
def get_islands_number_2(path = 'new_map.txt'):
	mat = []
	with open(path, 'rt') as f:
		mat = [list(line.strip()) for line in f]
	
	n = len(mat) #Linhas
	m = len(mat[0]) #Colunas
	vis = [[False] * m for _ in range(n)]
 
	qtIlhas = 0
	maxIlha = [0,0,0]
	minIlha = [n*m+1,0,0]
	for i in range(n):
		for j in range(m):
			if not vis[i][j] and mat[i][j] == '1': #Acha qual ilha ela pertence
				qtIlhas += 1
				ilha = dfs_2(i, j, mat, vis, n, m)
				if maxIlha[0] < ilha[0]: #Troca de maior ilha
					maxIlha[0] = ilha[0]
					maxIlha[1] = ilha[1]
					maxIlha[2] = ilha[2]
				if minIlha[0] > ilha[0]: #Troca de menor ilha
					minIlha[0] = ilha[0]
					minIlha[1] = ilha[1]
					minIlha[2] = ilha[2]
	centroidMax = [maxIlha[1]/maxIlha[0], maxIlha[2]/maxIlha[0]]
	centroidMin = [minIlha[1]/minIlha[0], minIlha[2]/minIlha[0]]
	#Se for exigido que o centroide seja um tile dessa ilha, basta aproximar usando round, se não fosse, basta ignorar a linha abaixo:
	centroidMax = [round(centroidMax[0]),round(centroidMax[1])]
	centroidMin = [round(centroidMin[0]),round(centroidMin[1])]
 
	return [qtIlhas,centroidMax,centroidMin]


# -------------------- Problema 5 --------------------
'''
Um lago é quase análogo a uma ilha, com a diferença de que não contam as diagonais, e água e terra trocam de papel, assim: perceba que a única forma de um conjunto de águas não ser um lago é se ela tocar a borda da matriz, pois aí ela não está completamente cercada por terra. Assim, basta verificar essa condição em particular, enquanto troca água e terra de papéis.
'''

def dfs_3(i, j, mat, vis, n, m):
	isLago = True #Vai virar falso se deixar de ser um lago
	vis[i][j] = True
	adj = [[i+1,j],[i,j-1],[i,j+1],[i-1,j]]
	for a,b in adj:
		if a < 0 or b < 0 or a >= n or b >= m:
			isLago = False #Não está cercada por terra, toca a borda
			continue
		if not vis[a][b] and mat[a][b] == '0':
			res = dfs_3(a,b,mat,vis,n,m)
			isLago = isLago and res
	return isLago

def has_lake(path = 'new_map.txt'):
	mat = []
	with open(path, 'rt') as f:
		mat = [list(line.strip()) for line in f]
	
	n = len(mat) #Linhas
	m = len(mat[0]) #Colunas
	vis = [[False] * m for _ in range(n)]

	for i in range(n):
		for j in range(m):
			if not vis[i][j] and mat[i][j] == '0': #Acha se isso pertece a um lago
				res = dfs_3(i, j, mat, vis, n, m)
				if res:
					return True
	return False
print(has_lake('ex_map.txt'))