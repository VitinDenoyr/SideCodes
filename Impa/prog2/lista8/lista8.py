import numpy as NP
import matplotlib.pyplot as MPL
import time as TIME

probTests = int(input("Digite o problema para executar os testes\n 0 -> Todos\n 1 -> Problema 1\n 2 -> Problema 2\n 3 -> Problema 3-A\n 4 -> Problema 3-B\n 5 -> Problema 3-C\nOBS: O problema 4D é basicamente uma parte do código que está presente nos outros itens, visto que o gráfico está sendo criado, visualizando as retas\n"))

# ---------------------- Problema 1 ----------------------

'''
Classe PolynomialMatcher
	self.deg -> grau do polinômio, que foi dito pelo usuário
	setCoefs() -> dados dois vetores de tamanho N com coordenadas x e y dos N pontos, constroi a matriz de vadermonte com as coordenadas X e usa o método dos menores quadrados para aproximar um polinômio desse grau e definir seus coeficientes. É usado a versão do numpy, pois já aborda polinômios diretamente
	evaluate() -> Usando o polinômio com coeficientes obtidos, calcula o valor dele em pontos de x
	__call__() -> Permite chamar o evaluate com ()
	plot() -> Plota com matplotlib o polinômio e os pontos com qualidade definida na função, onde a qualidade é a quantidade de pontos no gráfico para desenhar
'''
class PolynomialMatcher:
	def __init__(self, deg):
		self.deg = deg
		self.coefs = None #Ainda vai calcular
		self.x = None #Ainda falta
		self.y = None #Ainda tbm falta

	def setCoefs(self, xCoords, yCoords):
		self.x = xCoords
		self.y = yCoords

		#Constantes uteis para o problema 2
		self.x_medio = NP.mean(xCoords)
		self.y_medio = NP.mean(yCoords)

		X = NP.vander(xCoords, self.deg + 1)
		# Calcula os coeficientes do polinômio (método dos mínimos quadrados)
		self.coefs = NP.linalg.lstsq(X, yCoords, rcond=None)[0]

	def evaluate(self, x):
		if self.coefs is None:
			raise ValueError("Polinômio ainda indefinido, defina-o primeiro")
		return NP.polyval(self.coefs, x)
	
	def __call__(self, x):
		self.evaluate(x)

	def plot(self, quality=1000):
		MPL.scatter(self.x, self.y, label="Pontos dados", color="red")
		x_range = NP.linspace(min(self.x), max(self.x), quality) #Intervalo X
		y_range = self.evaluate(x_range)
		
		MPL.plot(x_range, y_range, label=f"Polinômio de grau {self.deg}", color="blue")
		MPL.legend()
		MPL.xlabel("x")
		MPL.ylabel("y")
		MPL.grid()
		MPL.show()

if __name__ == "__main__" and probTests <= 1:

	deg = int(input("Informe o grau do polinômio: "))
	NP.random.seed(int(TIME.time()))
 
	# Nuvem de pontos qualquer
	xCoords = NP.linspace(-deg,deg,10)
	yCoords = NP.random.uniform(-50,50,10)
 
	approximator = PolynomialMatcher(deg)
	approximator.setCoefs(xCoords, yCoords)
	approximator.plot()

# ---------------------- Problema 2 ----------------------

'''
Note que, na maioria dos casos, o que ocorre é o seguinte:
	- Se foram dados muitos pontos em relação ao grau do polinômio, eles podem se tornar impossíveis de serem bem aproximados por um polinômio de grau pequeno, precisando de um grau maior, para fazer mais curvas
	- Se forem dados poucos pontos em relação ao grau do polinômio, eles podem ser bem definidos por polinômios de graus grandes, mas o que normalmente ocorre é o surgimentos de curvas muito acentuadas que acabam fugindo bastante da nuvem de pontos, então o ideal seria um polinômio de grau menor.
 
	Note que aplicando essas observações, temos dois estados de aproximação dados os pontos e um grau: O estado bem aproximado e o mal aproximado, onde o bem aproximado deve diminuir o grau, enquanto o mal aproximado deve aumentar o grau.
 
	Isso caracteriza informação suficiente para uma busca binária, tentando chegar no grau ideal diminuindo o intervalo que o grau ideal pode estar dados dois valores distantes para os limites.
 
	Para determinar qual dos "estados" estamos, consideraremos a soma dos quadrados dos resíduos. Esse erro definirá se está "próximo o bastante" ou não.
'''

