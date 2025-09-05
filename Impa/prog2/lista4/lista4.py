import scipy as SCI
import numpy as NP
import random as RAND

# --------------------------------- Problema 1 ---------------------------------

class TreeNode: #Classe de um nó da árvore
	def __init__(self, val=0, l=None, r=None): #Modifiquei para incluir left e right na inicialização
		self.val = val
		self.left = l #Fazendo isso, facilita a criação de uma árvore
		self.right = r

'''
	isBalanced: retorna um inteiro. -1 Se em algum momento, a diferença entre duas sub-árvores de um nó for maior que 1 e retorna a profundidade da sub-árvore caso ela for balanceada.
 
	A função funciona de forma recursiva:
	- Resolve o problema para a sub-árvore da esquerda;
	- Resolve o problema para a sub-árvore da direita;
	- Se em alguma foi retornado -1, também retorna -1, pois não é balanceada.
	- Caso contrário, compara a profundidade das duas sub-árvores e retorna -1 se diferirem por mais de 1 ou retorna o máximo entre as duas + 1 caso contrário.
'''
def isBalanced(root, curr):
	if curr == None:
		return 0

	p1 = isBalanced(root, curr.left) #Sub-árvore esquerda
	p2 = isBalanced(root, curr.right) #Sub-árvore direita
 
	if p1 == -1 or p2 == -1: #Se na execução delas achou uma diferença > 1, então só retorna o -1
		return -1

	if abs(p1 - p2) > 1: #Se agora deu uma diferença > 1, retorna -1
		return -1
	return max(p1,p2)+1 #Não deu problema! Retorna o tamanho da maior + 1

# --------------------------------- Problema 2 ---------------------------------
'''
O problema diz que o método pop() deve então retornar um elemento aleatório ao invés do último (outra interpretação poderia ser a existências de dois métodos 'pop'(), um aleatório e outro no final, mas essa interpretação seria mais complexa e não parece ser o objetivo do problema, dado que o nome da função aleatória teria que ser algo diferente do pop, visto que o python não permite dois métodos de mesmo nome e ainda ambos sem argumentos para diferenciar).

Isso mostra que como em nenhum momento será necessário coferir a ordem da pilha para retorno dos elementos, podemos fazer um algoritmo que despreze a ordem relativa dos elementos, dado que sempre será pego um aleatório no fim. 
'''
class randomStack: #Primeiro, os métodos padrão:
	def __init__(self):
		self._data = []
  
	def is_empty(self):
		return (len(self._data) == 0)

	def size(self):
		return len(self._data)
	
	def pop(self):
		if self.is_empty():
			return None

		ind = RAND.randint(0,len(self._data)-1) #Escolhe um indice aleatório
		last = self.size()-1 #Último elemento
  
		valInd = self._data[ind] #Armazena os valores nessas posições
		valLast = self._data[last] #Nessas variáveis
  
		self._data[ind] = valLast #Troca os valores de lugar: agora para remover o "aleatório" basta remover o final
		self._data[last] = valInd #Coloca o antigo último na antiga posição do aleatório
	
		return self._data.pop() #Remove e retorna o final, que agora é o aleatório
		
	def push(self, val):
		self._data.append(val)

# --------------------------------- Problema 3 ---------------------------------

'''
1) Eu utilizaria uma classe TreeNode que possui 2 informações principais: o valor do nó e uma lista de ponteiros que guardaria os nós-filhos desse nó. A lista de ponteiros será uma lista padrão do python, contínua (sem posições vazias no início/meio dela).

2) A remoção de filhos poderia funcionar de maneira similar a implementação de "remover um elemento aleatório" da pilha do exercício 2, mas ao invés de aleatório, teríamos que inserir uma propriedade que identifique qual dos nós será removido (Ex: Dar indices aos nós e fornecer um índice, ou fornecer um ponteiro para o nó). Para remover e manter a continuidade da lista, se quisermos remover o indice k e a lista tem n elementos, basta trocar os ponteiros indices k e n-1 de lugar e depois executar um pop() no final dessa lista de filhos. Caso seja necessário "apagar" ou processar de alguma forma o nó excluido e os seus filhos, percorreríamos a sub-árvore para fazer o que for necessário.

3) Dado que a lista de vizinhos de cada nó é contínua, faria uma função de busca em profundidade iniciando na raíz. A função processa primeiro a raiz, e depois de processar um nó, chama outra iteração da função para cada um de seus filhos, na ordem em que aparecem na lista, visto que temos uma ordem arbitrária já que não foi requisitado uma árvore de busca binária, e sim uma árvore qualquer. Isso tornaria nossa busca de profundidade do tipo Pré-Ordem, visto que a raiz é visitada antes dos filhos.

Abaixo segue um código exemplo de como seria implementado:
'''

