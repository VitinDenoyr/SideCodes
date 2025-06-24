import numpy as np
from scipy.stats import uniform
from scipy.linalg import eigh_tridiagonal
import matplotlib.pyplot as plt
	
# Variaveis de Controle:
# N = tamanho das matrizes. LIM = modulo maximo das entradas. C = Numero de colunas de Q escolhidas.
N = 100; LIM = 1000000; C = 8; TST = 5000
	
# Funcao de plotagem
def plot(Matrix,Type,zero):
	plt.figure(figsize=(10, 6))
	for i in range(C):
		plt.plot(np.log10(np.abs(Matrix[:, i]) + zero), label=f'Q_{i+1}')
	plt.title(f'Escala Logaritmica dos Autovetores - {Type}')
	plt.xlabel('Indice da entrada')
	plt.ylabel('log10(||q||)')
	plt.legend()
	plt.grid(True)
	plt.show()
	
def simulateRandom(willPlot = True):
	# Criar matriz Hermitiana Tridiagonal Aleatoria com entradas [-LIM,LIM]
	# Diagonal principal = Primeiras N entradas. Diagonais secundarias = proximas entradas.
	dt = uniform.rvs(size=(2*N-1),scale=2*LIM,loc=-LIM)
	
	# Obter os autovetores e autovalores (Como o objetivo do exercicio nao e explicitamente implementar o algoritmo citado no capitulo, usei a funcao eigh_tridiagonal do scipy.linalg)
	lamb, Q = eigh_tridiagonal(dt[:N], dt[N:2*N-1])
	
	# Plotar as colunas da matriz
	if willPlot:
		plot(Q,"Tridiagonal Aleatoria",1e-20)
	else:
		QFiltro = np.abs(Q) > 1e-10
		return np.sum(QFiltro)
	
def simulateLaplacian(willPlot = True):
	# Criar uma matriz laplaciana (1,-2,1)
	laplace1 = -2 * np.ones(N)
	laplace2 = np.ones(N - 1)
	
	lamb, Q = eigh_tridiagonal(laplace1, laplace2)
	
	# Plotar as colunas da matriz
	if willPlot:
		plot(Q,"Laplaciana",0)
	else:
		QFiltro = np.abs(Q) > 1e-10
		return np.sum(QFiltro)
	
# Calculando o valor esperado de entradas
Expect = 0
for i in range(TST):
	Expect = Expect + simulateRandom(0)
	
print(f"Valor esperado da quantidade de entradas acima de 10^-10:{Expect/TST:.0f}")
	
# Gerar os graficos:
simulateRandom()
simulateLaplacian()