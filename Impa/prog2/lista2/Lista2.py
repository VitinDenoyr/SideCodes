import numpy as NP, time as TIME

#------------------------------------------------------------------------------------------------------------------

#Problema 1 - My_Array
#	Escolha da estrutura: Dado que o enunciado diz: "Usando a classe numpy Array" ao invés de "Amplie a classe numpy array", como citado no problema 2, decidi apenas criar uma classe My_Array que usa o numpy array como um de seus componentes, e não como uma herança, como foi feito no problema 2.
#	Após executar vários testes, vê-se que a implementação do My_Array, apesar de funcionar bem como um array dinâmico, para N's grandes o suficiente, o append de N elementos fica geralmente entre 5 a 6 vezes mais lento que a lista do python. Isso nos leva a pensar que de fato a ordem de complexidade das duas listas é a mesma, tendo apenas constantes diferentes, que implicaria na razão consistente entre os tempos.
class My_Array:
	def __init__(self, elements=[], limit=1):
		self.array = NP.zeros(limit,dtype=object) #Cria um array zerado no tamanho inicial e seta o limite e tamanho atuais
		self.limit = limit
		self.size = 0
		for e in elements: #Adiciona os elementos no array já fazendo uso do método append
			self.append(e)
		
	def __len__(self): #Apenas converte o significado de len
		return self.size
		
	def __getitem__(self, index): #Obter valor dado um indice
		if index >= self.size or index < 0:
			raise IndexError("Indice fora do alcance")
		return self.array[index]
	
	def __repr__(self): #Representação em string no formato [x1, x2, ..., xn]
		st = f"["
		for i in self.array[:self.size-1]:
			st += f"{i}, "
		return st + f"{self.array[self.size-1]}]"

	def append(self, element): #Função append requisitada
		if self.size < self.limit: #Há espaço suficiente, logo não precisa realocar
			self.array[self.size] = element
			self.size += 1
		else: #Realoca o array com dobro do limite atual e coloca o elemento normalmente no fim
			self.limit *= 2
			newArray = NP.zeros(self.limit,dtype=object)
			for i in range(self.size):
				newArray[i] = self.array[i]
			self.array = newArray
			self.array[self.size] = element
			self.size += 1

def testTime(obj,qt): #Teste arbitário de appends
	t0 = TIME.time_ns()
	for i in range(qt):
		obj.append(i)
	tn = TIME.time_ns()
	return (tn - t0)/(1000000)

if __name__ == "__main__": #Execução dos testes
	MyArray = My_Array()
	pythonList = []
	testSets = [
		[100, 200, 350, 500, 750, 800, 1000, 1200, 1500, 2000], #Testes extremamente curtos: Mostra clara inconsistência de tempos
		[30000, 40000, 50000, 65000, 80000, 100000, 110000, 135000, 150000, 180000], #Testes curtos
		[240000, 320000, 400000, 480000, 550000, 650000, 750000, 875000, 950000, 1100000], #Testes médios
  		[1200000, 1500000, 1800000, 2000000, 2400000, 2700000, 3000000, 3600000, 4200000, 5000000], #Testes grandes
		[8000000, 10000000, 11000000, 12000000, 16000000, 18000000, 20000000, 25000000, 30000000, 50000000] #Testes gigantes
	]
	averageRatio = 0
	chosenTestSet = int(input(f"Digite o número do conjunto de testes:\n0 - Extremamente curtos\n1 - Curtos\n2 - Médios\n3 - Grandes\n4 - Gigantes\n")) #Para outro conjunto de testes, troque o índice para algum inteiro em [0, 9]
	if type(chosenTestSet) != type(1):
		chosenTestSet = 1
	chosenTestSet %= 5

	for i,tst in enumerate(testSets[chosenTestSet]):
		tM = testTime(My_Array(),tst)
		tP = testTime([],tst)
		print(f"Teste {i+1}: {tst} elementos.\n O tempo de execução da inserção foi de:")
		print(f"My_Array: {tM:.3f}ms                       Python List: {tP:.3f}ms")
		print(f"Então, My_Array levou {(max(tM,.01)/max(tP,.01)):.3f}x o tempo da Python List\n")
		averageRatio += (max(tM,.01)/max(tP,.01))
	print(f"Nos testes executados, o My_Array levou em média {averageRatio/len(testSets[chosenTestSet]):.3f}x o tempo da Python List")

