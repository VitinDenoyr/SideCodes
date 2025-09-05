#Problema 1
class node:
	def __init__(self, val, next = None):
		self.value = val
		self.next = next
	
class linkedlist:
	#Método de inicializar uma lista ligada. É possível atribuir um nodo inicial como head
	def __init__(self,head = None):
		self.head = head
		self.last = self.head

	#Adiciona um nodo no fim da lista e o torna o novo fim da lista
	def addNode(self, value):
		newnode = node(value, None)
		if self.head == None:
			self.head = newnode
			self.last = newnode
		else:
			self.last.next = newnode
			self.last = newnode
	
	#Método que criei para imprimir a lista. Majoritariamente para debug
	def printlist(self):
		path = self.head
		if path == None:
			print("[]")
			return
		while path.next != None:
			print(f"[{path.value}] -> ",end="")
			path = path.next
		print(f"[{path.value}]")

	#Método de inverter ordem como requerido no enunciado. Retorna uma lista ligada com a ordem inversa da original
	def inverte_ordem(self):
		path = self.head
		nova = linkedlist()

		#Se a lista for vazia, sua inversa também é vazia
		if path == None:
			return nova

		#Se não for vazia, então cria o primeiro nó que como era o inicial da antiga, será o final da outra
		#Incialmente, também será o início da outra
		nova.last = node(path.value)
		nova.head = nova.last

		#Enquanto houver um próximo nó, faz ele se conectar a head atual e se tornar a nova head
		while path.next != None:
			novonode = node(path.next.value)
			novonode.next = nova.head
			nova.head = novonode
			path = path.next
		
		return nova
	#No enunciado diz que o inverte_ordem deve ser um método, mas também diz que deve receber uma lista como parâmetro. Como devemos inverter a ordem de uma só lista, ficaria ambíguo qual lista inverter caso A e B fossem listas e eu chamasse A.inverte_ordem(B), visto que isso deve retornar a lista nova. Então, eu fiz assumindo que não recebe lista como parâmetro, mas A.inverte_ordem() retorna A em ordem inversa
	#Sabemos que as primeiras linhas são apenas poucas operações que independem do tamanho da lista, feitas em O(1), enquanto o laço de repetição while percorre todos os nós da lista uma única fez e faz uma quantidade fixa de operações em cada, sendo isso de complexidade O(n). Portanto, a complexidade desse método é O(n).

#-------------------------------------------------------------------------------------------------------------------

#Problema 2
def para_romanos(n:int):
	#Listas de conversão: num[i] em base 10 -> conv[i] em romano
	num = [1000,500,100,50,10,5,1,0]
	conv = ['M','D','C','L','X','V','I']
	res = "" #String resposta do número romano
	ind = 0 #Índice de num e conv sendo comparado no momento
	while(n > 0):
		correspInd = ind+1+((ind+1)%2)
		if n >= num[ind]: #Neste caso, basta adicionar o número normalmente e continuar com o restante
			res += conv[ind]
			n -= num[ind]
		elif n >= num[ind] - num[correspInd]: #Caso for menor que o número mas exista como fazer uma subtração com outro número
			res += conv[correspInd] + conv[ind]
			n -= (num[ind] - num[correspInd])
		else: #Não há mais nada para fazer com esse dígito
			ind += 1
	return res
#-------------------------------------------------------------------------------------------------------------------

#Problema 3
#Primeiro será feito a implementação em O(n), que é a mais intuitiva
def potencia_n(x:float, n:int):
	ans = 1
	neg = 0
	if(n < 0):
		neg = 1
		n *= -1
	#Ela consiste em tomar ans = 1 e multiplicar por x exatamente n vezes
	for i in range(n):
		ans *= x
	if(neg):
		return 1/ans
	return ans
#Agora a implementação em O(logn)
def potencia_logn(x:float, n:int):
	ans = 1
	neg = 0
	if(n < 0):
		neg = 1
		n *= -1
	#Toma-se ans = 1. Considera-se a representação binária do expoente.
	while n > 0:
		#Enquanto o expoente existir, se ele for ímpar, multiplicaremos a resposta pela base uma vez e subtrairemos 1 do valor dele. Ou seja, antes faltava x^n para ser atribuido a ans, agora falta x^(n-1), visto que já foi multiplicado por x uma vez.
		if n%2==1:
			ans *= x
			n -= 1
		#Se for par, note que falta x^(2k) de expoente para ser multiplicado em ans. Isso equivale a multiplicar (x^2)^k, portanto, para facilitar nosso processo, tornaremos a base x^2 e o expoente como metade
		else:
			x *= x
			n /= 2
		#Note que a operação ímpar muda o último bit do expoente de 1 para 0 e a operação par apaga o bit. Como n possui log2(n) bits e podemos fazer no máximo 2 operações em cada bit, nosso algoritmo fará no máximo 2*log2(n) operações de alterar o bit e com isso, o código possui complexidade O(logn) visto que as operações dentro de cada if são feitas com complexidade constante O(1)
	if(neg):
		return 1/ans
	return ans

#-------------------------------------------------------------------------------------------------------------------

#Problema 4
def ache_o_sozinho(lista:list):
	res = 0 #Res guardará o número sozinho
	for elm in lista:
		res ^= elm #Operador bitwise xor. Ele resolve o problema por algumas propriedades:
		#1) Comutatividade: A^B == B^A e associatividade: (A^B)^C == A^(B^C). Ambas são claras pela sua definição.
		#2) A^A = 0, pois todos os bits são iguais, e A^0 = A, pois só os 1's são copiados nas mesmas posições.
		
		#Dadas essas propriedades, o xor resultante de todos os elementos da lista é equivalente ao xor de todos os elementos da lista quando ordenados de modo que os números iguais fiquem lado a lado. Fazendo isso, fica visível que os números iguais terão xor 0, e o xor resultante será uma longa sequência de 0^0^...^0^X, onde X é o número que não tem par. Isso mostra que o xor resultante será de fato o número X, encerrando o problema.
		
		#Não sei se podia usar esse operador, mas assumi que sim visto que estava ao menos já citado em um slide anterior de uma aula. Poderia ter feito também com uma lista que marca as ocorrências e depois iterar sobre ela, mas achei esse método mais bonitinho :)
	return res

#-------------------------------------------------------------------------------------------------------------------

#Problema 5
def longest_common_prefix(lista:list):
	#Primeiro, tira da lista a última palavra e guarda em comp e guarda em lim o tamanho dela. Lim é o tamanho máximo do prefixo, visto que ele também deve pertencer a última palavra
	lim = len(lista[len(lista)-1])
	comp = lista.pop()
	#Agora, para toda outra palavra na lista:
	for s in lista:
		#Verifica se os primeiros lim caracteres batem. Se em algum momento perceber que a palavra é menor que o limite atual ou tiver um caractere diferente, então já diminua o tamanho do prefixo visto que ele não tem como ser comum a essas duas palavras. Esse processo é repetido para todas as palavras
		for i in range(lim):
			if i >= len(s) or s[i] != comp[i]:
				lim = i
				break
		#No fim, garante-se que os primeiros lim caracteres são comuns a todos os membros da lista, e então, os retorna já que são parte de comp
	return comp[:lim]