class MultiTreeNode: #Classe de um nó da árvore de vários filhos
	def __init__(self, val=0, nextPointers=[]): #Inicialização
		self.val = val
		self.next = nextPointers

	def push(self, sonValue): #Insere um filho com valor sonValue
		self.next.append(MultiTreeNode(sonValue))
  
	def erase(self, sonValue): #Apaga um (poderia também ser todos, caso haja repetição. Bom, só um exemplo) filho que tenha esse valor caso exista
		for i,son in enumerate(self.next):
			if son.val == sonValue:
				self.next[i] = self.next[-1]
				self.next[-1] = sonValue
				return self.next.pop()
		return None
  
def MultiTreeWalk(node):
	print(f"*Processa nó com valor ${node.val}*")
	for son in node.next: #Quando não tiver filhos, é vazio, portanto não executará.
		MultiTreeWalk(son)

# --------------------------------- Problema 4 ---------------------------------

def getPoints(N, distX, distY):
	"""
	Sorteia N pontos no plano (x, y) de acordo com as distribuições escolhidas para x e y,
	assumindo valores entre (0 = 'uniforme', 1 = 'normal', 2 = 'student t').
 
	Retorna um array numpy com os N pontos gerados.
	"""
	def getCoordinates(dist, N): #Dado um N e a distribuição, essa função retorna N números nessa distribuição
		if dist == 0:
			return SCI.stats.uniform.rvs(-1, 2, size=N) # Pontos em [-1, (-1+2)] = [-1, 1]
		elif dist == 1:
			return SCI.stats.norm.rvs(loc=0, scale=0.5, size=N)  # μ = 0, σ = 0.5
		else:
			return SCI.stats.t.rvs(df=1, loc=0, scale=0.5, size=N)  # Student t para μ = 0, σ = 0.5.

	# Gerar as coordenadas de acordo com as distribuições escolhidas
	xArray = getCoordinates(distX, N)
	yArray = getCoordinates(distY, N)

	# Retorna os pontos como um array numpy de duplas de coordenadas
	return NP.column_stack((xArray, yArray))

# --------------------------------- Problema 5 ---------------------------------

def convexHull(points):
	if len(points) < 3:
		raise ValueError("Deve-se ter ao menos 3 pontos para formar um fecho convexo!")
	hull = SCI.spatial.ConvexHull(points) #Usa a função convex hull do scipy para fazer o convexhull
	res = points[hull.vertices] #Obtém a subsequência de vértices que formam o fecho convexo
	return res #Retorna ela

# --------------------------------- Testes ---------------------------------

if __name__ == "__main__":
    
	#Testes: Problema 1 -------------
	
	raiz1 = TreeNode(5,TreeNode(3,TreeNode(4),TreeNode(5,TreeNode(6))),TreeNode(0,TreeNode(1),TreeNode(2,TreeNode(7))))
	print(f"Árvore 1 é balanceada? {isBalanced(raiz1,raiz1) >= 0}")
	#Desenho:
	#				   5
	#				 /   \
	#			   3	   0
	#			 /  \	 / \
	#			4	5   1   2
	#				/	   /
	#			   6	   7
 
	raiz2 = TreeNode(5,TreeNode(3,TreeNode(4),TreeNode(5,TreeNode(6,TreeNode(99)))),TreeNode(0,TreeNode(1),TreeNode(2,TreeNode(7))))
	print(f"Árvore 2 é balanceada? {isBalanced(raiz2,raiz2) >= 0}\n")
	#Desenho:
	#				   5
	#				 /   \
	#			   3	   0
	#			 /  \	 / \
	#			4	5   1   2
	#				/	   /
	#			   6	   7
	#			  /
	#			 99
 
	#Testes: Problema 4 -------------

	nPoints = int(input("Insira um número de pontos: ")) #Assume-se que o usuário digite normalmente, visto que esse tipo de erro não é o foco da lista
	distTypeX = int(input("\nInsira um tipo de distribuição para o eixo X:\n0 -> Uniforme\n1 -> Normal\n2 -> Student T\nResposta: "))
	distTypeY = int(input("\nInsira um tipo de distribuição para o eixo Y:\n0 -> Uniforme\n1 -> Normal\n2 -> Student T\nResposta: "))
	res = getPoints(nPoints,distTypeX,distTypeY)
	print(f"\nPontos Sorteados:\n{res}")
 
	#Testes: Problema 5 -------------
	print(f"\nO fecho convexo dos pontos é constituído pelos pontos:\n{convexHull(res)}")