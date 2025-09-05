#Problema 1
def search_insert(lis, k):
	l = 0; r = len(lis)-1 #Valores do primeiro e último índice
	if k > lis[r]: return len(lis) #Se o valor for maior que todos os índice, já retorna, caso contrário, busca binária, que é auto explicativa
	while l < r: #Enquanto tiver mais de um elemento no intervalo:
		mid = (l+r)//2 
		if lis[mid] < k: #Verifica se o termo do meio é menor, e se for, sabemos que a posição correta está a direita
			l = mid+1
		else: #caso contrário, então a posição certa deve estar no meio ou a esquerda
			r = mid
	return l #No fim, só sobrará um valor possível para a posição, que será retornado

#Problema 2
#Item A:
def triangulo_pascal(n):
	r = []
	for i in range(n):
		r += [[0]] #Inicializa a i-ésima linha
		if i == 0:
			r[i][0] += 1 #Se for a linha 1, só tem 1 termo
			continue
		else:
			for j in range(i): #Se for outra linha, cada termo da linha anterior contribui na soma de 2 termos na linha nova
				r[i][j] += r[i-1][j]
				r[i] += [r[i-1][j]]
	return r

#Item B:
'''
Para cada uma das N linhas, o algoritmo faz 1 operação de inicializar a i-ésima linha, e para cada elemento
da i-ésima linha, ele o altera no máximo duas vezes, portanto, o algoritmo faz no máximo (1+2+3...+N)*2 =
N*(N+1) operações, e isso é complexidade O(N^2)
'''

#Problema 3
class List_Node:
	def __init__(self, val=0, next=None):
		self.val = val
		self.next = next
#Item A, B, C:
class Linked_List:
	#Cria init como desejado
	def __init__(self, head=None):
		self.length = 1
		self.head = head

	def delete_node(self, val):
		atual = self.head
		prev = None
		#Percorreremos os nós, e se achar um nó com o valor val, realocamos o ponteiro do anterior (caso não seja head)
		while atual != None:
			if atual.val == val:
				if atual is self.head:
					self.head = atual.next
				else:
					prev.next = atual.next
			#Segue o while para percorrer a lista
			prev = atual
			atual = atual.next

	def __add__(self, sec):
		#Cria uma nova lista vazia
		novaLista = Linked_List()
		atual = self.head
		prev = None
		nodo = None
		#Se a lista inicial for vazia, o while não executa e então a lista nova continua vazia por enquanto
		while atual != None:
			if novaLista.head == None: #Se a lista nova ainda não tem head, torne o primeiro nodo a head
				novaLista.head = List_Node(atual.val,atual.next)
				nodo = novaLista.head
			else:
				#Atualiza quem é o último nodo
				prev = nodo
				nodo = List_Node(atual.val) #Aqui, temos nodo apontando para o último nodo criado
				#Se não for a head, então o anterior tem que apontar pra ele também
				prev.next = nodo
			atual = atual.next #Percorre a lista
		#Percorreremos a segunda lista e faremos o procedimento de concanetação igual ao caso "else" anterior
		atual = sec.head
		while atual != None:
			prev = nodo
			nodo = List_Node(atual.val)
			prev.next = nodo
			atual = atual.next
		return novaLista
	
#Problema 4
#Definindo a função deixarNoggers que transforma uma string em forma de polinômio em sua versão de dicionário
def deixarNoggers(poli):
	lim = len(poli)
	poli += '.' #Marca o final da string
	pos = 0 #Posição do caractere a ser lido
	posType = 0 #Tipo do caractere a ser lido, entre 0 = coeficiente, 1 = letra x, 2 = expoente, 4 = adição/subtração
	sinal = 1
	coef = "" #Guardará o numero completo do coeficiente
	exp = "" #Guardará o numero completo do expoente
	dick = {} #Dicionário resposta
	while(pos <= lim):
		ch = poli[pos]
		if ch == 'x':
			if coef == "":
				coef += "1"
			posType = 1 #Informa que acabou de ler o x, portanto, assume-se que já tem o coeficiente
		elif ch.isdigit() == True and posType == 0:
			coef += ch #Sabemos que ainda está informando o coeficiente
		elif ch == '^':
			posType = 2 #Agora será lido o expoente
		elif ch.isdigit() == True and posType == 2:
			exp += ch #Ainda está informando o expoente
		elif ch == '+' or ch == '-' or ch == '.': #Encerrou algum termo da lista ou o primeiro termo é negativo
			if pos == 0:
				sinal = 2*(ch == '+') - 1 #Detecta se foi + ou - como primeiro caractere
			else:
				if posType == 1: #Não teve ^k, logo, é ^1
					exp += '1'
				elif posType == 0: #Não teve x, logo é ^0
					exp += '0'
				iexp = eval(exp)
				icoef = eval(coef)
				dick[iexp] = sinal * icoef #Marca o dicionário
				if ch == '+': #Marca o sinal
					sinal = 1
				elif ch == '-':
					sinal = -1

				#Zera tudo
				exp = ""
				coef = ""
				posType = 0
		pos += 1
	return dick

#Problema 5
#Definindo a função deixarPoggers que transforma um dicionário em uma string de polinômio
def deixarPoggers(dick):
	sortList = sorted(dick.keys(),reverse=True) #Ordem certa dos expoentes
	stri = ""
	for i in sortList:
		if i != sortList[0] and dick.get(i) >= 0: #Se precisar colocar o mais
				stri += '+'
		if (dick.get(i) == 0 and i != 0) or not (i == 1 and dick.get(i) == 1): #Se precisar colocar o coeficiente, não precisa em 0x^2 ou em 1x
			if dick.get(i) != -1: #Caso -1 a parte, pra ficar -x e não -1x
				stri += str(dick.get(i))
			else:
				stri += '-'
		if i > 0: #Não coloca o x se for constante
			stri += 'x'
		if i != 1 and i != 0: #Só coloca o expoente se for >= 2 ou < 0
			stri += '^'
			stri += str(i)
	return stri