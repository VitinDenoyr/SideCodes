import scipy as SCI
import numpy as NP
import heapq as PriorityQueue
import time

# Interpolador igual do exercício original
class Interpolater:
	def evaluate(self, X):
		raise NotImplementedError

	def __call__(self, X):
		return self.evaluate(X)
		
# Classe da matriz de Vandermonte igual o exercício original
class VandermondeMatrix(Interpolater):
	def __init__(self, x, y):
		if len(x) != len(y):
			raise RuntimeError(f"Dimensions must be equal len(x) = {len(x)} != len(y) = {len(y)}")
		self.data = [x, y]
		self._degree = len(x) -1
		self._buildMatrix()
		self._poly = NP.linalg.solve(self.matrix, self.data[1])

	def _buildMatrix(self):
		self.matrix = NP.ones([self._degree+1, self._degree+1])
		for i, x in enumerate(self.data[0]):
			self.matrix[i, 1:] = NP.multiply.accumulate(NP.repeat(x, self._degree))
		
	def evaluate(self, X):
		r = 0.0
		for c in self._poly[::-1]:
			r = c+r*X
		return r

# ---------------------- Problema 1 ----------------------

def find_judge(n, trust): #trust: n x n
	trustsHowMany = {} #Quantas pessoas a pessoa i confia
	isTrustedBy = {} #Quantas pessoas confiam na pessoa i
	for tr in trust: #Nessa relação:
		# Inicializa contagens
		if tr[0] not in trustsHowMany:
			trustsHowMany[tr[0]] = 0
		if tr[1] not in isTrustedBy:
			isTrustedBy[tr[1]] = 0

		trustsHowMany[tr[0]] += 1 #ai confia em um a mais
		isTrustedBy[tr[1]] += 1 #bi confia em um a mais

	id = -1
	for i in range(1,n+1):
		if trustsHowMany.get(i,0) == 0 and isTrustedBy.get(i,0) == n-1:
			id = i
			break
			#Podemos garantir que não pode haver outro possível juiz, visto que tal juiz deveria ser confiável por essa pessoa, e essa pessoa não confia em ninguém
	return id

if __name__ == "__main__":
	print("Testes: Problema 1")
	n1, t1 = 6,[[1,2],[1,3],[2,3],[4,3],[6,3],[5,3]]
	n2, t2 = 7,[[1,2],[1,3],[2,3],[4,3],[6,3],[5,3],[7,2]]
	n3, t3 = 3,[[1,2]]
	print(f"Teste 1: ({n1},{t1}) -> {find_judge(n1,t1)}")
	print(f"Teste 2: ({n2},{t2}) -> {find_judge(n2,t2)}")
	print(f"Teste 3: ({n3},{t3}) -> {find_judge(n3,t3)}\n")
 
# ---------------------- Problema 2 ----------------------

def MinimumSpanningTree(n, edges): #N vértices, e edges é uma lista onde edges[i] -> lista de duplas da forma [vizinho de i, custo para cruzar essa aresta]. Como não foi especificado a entrada, mas está implícito que essa informação das arestas deve existir, assumirei arbitráriamente uma forma de obter ela, na entrada
#Será o usado o algoritmo de prim, apenas pois já fiz esse problema antes em c++ e na hora que fiz ele o algoritmo que eu tinha deduzido para o problema descobri que se chama algoritmo de Prim, então que seja este
	pq = [] #Fila de prioridade
	PriorityQueue.heappush(pq, (0, 1, 1))
	vis = [False] * (n + 1) #Array de visitados
	r = 0  # Custo total da MST
	qtVis = 0  # Quantidade de vértices visitados
	mst = [] #Lista de arestas da MST
		
	while pq:
		cost, prev, u = PriorityQueue.heappop(pq)
		if vis[u]: #Só vai nos não visitados
			continue
		# Marca o vértice como visitado, ele é a melhor opção
		vis[u] = True
		r += cost  # Soma o custo da aresta
		qtVis += 1 # Marca um na quantidade de visitados
		if prev != u: # Exclui a aresta inicial que não é uma aresta de fato 
			mst.append([u,prev,cost])
  
		if qtVis == n: # Se já visitou todos, retorna
			return mst
		# Adiciona os vizinhos não visitados à fila de prioridade
		for v, w in edges[u]:
			if not vis[v]:
				PriorityQueue.heappush(pq, (w, u, v)) #Adiciona (u,v) com custo w
		
	# Verifica se todos os vértices foram visitados (ou seja, MST existe)
	if qtVis == n:
		return mst
	return None  # Caso não seja possível formar a MST

