import numpy as np

compare = np.frompyfunc(lambda a,b: np.abs(a-b) < 1e-12, 2, 1)

def LU_Decomposition(A):
    n = len(A); m = len(A[0]); nL = 0
    index = np.arange(n,dtype=int)
    where = np.arange(n,dtype=int)

    P = np.eye(n)
    L = np.eye(n)
    U = A.copy()
    operations = []
    
    for nC in range(m):
        if np.all(compare(U[nL:,nC],0)):
            continue
        l = np.argmax(np.abs(U[nL:,nC]))+nL
        
        if nL != l:
            U[[nL,l]] = U[[l, nL]]
            P[[nL,l]] = P[[l, nL]]
            index[nL],index[l] = index[l],index[nL]
            where[index[nL]],where[index[l]] = where[index[l]],where[index[nL]]
            
        alpha = U[nL+1:,nC] / U[nL,nC]
        for i,x in enumerate(alpha,start=nL+1):
            operations.append([index[i],x,index[nL]])
        
        for i in range(nL+1,n):
            U[i] -= alpha[i-nL-1]*U[nL]

        nL += 1
        if (nL == n):
            break
    
    for op in operations:
        i = where[op[0]]
        j = where[op[2]]
        L[:, j] += op[1] * L[:, i]

    return P,L,U

B = np.array([
    [1,2,4,5,6],
    [-3,5,0,11,4],
    [1,-41,1.1,-5,.5],
    [-3,-3,-9,99,0],
    [0,13,15,0,13]
],dtype=np.float64)

P,L,U = LU_Decomposition(B)

print(P)
print(L)
print(U)