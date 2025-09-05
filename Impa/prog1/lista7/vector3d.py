class Vector3D:
	def __init__(self, vals:list = []): #Método init - recebe uma lista e garante que tenha ao menos 3 posições para serem salvas
		while(len(vals) < 3): vals += [0]
		self.val = [float(vals[0]),float(vals[1]),float(vals[2])]
	def __add__(self, v2): #Soma coordenada a coordenada do vetor
		return Vector3D([self.val[0]+v2.val[0], self.val[1]+v2.val[1], self.val[2]+v2.val[2]])
	def __mul__(self, alfa:float): #Produto por escalar coordenada a coordenada do vetor
		return Vector3D([self.val[0]*alfa, self.val[1]*alfa, self.val[2]*alfa])
	def __str__(self): #Faz uma string no formato [A, B, C] sendo A,B,C as coordenadas do vetor
		return f"[{self.val[0]:.3f}, {self.val[1]:.3f}, {self.val[2]:.3f}]"
	
class float(float):
	def __mul__(self, v:Vector3D):
		return Vector3D([v.val[0]*self, v.val[1]*self, v.val[2]*self])