'''
Item B) Perceba que para garantir que o algoritmo obtenha realmente a arvore geradora MÍNIMA, precisamos escolher a todo momento arestas mínimas, e isso envolve ordenar N arestas, pois ao todo, precisamos das menores M-1 arestas que visitam vértice novo na árvore geradora mínima, onde M é o número de vértices e N o de arestas.

Sabemos que o problema de ordenação de tem complexidade mínima Ω(NlogN), portanto, podemos usar um argumento de redução para afirmar que o problema da Minimum Spanning Tree, como um de seus passos é ordenação de arestas, também tem complexidade mínima Ω(NlogN).


Item C) Perceba que o algoritmo usado, apesar de não ordenar todas as arestas uma única vez, faz K <= N operações de inserção da priority queue, onde K é o número de arestas encontradas até visitarmos os M vértices. Além disso, faz também M-1 operações de pop da priority queue.

Note que então ele faz uma quantidade de operações na ordem de N, visto que M-1 < N, e além disso, cada operação tem custo máximo possível log(N), pois está sendo usada uma priority queue. Além disso, as operações de append em lista são feitas em tempo constante, tal como a maioria das outras operações, o que novamente implica que o tempo não ultrapassará NlogN em complexidade. Assim, concluímos que o algoritmo obedece sim a cota ótima de NlogN.

'''

if __name__ == "__main__":
	print("Testes: Problema 2")
	mst = MinimumSpanningTree(5,[[],[[2,3],[5,7]],[[3,5],[4,2]],[[4,8]],[[5,4],[3,8],[2,2]],[[1,7],[4,4]]])
	totCost = 0
	for ed in mst:
		print(f"({ed[0]} <-> {ed[1]}) , cost: {ed[2]}")
		totCost += ed[2]
	print(f"Total cost: {totCost}")
	print()

# ---------------------- Problema 3 ----------------------

'''
Dada a entrada, é visível que devêmos usar uma interpolação, e será usada a interpolação polinomial, e será usada a matriz de vandermonte por escolha arbitrária, pois tenho que decidir uma interpolação que devo usar, e a matriz de vandermonte é uma escolha que possui inicialização rápida

Para obter altura 700, basta colocar a altura como parâmetro e calcular o evaluate
Para obter a temperatura 0, uma escolha seria fazer a altura ser parâmetro e obter uma raíz no intervalo, mas uma mais simples é interpolar com a temperatura como parâemtro e avaliar em 0 com evaluate, que é o que foi feito
'''
if __name__ == "__main__":
	print("Testes: Problema 3")
	temps = NP.array([15,9,5,3,-2,-5,-15])
	alts = NP.array([200,400,600,800,1000,1200,1400])
	r1 = VandermondeMatrix(temps,alts) #temperatura é parametro
	r2 = VandermondeMatrix(alts,temps) #altura é parametro
	print(f"Temperatura 0 -> {r1.evaluate(0):.2f}m") #X é temperatura, quero X = 0
	print(f"Altura 700 -> {r2.evaluate(700):.2f}°C") #X é altura, quero X = 700

# ---------------------- Problema 4 ----------------------

from root_finder import Interval, bissect, grid_search, RealFunction

