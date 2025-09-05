#-------------------- Problema 1 --------------------

'''
A função find_nb recebe dois parâmetros: "data", que é uma lista de pontos no R^2 gerados de modo que a coordenada X esteja delimitada
entre 2 e 6 e a coordenada Y esteja delimitada entre 4 e 5, e "point", que é um ponto no R^2.

A função find_nb tem o objetivo de encontrar qual o ponto do array "data" está mais próximo do ponto "point". Para isso, a primeira coisa feita
é criar o array Dt, que ele é feito subtraindo point de data. Isso significa que a i-ésima posição de Dt equivale as coordenadas do i-ésimo ponto
de data subtraidas das coordenadas de point, respectivamente.
Portanto, matemáticamente isso representa os componentes X e Y do vetor Point -> data[i].

Após isso, é definido o array d que é um array que guarda a norma de todos os vetores representados em Dt, seguido de idt, que é o índice que
possua o argumento mínimo do vetor d, ou seja, o vetor com menor norma, que também é o índice do ponto mais próximo de point. Por fim, a função
retorna d[idx] e idx: a menor distância de um ponto de data até point e o índice desse ponto com a menor distância.

Note que sendo N o número de pontos, todas as operações realizadas para um ponto específico são de tempo constante,
o código acaba por ser O(N), pois a única variação de complexidade é a proporção linear em relação a quantidade de pontos.
'''

#-------------------- Problema 2 --------------------

#Versão recursiva da função dfs. Segue abaixo o trecho do código correspondente
#Foi alterado apenas das linhas 24 até 53

import random
def generate_maze(m, n, room = 0, wall = 1, cheese = '.' ):
	# Initialize a (2m + 1) x (2n + 1) matrix with all walls (1)
	maze = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)]

	# Directions: (row_offset, col_offset) for N, S, W, E
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

	# ----- INÍCIO DO CÓDIGO NOVO -----
	def dfs(x, y): #Dfs iterativa. Para gerar o MESMO RESULTADO, temos que iterar todo processamento em pilha
		dfStack = [[0,[x,y]]] #Cada elemento da pilha é uma dupla de valores
		#Uma operação pode ser do tipo 0 => visitar (equivalente a chamar dfs(x,y);
  		#ou tipo 1 => abrir (operação que abre um caminho da sala correspondente ao [x,y] na direção [dx,dy])
		
		while len(dfStack) > 0:
			type,data = dfStack.pop()
			if type == 0: #Operação de visitar
				x,y = data
		
				#Marca a célula como caminho livre e não parede
				maze[2 * x + 1][2 * y + 1] = room

				#Embaralha os caminhos para gerar um caminho aleatório
				random.shuffle(directions)

				#Adiciona na pilha as outras iterações
				for dx, dy in reversed(directions): #reversed pois uma pilha guarda na ordem inversa do 'for' original
					dfStack.append([1,[x,y,dx,dy]]) #Agenda na pilha essa operação

			else: #Operação de abrir
				x, y, dx, dy = data
				nx, ny = x + dx, y + dy #Novas coordenadas da célula seguinte
				if 0 <= nx < m and 0 <= ny < n and maze[2 * nx + 1][2 * ny + 1] == wall:
					#Abre um caminho de uma sala na direção [dx,dy]
					maze[2*x + 1 + dx][2*y + 1 + dy] = room
					#Coloca a operação de visitar a nova sala na pilha
					dfStack.append([0,[nx,ny]])
	# ----- FIM DO CÓDIGO NOVO -----

	# Start DFS from the top-left corner (0, 0) of the logical grid
	dfs(0, 0)
	count = 0
	while True: # placing the chesse
		i = int(random.uniform(0, 2 * m))
		j = int(random.uniform(0, 2 * m))
		count += 1
		if maze[i][j] == room:
			maze[i][j] = cheese 
			break
	return maze

def print_maze(maze):
	for row in maze:
		print(" ".join(map(str, row)))

#-------------------- Problema 3 --------------------

#Dado um labirinto gerado pelo problema 2, faça uma dfs que encontre o queijo partindo da posição (1,1)!
def encontre_o_queijo(maze, room = 0, wall = 1, cheese = '.'):
	'''
 	O código é no geral uma DFS simples. A escolha da DFS foi feita pois ela é capaz de encontrar o caminho completo de forma recursiva de uma maneira muito simples e eficaz. Como os labirintos gerados tem a característica de serem algo como "árvores" de certo modo, a DFS não é ineficiente e nem sofre problemas com ciclos.
	'''
	m = (len(maze)-1)//2
	n = (len(maze[0])-1)//2
	vis = [[wall] * (2 * n + 1) for _ in range(2 * m + 1)] #Cria uma matriz do tamanho do labirinto para acessar os vértices visitados em tempo constante
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #Direções possíveis
	def dfs(x,y):
		vis[x][y] = room #Marca como visitado
		if maze[x][y] == cheese:
			vis[x][y] = cheese
			return True
		for dx,dy in directions: #Para cada direção, vê se é possível seguir por ela
			if 0 <= x+dx < 2*m+1 and 0 <= y+dy < 2*n+1: #Se a posição for válida
				if maze[x+dx][y+dy] != wall and vis[x+dx][y+dy] == wall: #E não for uma parede e nem foi visitada
					res = dfs(x+dx,y+dy) #Tenta ir por esse caminho
					if res == True: #Se encontrou o queijo, vai retornando e marcando o caminho como definitivo
						return True
		vis[x][y] = wall #Se chegou aqui, em todas as direções livres o queijo não está, então não visita aqui e retorna Falso
		return False
	dfs(1,1) #Procura partindo de 1,1, o resultado será marcado em vis
	return vis

