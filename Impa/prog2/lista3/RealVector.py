# python 3.10
import numpy as NP
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

class Vector3D(RealVector):
    # Início: Código da lista 1
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

	def vectorProduct(self, v:'Vector3D'): #Produto Vetorial: Definição matemática por determinante
		return Vector3D([
			self.coord[1]*v.coord[2] - self.coord[2]*v.coord[1],
			self.coord[2]*v.coord[0] - self.coord[0]*v.coord[2],
   			self.coord[0]*v.coord[1] - self.coord[1]*v.coord[0],
		])
	#Fim: Código da Lista 1