def newton_root(f: RealFunction, guess_0: float = 0, erroTol: float = 1e-4, maxItr: int = 1e4, eps: float = 1e-6) -> Interval:
	#Faz o método de newton com limite de iterações e com chute inicial de valor
	count = 0
	x = guess_0
	fx = f(x)
	
	while count < maxItr and abs(fx) > erroTol:
		# Calcula a derivada no ponto atual
		f_prime_x = f.prime(x)
		
		# Atualiza o ponto x usando o método de Newton
		if f_prime_x == 0: #Evita divisão por 0
			f_prime_x += eps*2	
		x = x - fx / f_prime_x
		
		# Encerra e retorna None se x sair do domínio, pois não há comportamento padrão definido, mas indica que o método de newton não funciona com esse chute
		if x > f.domain.supp or x < f.domain.inff:
			return None
		
		# Calcula f no novo ponto do método de Newton
		fx = f(x)
		count += 1 # Conta mais uma iteração
		
	# Retorna um intervalo muito pequeno em torno do valor encontrado para ser compatível com o retorno do `bissect`
	return Interval(x, x)


if __name__ == "__main__":
	print("Testes: Problema 4")
 
	# Exemplo de uso de RealFunction:
	# Função f^2 -> capaz de calcular x^3 - 3x^2 - 49 para x em um intervalo dado
	class f2(RealFunction):
		def __init__(self, dom):
			self.f = lambda x : NP.power(x, 3) - 3*NP.power(x, 2) - 49
			self.prime = lambda x : 3*NP.power(x, 2) - 6*x #Derivada: 3x^2 - 6x
			self.domain = dom

	# Exemplo de uso das funções e comparação de resultados
	func = f2(Interval(-2**30,2**30)) #Intervalão, deve ter raíz
	sign = 1; dist = .25
	rootInterval = None
	while rootInterval == None:
		if sign: #Duplica a cada duas iterações
			dist *= 2
		if dist > func.domain.supp: #Passou do máximo de domínio da função, que como é simétrico, não tem como ter raíz mais
			break
		sign *= -1
		currInterval = Interval(min(dist*sign,0),max(dist*sign,0)) #Novo intervalo para procurar: não necessáriamente optimal, apenas um que seja justo
		rootInterval = grid_search(func, currInterval)
		#Se em algum momento encontrar intervalo com raíz, para
  
	if rootInterval != None:
		r1 = bissect(func, rootInterval) #Usa o método da bissecção para achar uma raíz nesse intervalo
		r2 = newton_root(func)
		print(f"Método da bissecção: a raíz está entre {r1}") #Não fiz error handling para None, mas é intuitivo que falhou ao ver um "None"
		print(f"Método de newton: a raíz está entre {r2}") #Também não fiz error handling para None, mas também é intuitivo que falhou ao ver um "None"
	else:
		print("Deu azar... sua função não tem raízes ou tem raízes gigantescas")
	print()

# ---------------------- Problema 5 ----------------------
# Classe do polinômio de lagrange usando o lagrange do scipy
class LagrangePolynomial(Interpolater):
	def __init__(self, x, y):
		if len(x) != len(y):
			raise RuntimeError(f"Dimensions must be equal len(x) = {len(x)} != len(y) = {len(y)}")
		self._poly = SCI.interpolate.lagrange(x,y)

	def evaluate(self, X):
		return NP.polyval(self._poly, X)

#Função de comparação de velocidades
def compareBuildSpeed(x,y):
	#Cria um polinômio de Lagrange com parâmetros x e y
	t0 = time.time()
	LagrangePolynomial(x,y)
	tLagrange = time.time() - t0
 
	#Cria a matriz vandermonte com parâmetros x e y
	t0 = time.time()
	VandermondeMatrix(x,y)
	tVandermont = time.time() - t0
	
	#Print de informações
	print(f"Size: {len(x)}.	  Vandermonte: {tVandermont:.3f}s  x  Lagrange: {tLagrange:.3f}s")
		
if __name__ == "__main__": #Testes
	print("Testes: Problema 5")
	arrSize = 1; prevSize = 1
	for i in range(11):
		arrSize, prevSize = arrSize+prevSize, arrSize
		xi = NP.random.choice(range(999),size=arrSize,replace=False)
		yi = NP.random.choice(range(999),size=arrSize,replace=False)
		compareBuildSpeed(xi,yi)
	#Resumo: lagrange é bizarramente mais lento
	print()