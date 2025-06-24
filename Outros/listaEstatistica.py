import numpy as np
from scipy.stats import randint as Unif

# Inicializa os arrays amostrais
X = np.array([3.85, 3.88, 1.46, 3.74, 3.69, 1.19, 3.06, 1.13, 1.11, 2.24, 4.00, 1.99, 2.40, 2.04, 1.31])
Y = np.array([4.95, 6.63, 4.65, 6.03, 5.26, 3.71, 6.06, 5.19, 3.37, 3.71])

# Mediana usando Numpy
print(f'Mediana de X: {np.percentile(X,50)}') # 2.24
print(f'Mediana de Y: {np.percentile(Y,50)}') # 5.07

def Bootstrap(V, B):
    #Faz o resampling
	resample = [V[Unif.rvs(low=0,high=len(V),size=len(V))] for i in range(B)]
 
	#Calcula as medianas
	meds = [np.percentile(w,50) for w in resample]
 
	#Calcula o estimador
	est = np.average(meds)
 
	#Calcula a variancia
	var = np.sum([(z - est)**2 for z in meds])/B
 
	#Retorna o estimador da mediana com seu desvio padrão
	return [est, np.sqrt(var), meds]
	
print(Bootstrap(X,5000)[:2]) #Saida: [2.34, 0.58]
print(Bootstrap(Y,5000)[:2]) #Saida: [4.99, 0.49]

#Ordena e descarta as entradas desnecessarias
arrx = sorted(Bootstrap(X,5000)[2])[250:4750]
arry = sorted(Bootstrap(Y,5000)[2])[250:4750]
intervx = [arrx[0], arrx[-1]]
intervy = [arry[0], arry[-1]]
print(intervx) #Saida: [1.46, 3.69]
print(intervy) #Saida: [4.18, 5.66]