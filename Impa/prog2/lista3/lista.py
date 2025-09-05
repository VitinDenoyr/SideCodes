import numpy as NP
from RealVector import Vector3D

# -------------------------------------- PROBLEMA 1 --------------------------------------
class Vector3D(Vector3D): #Adiciona novas operações a Vector3D
	def __abs__(self): #Módulo de um vetor: Definido com v = [x,y,z] -> abs(v) = sqrt(x^2 + y^2 + z^2)
		return (self.coord[0]**2 + self.coord[1]**2 + self.coord[2]**2)**(0.5)
	
	def __eq__(self, v: 'Vector3D'): #Operador ==, coordenada a coordenada
		#Tolerância para erros de cálculo considerada em atol e rtol, onde os valores usados são os apresentados na seção 7 do github, visto que até o momento de fazer essa questão não foi requisitado usar o epsilon da máquina. Usei o Numpy.isclose apenas para ficar similar ao github.
		return (
			NP.isclose(self.coord[0], v.coord[0], atol=1e-25, rtol=1e-15) and
			NP.isclose(self.coord[1], v.coord[1], atol=1e-25, rtol=1e-15) and
			NP.isclose(self.coord[2], v.coord[2], atol=1e-25, rtol=1e-15)
		)
	
	def __lt__(self, v: 'Vector3D'): #Operador <, com as normas
		#Tolerância calculada assumindo o valor similar ao do exercício anterior
		#Se a diferença das normas for pequena demais, consideramos a norma igual e portanto não queremos isso no operador <, então usaremos que a diferença dos módulos seja negativa e menor que -tolerance
		tolerance = 1e-25
		return (abs(self) - abs(v)) < -tolerance

	def __gt__(self, v: 'Vector3D'): #Operador >, análogo ao anterior
		tolerance = 1e-25
		return (abs(self) - abs(v)) > tolerance

	def __le__(self, v: 'Vector3D'): #Operador <=, com as normas
		#Parecido com o operador __lt__, mas se a diferença for positiva mas menor que tolerance, será ainda igual e considerada no <=.
		tolerance = 1e-25
		return (abs(self) - abs(v)) < tolerance

	def __ge__(self, v: 'Vector3D'): #Operador >=, análogo ao anterior
		tolerance = 1e-25
		return (abs(self) - abs(v)) > -tolerance



# -------------------------------------- PROBLEMA 2 --------------------------------------
'''
Para representar o sinal, basta um bit somente.

Note que usando dígitos na base β, podemos representar β^p números, então, precisamos de ceil(log2(β^p)) bits para conseguir com garantia representar todos os bits, visto que ceil(log2(β^p)) >= log2(β^p), e com essa quantia de bits conseguiríamos representar 2^(log2(β^p)) = β^p números distintos, como queríamos fazer com a mantissa.

Dada a mantissa, precisamos agora saber quantos bits são necessários para representar todos os expoentes distintos. Como os expoentes são inteiros no intervalo [e_min, e_max], há e_max - e_min + 1 números distintos para serem representados, e pela mesma lógica, são necessários ceil(log2(e_max - e_min + 1)) bits para representar todos os números nesse intervalo.

No total, portanto, precisamos de 1 + ceil(log2(β^p)) + ceil(log2(e_max - e_min + 1)) bits para representar todos os números da maneira descrita no enunciado do problema.
'''



# -------------------------------------- PROBLEMA 3 --------------------------------------
def machineEpsylon():
	'''
    	Justificativa: Considere a representação binária do número. Partimos do fato de que 1 é representado com o	menor número não-nulo na mantissa, e seu expoente sendo o padrão da representação binária de um float.
     
     	A partir disso, veremos qual o menor expoente considerado para que a desigualdade se mantenha, pois se um bit é considerado, combinações desse bit também são, então teremos que o epsilon da maquina será o "menor bit de expoente" considerado na representação do float com a mantissa sendo a menor mantissa não nula possível.
    
    	Note que o algoritmo abaixo calcula isso, pois parte do valor de 1 e divide o possível epsilon da máquina por 2 continuamente, que é equivalente a diminuir o valor do bit do expoente repetidamente, garantindo assim que achará no momento certo o menor bit considerado.
	'''
	eps = 1.0
	while((1+(eps/2.0)) != 1):
		eps /= 2.0
	return eps



