import matplotlib.pyplot as plt
import scipy.stats as sci
import numpy as np
import math

#Prática
n = 100; p = 0.71; x = sci.bernoulli.rvs(p, size=n)
s = sum(x); a = s + 1; b = n - s + 1
y = sci.beta.rvs(a, b, size=1000)
z = np.log(y/(1 - np.clip(y, 1e-10, 1-1e-10)))

#Teórica
psi = 0; psi_vals = np.linspace(min(z), max(z), 1000)
if(n <= 100):
    #Teórica de forma explícita
    def psii(x):
        return (math.factorial(a+b-1)/(math.factorial(a-1)*math.factorial(b-1))) * (np.exp(x)/(1 + np.exp(x)))**(s+1) * (1/(1+np.exp(x)))**(n-s+1)
    psifunc = np.frompyfunc(psii,1,1)
    psi = psifunc(psi_vals)
else:
    #Outro método para fazer a teórica, para valores grandes de n sem acontecer overflow na gamma
    p_vals = 1/(1 + np.exp(-psi_vals))
    jacobian = np.exp(-psi_vals)/(1 + np.exp(-psi_vals))**2
    psi = sci.beta.pdf(p_vals, a, b) * jacobian

plt.figure(figsize=(10, 6))
plt.hist(z, bins=100, density=True, alpha=0.6, color='skyblue', edgecolor='white', label='Amostras')
plt.plot(psi_vals, psi, 'r-', linewidth=2, label='Distribuição Teórica')
plt.axvline(np.log(p/(1 - p)), color='black', linestyle='--', label=f'psi verdadeiro = {np.log(p/(1 - p)):.3f}')
plt.title('Distribuição de psi = log(p/(1-p))')
plt.xlabel('psi'); plt.ylabel('Densidade'); plt.legend()
plt.grid(alpha=0.2); plt.tight_layout(); plt.show()