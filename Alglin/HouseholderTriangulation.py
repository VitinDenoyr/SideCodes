import numpy as np
np.set_printoptions(precision=2,suppress=True)

def HouseholderTriangulate(A):
	m, n = A.shape
	R = A.copy()
	Q = np.eye(m)
 
	adj = lambda v: v.conj().reshape(1,-1)

	for k in range(min(n,m-1)):
		#Calculando os vetores. O(m)
		x = R[k:m,k]
		alpha = np.sign(x[0]) * np.linalg.norm(x)
		v = x - alpha * np.eye(m-k,1).flatten()
		v /= np.linalg.norm(v)

		#Atualizando R. O(mn)
		vR = (adj(v) @ R[k:m,k:n])
		R[k:m,k:n] -= 2*(v.reshape(-1,1) @ vR)
  
		#Atualizando Q - Multiplicamos pela direita: Qn...Q1 = Q^-1. O(m^2)
		Q[:,k:m] -= 2*((Q[:,k:m] @ v.reshape(-1,1)) @ adj(v))
	return Q,R

A = np.array([
	[5.2, 3, -100],
	[161, 2.3, 69],
	[1, -4, 133.1],
],dtype=np.float64)

Q, R = HouseholderTriangulate(A)