# -------------------------------------- PROBLEMA 4 --------------------------------------
def largeMachineEpsylon():
	eps = 1.0
	while((1e6+(eps/2.0)) != 1e6):
		eps /= 2.0
	return eps
'''
	Diferenças: O epsilon da máquina se adequa a ordem de grandeza do número. Como um grande número usa mais bits para serem guardados, isso implica que há menos bits disponíveis para serem usados na representação do restante do float, tanto para haver uma preservação de espaço, quanto pelas mudanças de números pequenos em números grandes serem menos significativas.
 
 	Veja que a razão entre os epsilons da máquina calculados está na ordem de 10^6, que é também proporcional a razão entre os números em que o epsilon da máquina foi calculado ao redor, onde possivelmente reduziu-se na precisão o valor numérico do número de bits gastos para representar o número grande.
  
  	Isso implica que quanto maior sua precisão decimal, menos bits você deveria estar usando para representar os "números-base", para assim o epsilon da máquina ser mais preciso e tornar seus cálculos mais acurados.
'''



# -------------------------------------- PROBLEMA 5 --------------------------------------
'''
Note que o problema pede que a precisão seja exata na ordem de milímetros, mas que as contas consigam ser realizadas na ordem de centenas de km também.

Sabemos que os erros de precisão surgem pois há dificuldades de representar números racionais que não são uma soma de potências de dois (com expoentes negativos ou positivos), e isso causa erros de aproximação. Uma boa forma de contornar isso é evitar o uso de floats, utilizando as medidas como inteiros na unidade de milimetros, pois é a precisão mínima exigida.

Criaremos uma classe Coordenada, que tem como argumento inicial as coordenadas em milímetros do ponto em relação a outro ponto, e o segundo argumento são as coordenadas desse outro ponto que será o pivô: um ponto que terá no nosso sistema de coordenadas o valor (0,0,0), mas no 'sistema da vida real de coordenadas' pode ter outro valor referente. novamente, em unidade de milímetros em cada eixo entre [x,y,z].

O classe também recebe no init um nome, que representa um nome único de um pivô e o que ele representa: por exemplo, se estamos construindo uma plataforma de petróleo, o nome representaria essa plataforma para evitar que coordenadas de diferentes pivôs realizem operações entre si, pois isso traria erros de precisão, que é o que estamos tentando evitar. 

Assim, calcularemos as posições dos objetos do sistema assumindo como paradigma que cada objeto tem um ponto notável específico que pode ser usado para identificar sua posição, por exemplo, poderia ser o canto superior esquerdo de algo retangular ou um ponto "central" de algo circular, como a extremidade do eixo central de um cilindro.

Como os inteiros não possuem erro de aproximação e podem ser armazenados tranquilamente quando consideramos inteiros na ordem de [-10^10, 10^10] (ou até maior se necessário), que seria o equivalente números com precisão entre 0mm e 10^9mm => 0mm e 10000km, um escopo que julgo mais que adequado a precisão exigida de mm em centenas de km, esse tipo de coordenadas com um pivô de referência e medidas inteiras parece o mais adequado.
'''