#Soma dos quadrados dos resíduos -> coeficiente de determinação R2
def coefR2(xCoords, yCoords, deg):
	approximator = PolynomialMatcher(deg)
	approximator.setCoefs(xCoords, yCoords)
 
	#Calcular os dados para a soma dos quadrados dos resíduos com o rss e tss
	rss = NP.sum((yCoords - approximator.evaluate(NP.array(xCoords)))**2)
	tss = NP.sum((yCoords - approximator.y_medio)**2)

	#Retorna o coeficiente R2 de determinação
	return 1 - (rss/tss)

#Busca binária em grau <= maxDeg
def binSearch(xCoords, yCoords, maxDeg = 20):
	l , r = 1, maxDeg #Limites da busca binária
		
	while l < r:
		mid = (l+r)//2
		newR2 = coefR2(xCoords, yCoords, mid)
   
		if newR2 > 0.995: #Está ao menos 99.5% bom, estão está bem aproximado. Diminua o grau
			r = mid
		else: #Está mal aproximado, estão aumente o grau
			l = mid+1
	
	return l

if __name__ == "__main__" and (probTests == 0 or probTests == 2):
	#Algumas nuvens de pontos
	x_tests = [
		[1,2,3,4,5,6,7,8],
		[2,4,6,8,10,12],
		[-3,-1,0,1,2,4],
		[3,4,5,6,7,8,9,10,11],
		[0,5,10,15,20],
		[0,1,2,3,4,5,6]
	]
	y_tests = [
		[1,4,9,16,25,36,49,64],
		[0,1,3,7,15,31],
		[-8,0,1,8,27,125],
		[7,9,11,13,15,17,19,21,23],
		[1,6,11,179,21],
		[40,0,-36,0,18,0,1500]
	]

	tnumb = 1
	for x, y in zip(x_tests, y_tests):
		bestDeg = binSearch(x,y,maxDeg=min(20,2*len(x)))
		print(f"Melhor grau no teste {tnumb}: {bestDeg}")
		tnumb += 1
		
		approximator = PolynomialMatcher(bestDeg)
		approximator.setCoefs(x, y)
		approximator.plot()
  
# ---------------------- Problema 3 ----------------------
from scipy.optimize import minimize

x_tests = [
	NP.array([1,2,3,4,5,6,7,8]),
	NP.array([2,4,6,8,10,12]),
	NP.array([-3,-1,0,1,2,4]),
	NP.array([3,4,5,6,7,8,9,10,11]),
	NP.array([0,5,10,15,20]),
	NP.array([0,1,2,3,4,5,6]),
	NP.array([0,1.4285714285714286,2.857142857142857,4.285714285714286,5.714285714285714,7.142857142857143,8.571428571428571,10.0])
]
y_tests = [
	NP.array([1,4,9,16,25,36,49,64]),
	NP.array([0,1,3,7,15,31]),
	NP.array([-8,0,1,8,27,125]),
	NP.array([7,9,11,13,15,17,19,21,23]),
	NP.array([1,6,11,179,21]),
	NP.array([40,0,-36,0,18,0,15]),
	NP.array([-5.655215911789961,6.063681318952608,13.766844508136844,20.42212078230105,30.006335789185535,39.14743019999067,49.26808073264344,55.96919861441928])
]

#Função que calcula a soma dos erros absolutos
def calcSumAbs(parametros):
	a,b = parametros
	return NP.sum(NP.abs(a*x_tests[tnumb] + b - y_tests[tnumb]))

#Função que calcula a soma dos erros quadráticos
def calcSumQuad(parametros):
	a,b = parametros
	return NP.sum((a*x_tests[tnumb] + b - y_tests[tnumb])**2)

#Função que lê o arquivo de generatePoints.py e retorna arrays numpy com as coordenadas x e y
def readFile(filepath):
	x_coords = []
	y_coords = []
	with open(filepath, 'rt') as file:
		for ln in file: #Pra cada linha do arquivo
			x, y = map(float, ln.split())
			x_coords.append(x)
			y_coords.append(y)
	return NP.array(x_coords), NP.array(y_coords)

