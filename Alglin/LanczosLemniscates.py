#Trefethen-Bau: 36.4
import matplotlib.pyplot as plt
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

def lanczos_leminiscadas(A, max_iter, v0=None):
    n = A.shape[0]
    if v0 is None:
        v0 = np.random.randn(n)
    v0 /= np.linalg.norm(v0)

    alpha = []
    beta = []
    V = np.zeros((n, max_iter + 1))
    V[:, 0] = v0

    w = A @ v0
    a = np.dot(w, v0)
    alpha.append(a)
    w -= a * v0

    tsts = []
    # Iteração nova
    for k in range(1, max_iter + 1):
        b = np.linalg.norm(w)
        beta.append(b)
        if b == 0 or k == max_iter:
            break
        v_new = w / b
        V[:, k] = v_new
        w = A @ v_new
        w -= b * V[:, k - 1]
        a = np.dot(w, v_new)
        alpha.append(a)
        w -= a * v_new

        # Tridiagonal T_k
        T_k = np.diag(alpha[:k]) + np.diag(beta[:k - 1], 1) + np.diag(beta[:k - 1], -1)
        eigs = np.linalg.eigvalsh(T_k)
        tsts.append((k, eigs.copy()))
    return tsts

def plott(tsts):
	plt.figure(figsize=(10, 6))
	for k, eigs in tsts:
		plt.plot(eigs, [k] * len(eigs), 'o', label=f"n = {k}" if k <= 3 else "")
	plt.xlabel("Autovalores de T_k")
	plt.ylabel("Iteração (k)")
	plt.title("Lemniscatas de Lanczos (autovalores de T_k)")
	plt.grid(True)
	plt.tight_layout()
	plt.show()

tests = lanczos_leminiscadas(build_matrix(1000), max_iter=12)
plott(tests)