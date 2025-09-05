# Problema 1:
# Imagine que você está subindo uma escada. São necessários n degraus
# para chegar ao topo. A cada vez, você pode subir 1 ou 2 degraus. Escreva
# um programa que retorne quantas maneiras distintas existem para subir
# ao topo dado um número natural n

#Com memória auxiliar fora da função:
'''
memo = [1,1]
def contaManeiras(n: int):
    if n < len(memo): return memo[n]
    memo.append(contaManeiras(n-1) + contaManeiras(n-2))
    return memo[n]
'''

#Sem memória auxiliar:
'''
def contaManeiras(n: int):
	if n < 2: return 1
	return contaManeiras(n-1) + contaManeiras(n-2)
'''

#Com memória auxiliar mas apenas dentro da função:
#'''
def contaManeiras(n: int):
	memo = [1,1]
	for i in range(2,n+1):
		memo.append(memo[i-1] + memo[i-2])
	return memo[n]
#'''

#Alguns Testes
#'''
print(contaManeiras( 1 ))  # Esperado: 1
print(contaManeiras( 2 ))  # Esperado: 2
print(contaManeiras( 5 ))  # Esperado: 8
print(contaManeiras( 10 )) # Esperado: 89
print(contaManeiras( 20 )) # Esperado: 10946
print(contaManeiras( 35 )) # Esperado: 14930352
#'''