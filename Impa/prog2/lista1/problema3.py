from RealVector import Vector3D
from VectorSpace import Polynomial

if __name__ == '__main__':
	
	#Teste de Vetores3D:
	V3 = Vector3D([2,0,0])
	W3 = Vector3D([0,5,0])
	X3 = Vector3D([0,0,10])
	P3 = Vector3D([4,5,0])
	Q3 = Vector3D([-2,0,-40])
	a1 = 25
	a2 = 4
 
	#Todos devem retornar verdade:
	print((2*V3 + W3) == P3)
	print(((-V3) - a2*X3) == Q3)
	print(abs(V3)*abs(W3) == abs(X3))
	print((V3.vectorProduct(W3)) == X3)
	print((W3.vectorProduct(X3)) == (a1*V3))
	print((-V3.vectorProduct(X3)) == (W3*a2))
 
	#Teste de Polinômios:
	p1 = Polynomial('x^3+x')
	p2 = Polynomial([[3,1],[1,1]])
	print(p1 + -(-p2)) #Deve printar a mesma coisa
	print(3*p2 - p1) #Que esse
 