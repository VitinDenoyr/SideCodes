#Problema 1 - Escreva a saída padrão esperada
x = 2
myList = [1, 2, 3, 4]
myDict = {
	'chave1': 1,
	'chave2': x,
	3 : 'Value',
	(1,2) : 'Nossa que massa!!!',
	'L' : myList
}
x = 3
myDict['L'][2] = 5

'''
#Item A
1
2

#Item B
Value is bad

#Item C
que massa!

#Item D
[1, 2, 5, 4]
'''

#---------------------------------------------------------------------

#Problema 2 - Observar código e corrigir o erro

#Item A:
#A função de inicialização deve se chamar "__init__" e não "__ints__", corrigindo isso temos:

'''
class Vector():
	def __init__(self, values):
		"""
		Initializes the vector with the given values.
		"""
		self.values = values
		self.dim = len(self.values)

	def add( self, other_vector):
		"""
		Returns a new vector that represents the sum of this
		vector and the given vector.
		It checks if the dimensions of the two vectors are equal,
		if not returns an empty list.
		"""
		if other_vector.dim != self.dim:
			return []
		new_vector = [0] * self.dim
		for i in range(self.dim):
			new_vector[i] = self.values[i] + self.values[i]
		return new_vector
v = Vector([0.0 , 2.0 , 3.5 ])
u = Vector([1.0, 0.5])
w = Vector([2.0, 1.5])
print(v.add(u))
print(u.add(w))
'''

#Item B:
'''
Com esse código, a saída padrão é:
[]
[2.0, 1.0]
'''

#Item C:
'''
O código deveria somar os dois vetores, mas do método atual verifica se são somáveis mas apenas dobra o vetor original. Para funcionar, deveríamos substituir new_vector[i] = self.values[i] + self.values[i] por new_vector[i] = self.values[i] + other_vector.values[i]
'''

#---------------------------------------------------------------------

#Problema 3 - Criar as classes
#Item A:
class Circle:
	def __init__(self, point:list, radius:float):
		self.radius = radius
		self.center = point
	def contains(self, point:list):
		#Calcula a distância ao quadrado (para não perder precisão com raiz) do ponto até o centro do círculo
		dist2 = (point[0] - self.center[0])**2 + (point[1] - self.center[1])**2
		if dist2 < self.radius**2: #Retorna que está dentro se ela for menor que o raio ao quadrado
			return 1 #Dentro
		elif dist2 > self.radius**2: #Fora se for maior que o raio ao quadrado
			return -999 #Fora
		return 0 #Exatamente na circunferência se for o raio ao quadrado

#Item B:
class LineSegment:
	def __init__(self, pointA:list, pointB:list):
		#Define os pontos de início e fim da reta
		if pointA[0] < pointB[0]:
			self.start = pointA
			self.end = pointB
		else:
			self.start = pointB
			self.end = pointA

	def contains(self, point:list): #3 pontos A = (a,a*m+n), B = (b,b*m+n), P = (p,p*m+n) são colineares na reta m*x+n com P contido no segmento AB se e somente se P.x está em [A.x, B.x] e (P-A).x*(B-P).y == (P-A).y*(B-P).x
		cond1 = (point[0]-self.start[0])*(self.end[0]-point[0]) >= 0
		cond2 = (point[0]-self.start[0])*(self.end[1]-point[1]) == (point[1]-self.start[1])*(self.end[0]-point[0])
		if cond1 and cond2:
			return True
		return False
	
#---------------------------------------------------------------------

#Problema 4 - Usando as classes verifique se um circulo contem uma reta

def circleContainSegment(circ:Circle, seg:LineSegment):
	#Se um círculo contém as duas extremidades, ele contém todo o segmento
	return circ.contains(seg.start) + circ.contains(seg.end) >= 0

#---------------------------------------------------------------------

#Problema 5 - Calcular o produto interno
class Vector:
	def __init__(self, val:list):
		self.val = val
		self.dim = len(val)
	def dyadic_product(self, vec):
		mat = [[0 for y in range(vec.dim)] for z in range(self.dim)] #Criar matriz MxN 'vazia'
		for i in range(self.dim):
			for j in range(vec.dim):
				mat[i][j] += self.val[i]*vec.val[j] #mat[i][j] = v1[i]*v2[j]
		return mat