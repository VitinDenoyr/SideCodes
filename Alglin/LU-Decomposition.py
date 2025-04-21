import numpy as np
import scipy as sci

# Comparação com tolerância a erro de ponto flutuante
eq = np.frompyfunc(lambda a,b: np.abs(a-b) < 1e-12, 2, 1)

def LU_Decomposition(A): #Numpy
	n = len(A); m = len(A[0]) #A = nxm
	nl = 0 #Próxima linha livre
	index = np.zeros(n,dtype=int) #Índice das linhas, inicial = posição 
	for i in range(n):
		index[i] = i
  
	P = np.eye(n); L = np.eye(n); U = A.copy()
	ops = []

	#Início da iteração
	for i in range(m):
		if np.all(eq(U[nl:,i],U[nl:,i]*0)):
			continue
		idx = np.argmax(np.abs(U[nl:,i]))+nl
  
		#Troca as linhas do máximo e de cima
		U[[nl,idx]] = U[[idx, nl]]
		P[[nl,idx]] = P[[idx, nl]]
		index[nl],index[idx] = index[idx],index[nl]

		#Zera as outras linhas
		factor = U[nl+1:,i].reshape(n-nl-1,1) / U[nl,i]
		for ii,x in enumerate(factor,start=nl+1):
			ops.append([index[ii],index[nl],x.item()])
		subtractors = np.repeat(U[nl:nl+1],n-nl-1,axis=0) * factor
		U[nl+1:] -= subtractors
		nl += 1
		if (nl == n):
			break

	#Construir vetor que informa qual linha está a linha com cada índice
	where = np.zeros(shape=[n,1],dtype=int)
	for i in range(n):
		where[index[i]] = i

	#Construir matriz L
	for op in ops:
		Li = np.eye(n)
		Li[where[op[0]].item(), where[op[1]].item()] = op[2]
		L @= Li
  
	return P, L, U
  
A = np.array([
    [5.2, 3, -100],
    [161, 2.3, 69],
    [1, -4, 133.1]
],dtype=np.float64)

P, L, U = LU_Decomposition(A)