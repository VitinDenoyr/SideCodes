#Trefethen-Bau: 36.4
import numpy as np

# Matriz doida do enunciado
def build_matrix(n = 1000):
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = np.sqrt(i + 1)
        if i < n - 1:
            A[i, i + 1] = A[i + 1, i] = 1  # +- 1 Diag
        if i < n - 100:
            A[i, i + 100] = A[i + 100, i] = 1  # +- 100 Diag
    return A

def lanczos(A, m, v0=None):
    
    #Toma v0 != 0
    n = A.shape[0]
    while v0 is None or np.allclose(v0,0):
        v0 = np.random.randn(n)
    
    #Normaliza + defs
    v0 = v0 / np.linalg.norm(v0)
    V = np.zeros((n, m))
    alpha = np.zeros(m)
    beta = np.zeros(m - 1)

    V[:, 0] = v0
    w = A @ V[:, 0]
    alpha[0] = V[:, 0].dot(w)
    w = w - alpha[0] * V[:, 0]

	# Iteracao
    for j in range(1, m):
        beta[j - 1] = np.linalg.norm(w)
        if beta[j - 1] == 0:
            break
        V[:, j] = w / beta[j - 1]
        w = A @ V[:, j]
        w = w - beta[j - 1] * V[:, j - 1]
        alpha[j] = V[:, j].dot(w)
        w = w - alpha[j] * V[:, j]

    T = np.diag(alpha) + np.diag(beta, k=1) + np.diag(beta, k=-1)
    return T, V

# Numero de passos (o suficiente pra convergir bem, acho que 100 da)
steps = 100
T, V = lanczos(build_matrix(1000), steps)

# Autovalor estimado:
print(f'O menor autovalor é: {np.min(np.linalg.eigvalsh(T)):.6f}')