#------------------------------------------------------------------------------------------------------------------

#Problema 2 - Ampliar classe do Array Numpy para ToroArray
class ToroArray(NP.ndarray):
	def __new__(cls, arr): #Converte o array Numpy para um ToroArray como mostrado no github
		obj = NP.asarray(arr).view(cls)
		return obj

	def __getitem__(self, index): #Converte o indice módulo tamanho do array e usa a função da classe pay para obter o valor
		return super().__getitem__(index%len(self))

#Testes Opcionais - Caso queira testar exemplos básicos
#tr = ToroArray([10, 11, 12, 13, 14])
#print(tr[6])
#print(tr[-20])

#------------------------------------------------------------------------------------------------------------------

#Problema 3 - Complexidade de n^2 + 1000n
'''
Pela definição de uma função ser O(n^2), podemos tomar por exemplo as constantes C = 2 e N = 1000, e assim temos que:
n^2 + 1000n = 2*n^2 - (n^2 - 1000n) <= 2*n^2, pois para n >= 1000, n^2 >= 1000n, fazendo (n^2 - 1000n) >= 0 e assim 2*n^2 - (n^2 - 1000n) <= 2*n^2. Portanto, tais constantes cumprem a definição de n^2 + 1000n ser O(n^2). Agora mostraremos que os outros exemplos de constantes também funcionam.

c = 101 e n = 10:
n^2 + 1000n = 101n^2 - (100n^2 - 1000n) <= 101n^2, pois para n >= 10, 100n >= 1000 e 100n^2 >= 1000n, e isso faz (100n^2 - 1000) >= 0 e portanto 101n^2 - (100n^2 - 1000) <= 101n^2. Logo, essas constantes servem para a definição da complexidade.

c = 1001 e n = 1:
n^2 + 1000n = 1001n^2 - (1000n^2 - 1000n) <= 1001n^2, pois para n >= 1, n^2 >= n e 1000n^2 >= 1000n, então 1000n^2 - 1000n >= 0 e isso leva a 1001n^2 - (1000n^2 - 1000n) <= 1001n^2. Logo, essas constantes também servem para a definição da complexidade.
'''

#------------------------------------------------------------------------------------------------------------------

#Problema 4 - g é O(f) se e somente se f é Ω(g)
'''
Primeiro, provaremos se g é O(f), então f é Ω(g).
Se g é O(f), significa que existem constantes C e X tal que para todo x >= X, g(x) <= C*f(x). Logo, também é válido que C*f(x) >= g(x) e que f(x) >= (1/C)*g(x).

Note que isso equivale a dizer que para as constantes X e (1/C), temos que f é Ω(g), como queríamos.

Agora, provaremos se f é Ω(g), então g é O(f) 
Se f é Ω(g), significa que existem constantes C e X tal que para todo x >= X, f(x) >= C*g(x). Logo, também é válido que C*g(x)  <= f(x) e que g(x) <= (1/C)*f(x).

Note que isso equivale a dizer que para as constantes X e (1/C), temos que g é O(f), como queríamos.
'''

#------------------------------------------------------------------------------------------------------------------

#Problema 5 - g é Θ(f) se e somente se f é Θ(g)
'''
Se g é Θ(f), existem constantes C e X' tal para todo x >= X', C*f(x) <= g(x), e ainda, existem constantes D e X'' tal que para todo x >= X'', D*f(x) >= g(x).

Percebe-se que dadas essas desigualdades, significa que existem constantes C,D,X=Max(X',X''), tal que para todo x >= X, C*f(x) <= g(x) <= D*f(x).

Como C*f(x) <= g(x), então (1/C)*g(x) >= f(x) e como g(x) <= D*f(x), f(x) >= (1/D)*g(x).

Note que isso implica que, para x >= X, (1/D)*g(x) <= f(x) <= (1/C)*g(x), que é definição de f ser Θ(g) para as constantes 1/D e 1/C. Como as funções são identicamente simétricas, isso também implica que se f for Θ(g), então g é Θ(f).
'''