class Coordenada:
	def __init__(self, value: list, pivo:list, nomePivo): #Exige-se duas listas de 3 coordenadas (pelo plano 3D) e o nome do pivô.
		if (type(value) != type([])) or (type(pivo) != type([])) or (type(nomePivo) != type(" ")):
			raise TypeError("Entrada inválida para coordenada")
		if (len(value) != 3) or (len(pivo) != 3) or (len(nomePivo) == 0):
			raise ValueError("Entrada com valores incorretos")

		self.c = [int(value[0]), int(value[1]), int(value[2])] #Valores nos eixos x,y,z
		self.pivot = pivo
		self.pivotName = nomePivo

	def validateOperation(self, v:'Coordenada'): #Validar operação aritmética, garante o mesmo pivô
		if v.pivotName != self.pivotName:
			raise ValueError("Tentativa de operação aritmética entre coordenadas de pivôs diferentes.")

	#Operações básicas necessárias
 
	def __add__(self, v:'Coordenada'): #Adição de coordenadas
		self.validateOperation(v)
		return Coordenada([self.c[0] + v.c[0], self.c[1] + v.c[1], self.c[2] + v.c[2]],self.pivot,self.pivotName)
  
	def __sub__(self, v:'Coordenada'): #Subtração de coordenadas
		self.validateOperation(v)
		return Coordenada([self.c[0] - v.c[0], self.c[1] - v.c[1], self.c[2] - v.c[2]],self.pivot,self.pivotName)
	
	def __neg__(self): #Negação
		return Coordenada([-self.c[0],-self.c[1],-self.c[2]],self.pivot,self.pivotName)

	def __mul__(self, v:int): #Multiplicação por escalar
		return Coordenada([self.c[0] * v, self.c[1] * v, self.c[2] * v],self.pivot,self.pivotName)

	def __rmul__(self, v:int): #Multiplicação por escalar ao outro lado
		return self.__mul__(v)

	#Representar as coordenadas
	
	def stringify(self, id:int):
		if (id != 0 and id != 1 and id != 2 and id != 3):
			raise ValueError("Unidade incorreta.")
		unit = ['mm','cm','m','km']
		dv = [1,10,1000,1000000]
  
		if id == 0:
			return f"[{self.c[0]}{unit[id]}, {self.c[1]}{unit[id]}, {self.c[2]}{unit[id]}]"
		else:
			return f"[{self.c[0]/dv[id]:.6f}{unit[id]}, {self.c[1]/dv[id]:.6f}{unit[id]}, {self.c[2]/dv[id]:.6f}{unit[id]}]"

	def toMM(self):
		return self.stringify(0)

	def toCM(self):
		return self.stringify(1)

	def toM(self):
		return self.stringify(2)

	def toKM(self):
		return self.stringify(3)

	def __repr__(self):
		return self.toMM()



# --------------------------------------   TESTES   --------------------------------------
if __name__ == '__main__':
	print(f"Testes: Problema 1")
	v1 = Vector3D([1,       2.131, 3.5646 + 1e-30])
	v2 = Vector3D([1+1e-20, 2.131, 3.5646        ])
	v3 = Vector3D([1+1e-14, 2.131, 3.5646        ])
	print(f"v1 == v2? {v1 == v2};\nv1 == v3? {v1 == v3}")
	print(f"v1 < v2? {v1 < v2};\nv1 < v3? {v1 < v3}")
	print(f"v1 <= v2? {v2 >= v1};\nv1 <= v3? {v3 >= v1}",end="\n\n\n")
 
	print(f"Testes: Problema 4")
	print(f"Epsilon da maquina em torno de 1 = {machineEpsylon()}")
	print(f"Epsilon da maquina em torno de 10^6 = {largeMachineEpsylon()}",end="\n\n\n")
 
	print(f"Testes: Problema 5")
	parafuso1 = Coordenada([1,4,6],[1531,6463,1353],"Fabrica")
	parafuso2 = Coordenada([13,4135,631],[1531,6463,1353],"Fabrica")
	peca1 = Coordenada([1,4,7],[19700,15000,103000],"Petroleira")

	print(f"{parafuso1}, {parafuso2} = {parafuso1.toKM()}, {parafuso2.toKM()}")
	print(f"{10*parafuso1 + parafuso2*2} = 2*{parafuso2} + 10*{parafuso1}")