#Testes 3A
if __name__ == "__main__" and (probTests == 0 or probTests == 3):
	tnumb = 0
	#Usa scipy minimize com chute inicial [1,1]
	print("Parte A")
	for x, y in zip(x_tests, y_tests):
		a,b = minimize(calcSumAbs,[1,1]).x
		print(f"Melhores valores para (a,b) no teste {tnumb+1}: ({a:.2f},{b:.2f})")
  
		approximator1 = PolynomialMatcher(1)
		approximator1.coefs = NP.array([a, b])
		approximator1.x = x
		approximator1.y = y
		approximator1.plot()
		tnumb += 1
  
#Testes 3B
if __name__ == "__main__" and probTests%4 == 0:
	#Estou assumindo que você já está na pasta do arquivo de testes, que é meu caso
	tnumb = 0
	print("Parte B")
	for v in [64, 128, 256, 512, 1024]:
		filepath = f'xy{v}.txt'
		x_tests[tnumb], y_tests[tnumb] = readFile(filepath)
		
		a,b = minimize(calcSumAbs,[0,1]).x
		print(f"Melhores valores para (a,b) no teste {tnumb+1}: ({a:.2f},{b:.2f})")
  
		approximator2 = PolynomialMatcher(1)
		approximator2.coefs = NP.array([a, b])
		approximator2.x = x_tests[tnumb]
		approximator2.y = y_tests[tnumb]
		approximator2.plot()
		tnumb += 1

  
#Testes 3C
if __name__ == "__main__" and probTests%5 == 0:
	tnumb = 0
	#Usa scipy minimize com chute inicial [1,1]
	print("Parte C")
	for x, y in zip(x_tests, y_tests):
		a,b = minimize(calcSumQuad,[1,1]).x
		print(f"Melhores valores para (a,b) no teste {tnumb+1}: ({a:.2f},{b:.2f})")
  
		approximator3 = PolynomialMatcher(1)
		approximator3.coefs = NP.array([a, b])
		approximator3.x = x
		approximator3.y = y
		approximator3.plot()
		tnumb += 1

	tnumb = 0
	for v in [64, 128, 256, 512, 1024]:
		filepath = f'xy{v}.txt'
		x_tests[tnumb], y_tests[tnumb] = readFile(filepath)
		
		a,b = minimize(calcSumQuad,[0,1]).x
		print(f"Melhores valores para (a,b) no teste {tnumb+1}: ({a:.2f},{b:.2f})")
  
		approximator4 = PolynomialMatcher(1)
		approximator4.coefs = NP.array([a, b])
		approximator4.x = x_tests[tnumb]
		approximator4.y = y_tests[tnumb]
		approximator4.plot()
		tnumb += 1
  
# Problema 3E - Vantagens
'''
Vêmos que em alguns tipos de nuvens de pontos, a aproximação minimizando soma dos valores absolutos da diferença 
acaba por na prática "escanear" todos os coeficientes da reta e para cada um deles, arrastar a reta até a mediana 
dos pontos, visto que é possível provar que fixado um coeficiente, isso minimaliza a soma dos valores absolutos. 
Isso pode ser bom principalmente quando você quer encontrar uma reta que represente bem o lugar com no plano com 
maior "densidade de pontos alinhados", visto que mesmo se houver um outlier com valor muito alto, ele praticamente 
será desconsiderado. Isso é algo que você quer que ocorra por exemplo analizando um conjunto de medições de um 
sensor, sem ter o problema de que o sensor as vezes pode ler um número absurdo (ex: normalmente era para medir na 
escala de 1cm, mas mediu um único ponto como 1000km) sem danificar seus dados.

Já a aproximação minimizando o quadrado da diferença, na maioria dos casos se comporta de uma forma levemente 
similar a outra: ambas aproximando bem conjuntos que parecem retas, mas esta por sua vez tenta minimizar um pouco 
mais o "erro máximo" do que a outra abordagem, que prioriza mais um "erro médio". Por conta disso, ela tem a 
vantagem de sempre conseguir aproximar bem uma nuvem de pontos com poucos pontos extremamente longes do previsto, 
se possível, mas por outro lado, acaba por ser vulnerável a casos em que vários pontos tem valores pequenos (ordem 
de 1), e um único ponto tem um valor gigante, provavelmente por erro de medição (ordem de 10^9), e como ela 
considera o quadrado da diferença, acaba que a reta talvez se afaste mais da maioria dos pontos para chegar mais 
perto do ponto extremamente distante, o que em alguns casos você quer que ocorra, em outros não. Basta escolher bem 
qual situação você está, e assim ambas serão ótimas abordagens para a maioria das situações adequadas.
'''