# python 3.10

from VectorSpace import VectorSpace

class RealVector(VectorSpace):
	_field = float
	def __init__(self, dim, coord):
		super().__init__(dim, self._field)
		self.coord = coord
		
	@staticmethod
	def _builder(coord):
		raise NotImplementedError

	def __add__(self, other_vector):
		n_vector = []
		for c1, c2 in zip(self.coord, other_vector.coord):
			n_vector.append(c1+c2)
		return self._builder(n_vector)

	def __mul__(self, alpha):
		n_vector = []
		for c in self.coord:
			n_vector.append(alpha*c)
		return self._builder(n_vector)
		
	def iner_prod(self, other_vector):
		res = 0
		for c1, c2 in zip(self.coord, other_vector.coord):
			res += c1*c2
		return res

	def __str__(self):
		ls = ['[']
		for c in self.coord[:-1]:
			ls += [f'{c:2.2f}, ']
		ls += f'{self.coord[-1]:2.2f}]'
		s =  ''.join(ls)
		return s

class Vector2D(RealVector):
	_dim = 2
	def __init__(self, coord):
		if len(coord) != 2:
			raise ValueError
		super().__init__(self._dim, coord)

	@staticmethod
	def _builder(coord):
		return Vector2D(coord)
	
	def __neg__(self):
		return Vector2D([-self.coord[0],-self.coord[1]])
 
	def __sub__(self, v:'Vector2D'):
		return	self+(-v)

	def __rmul__(self, alfa:float):
		return self*alfa

	def __abs__(self):
		return (self.coord[0]**2 + self.coord[1]**2)**(0.5)
		
	def CW(self):
		return Vector2D([-self.coord[1], self.coord[0]])
		
	def CCW(self):
		return Vector2D([self.coord[1], -self.coord[0]])

	def __eq__(self, v:'Vector2D'):
		return (self.coord[0] == v.coord[0] and self.coord[1] == v.coord[1])

class Vector3D(RealVector):
	_dim = 3
	def __init__(self, coord):
		if len(coord) != 3:
			raise ValueError
		super().__init__(self._dim, coord)

	@staticmethod
	def _builder(coord):
		return Vector3D(coord)
	
	def __neg__(self): #Negação de um vetor (-v)
		return Vector3D([-self.coord[0],-self.coord[1],-self.coord[2]])

	def __sub__(self, v:'Vector3D'):
		return	self+(-v)

	def __rmul__(self, alfa:float): #Multiplicação pela esquerda
		return self*alfa

	def __abs__(self): #Módulo/Comprimento de um vetor: Definido com v = [x,y,z] -> abs(v) = sqrt(x^2 + y^2 + z^2)
		return (self.coord[0]**2 + self.coord[1]**2 + self.coord[2]**2)**(0.5)

	def __eq__(self, v:'Vector3D'): #Igualdade entre vetores: São iguais se tiverem as mesmas coordenadas
		return (self.coord[0] == v.coord[0] and self.coord[1] == v.coord[1] and self.coord[2] == v.coord[2])

	def vectorProduct(self, v:'Vector3D'): #Produto Vetorial: Definição matemática por determinante
		return Vector3D([
			self.coord[1]*v.coord[2] - self.coord[2]*v.coord[1],
			self.coord[2]*v.coord[0] - self.coord[0]*v.coord[2],
   			self.coord[0]*v.coord[1] - self.coord[1]*v.coord[0],
		])
		
if __name__ == '__main__':
	V2 = Vector2D([1, 2])
	print('V2 = ', V2)
	W2 = Vector2D([3, 4])
	print('W2 = ', W2)

	print(V2.getVectorSpace())

	r = V2+4*W2
	print('V2 + 4*W2 =', r)
	print('(V2 + 4*W2).CW() = ', r.CW())
	print('W2.CCW() = ', W2.CCW())
	print('V2.iner_prod(W2) = ', V2.iner_prod(W2))
 