#-------------------- Problema 4 --------------------

#Fatos assumidos:
#- O grafo é direcionado, visto que as palavras usadas no enunciado inferem isso: "de x para y" significa uma aresta que só pode ir de x até y, mas "entre x e y" infere que pode ir de x até y e de y até x. Dada a escolha de palavras, assumirei que o grafo é direcionado.
#- A lista de adjacência pode ser implementada de qualquer maneira válida, desde que seja correta, não sendo o critério para avaliar isso a eficiência: Implementando um grafo com dicionário e conjuntos para fazer as listas de adjacência torna a operação de remoção mais custosa do que por exemplo em listas encadeadas, então apesar de talvez não ter a melhor complexidade possível, dado que o exercício não pede nada sobre complexidade, assumirei que ela não é tão relevante no objetivo desse problema. Meu objetivo foi fazer algo suficientemente simples para implementar.
#- Os vértices do grafo são identificados por um 'id' e um valor, apenas para simplificação. Poderia ser também um nome ou algo similar.
 
class Vertex:
	def __init__(self, id, val): #Inicializa um vertice com id e valor
		self.id = id
		self.value = val

class Graph:
	def __init__(self): #Incicializa um grafo vazio
		self.vert = {} #Dicionário de vértices existentes: chave = id, valor = instância de vertex correspondente
		self.adj = {} #Dicionário com as adjacências: chave = id, valor = conjunto com os vértices que existe uma aresta até lá.
  
	def adjacent(self, x, y): #Verificar se existe a aresta x -> y, onde x e y são ids
		if x not in self.vert or y not in self.vert: #Algum dos ids de vértices não existe
			return False
		if y not in self.adj[x]: #y existe mas não existe a aresta x -> y
			return False
		return True

	def neighbors(self, x): #Retorna a lista de vizinhos tal que exista x -> y, onde x é um id
		return list(self.adj[x])

	def add_vertex(self, x): #Adiciona o vértice x nos vértices. Assume que x = Vertex()
		if x in self.vert:
			return False
		self.vert[x.id] = x
		self.adj[x.id] = set([])
		return True

	def remove_vertex(self, x): #Remove o vértice de id x dos vértices e também todas as arestas que ele existe
		if x not in self.vert:
			return False
		self.adj[x] = set([]) #Apaga as arestas da forma x -> y
		for viz in self.adj.values(): #Itera sobre os conjuntos de vizinhos
			if x in viz: #Remove x caso ele esteja nos vizinhos daqui
				viz.remove(x)
		return True

	def add_edge(self, x, y): #Adiciona uma aresta x -> y se ela não existe
		if y in self.adj[x]:
			return False
		self.adj[x].add(y)
		return True

	def remove_edge(self, x, y): #Remove uma aresta x -> y se ela existe
		if y not in self.adj[x]:
			return False
		self.adj[x].remove(y)
		return True

	def get_vertex_value(self, x): #Obtem o valor do vértice de id x, ou None caso ele não existe
		if x not in self.vert:
			return None
		return self.vert[x].value

	def set_vertex_value(self, x, v): #Insere o valor v no vértice de id x caso ele exista
		if x in self.vert:
			self.vert[x].value = v
			return True
		return False

if __name__ == "__main__":
	print("Testes de execução: Problemas 2 e 3")
	print("No labirinto:")
	maze = generate_maze(10,10,' ','O','X')
	print_maze(maze)
	print("\nPodemos encontrar o queijo seguindo o caminho:")
	path = encontre_o_queijo(maze,' ','O','X')
	print_maze(path)

	print("\nTestes de execução: Problema 4")
	grafo = Graph()
	grafo.add_vertex(Vertex(2,4))
	grafo.add_vertex(Vertex(4,10))
	grafo.add_vertex(Vertex(6,16))
	grafo.add_edge(2,4)
	grafo.add_edge(2,6)
	grafo.add_edge(4,6)
	grafo.add_edge(4,2)
	print(f'vizinhos de 2: {grafo.neighbors(2)}')
	print(f'existe 2 -> 4? {grafo.adjacent(2,4)}')
	print(f'vizinhos de 4: {grafo.neighbors(4)}')
	if grafo.remove_edge(4,2):
		print('removi 4 -> 2')
	print(f'vizinhos de 4: {grafo.neighbors(4)}')
	print(f'vizinhos de 6: {grafo.neighbors(6)}')
	if grafo.remove_vertex(4):
		print('removi vertice 4')
	print(f'vizinhos de 2: {grafo.neighbors(2)}')
	print(f'valor do vertice de id 2 = {grafo.get_vertex_value(2)}')
	if grafo.set_vertex_value(2,600):
		print('mudei o valor de 2 pra 600')
	print(f'valor do vertice de id 2 = {grafo.get_vertex_value(2)}')