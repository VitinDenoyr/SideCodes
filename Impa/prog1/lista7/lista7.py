import csv
import turtle
from vector3d import Vector3D as V3D
#--------------------------------------------------------------------------------------

#Problema 1
def f(x): #Função pedida
	return ((x**8) - 3*(x**4) + 2*(x**3) - 2*(x**2) - (x) + 2)

def gerarPontos(func, qtd, inter, file): #Chame gerarPontos(f,1000,[-1.5,1.5],'arq.csv') para resolver o exercício
	with open(file, 'w', newline='') as csvf: #Abre o arquivo e impede linhas vazias sendo imprimidas
		csvWrite = csv.writer(csvf) #Abre o writer
		adder = (inter[1]-inter[0])/qtd #Adiciona um valor padrão a cada próximo ponto para gerar 1000 pontos igualmente espaçados
		res = [] #Array de pontos
		for i in range(qtd):
			xi = inter[0] + i*adder
			res += [[xi,func(xi)]]
		csvWrite.writerows(res)
'''gerarPontos(f,1000,[-1.5,1.5],'arq.csv')'''

def criaGrafico(file):
	with open(file, 'r') as csvf: #Abre o arquivo
		pts = [] #Guarda os pontos
		csvRead = csv.reader(csvf)
		for l in csvRead: #Lê os pontos do arquivo e leva para a lista pts. Assume que estão no formato correto (função anterior)
			pts.append([float(l[0]), float(l[1])])

		minX = min(pts, key=lambda p: p[0])[0] #Menores e máximos valores de cada função
		maxX = max(pts, key=lambda p: p[0])[0] #Aprendi oq era essa função lambda pq fazer if else era feio :(
		minY = min(pts, key=lambda p: p[1])[1]
		maxY = max(pts, key=lambda p: p[1])[1]
		
		#Inicializaremos o turtle
		scr = turtle.Screen()
		scr.setworldcoordinates(minX, minY, maxX, maxY) #Deixa o tamanho da tela mais próximo para visualizar o gráfico
		scr.colormode(255) #Usar rgb
		scr.bgcolor((0,0,0)) #Cor de fundo
		tr = turtle.Turtle() #Cria a tortuguita

		#Move o turtle para o ponto inicial e ajusta velocidade, grossura do gráfico e cor dele
		tr.penup()
		tr.goto(pts[0][0],pts[0][1])
		tr.pendown()
		tr.pencolor((255,0,255))
		tr.pensize(3)
		tr.speed(0)
		#Insere todos os pontos
		for p in pts:
			tr.goto(p)
		scr.exitonclick()
'''criaGrafico('arq.csv')'''

#--------------------------------------------------------------------------------------

#Problema 2
def merge_intervals(interList):
	interList = sorted(interList) #Ordenação: NlogN. Não me preocuparei com complexidade visto que não foi pedido nesse problema
	trueList = []
	ant = [-1,-1] #Guarda o termo anterior na ordenação
	for it in interList:
		if ant[1] < it[0]: #Significa que o anterior acaba antes mesmo de começar, não há interseção
			trueList += [it] #Só adiciona na lista normalmente
		else: #Há interseção com o anterior
			tlast = trueList[len(trueList)-1]
			trueList[len(trueList)-1] = [tlast[0],max(tlast[1],it[1])] #O início da junção vai ser o início do anterior, pois está ordenado. Já no final, basta olhar quem acaba depois 
		ant = it #Atualiza o anterior
	return trueList
'''print(merge_intervals([[17,20],[1,2],[3,4],[6,6],[15,19],[3,6],[1,1]]))'''

#--------------------------------------------------------------------------------------

#Problema 3
def missing_int(lista):
	realoc = lista[0] #Consideremos uma realocação de valores: se o primeiro valor vale i e está na posição 0, uma lista está contínua se v-i está na posição v-i. Caso contrário, tem alguém faltando lá atras. O(1)
	l = 0; r = len(lista)-1 #Posições possíveis de fazer a busca. Uma busca binária tem complexidade O(logn)
	while(l < r):
		mid = (l+r)//2
		if	lista[mid]-realoc == mid:
			l = mid+1
		else:
			r = mid
	#Aqui, l == r. Se mesmo assim v-i estiver na posição i, a lista inteira estava sem ninguem faltando O(1)
	if	lista[l]-realoc == l:
		return (lista[len(lista)-1] + 1)
	return lista[l-1]+1 #Caso contrário, como l tem posição errada, falta alguém entre ele e o anterior
	#Complexidade total: O(1) + O(logn) + O(1) = O(logn)
'''print(missing_int([4,5,6,7,8,9,10,11,12,13,15,17,19,25]))'''

#--------------------------------------------------------------------------------------

#Problema 4
#Lista ligada como no exercício 3 da lista 6, visto que o exercício deixa usar
#Reutilizei o método add só para não ter trabalho ao criar exemplos para testar
class List_Node:
	def __init__(self, val=0, next=None):
		self.val = val
		self.next = next

class Linked_List:
	def __init__(self, head=None):
		self.length = 1
		if head==None:
			self.length = 0
		self.head = head
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
		novaLista.length = self.length + sec.length
		return novaLista

def is_palindrome(atual:List_Node):
	ls = [] #Onde os valores serão guardados para comparar

	while(atual != None): #Percorre a lista ligada e transforma em uma lista normal
		ls += [atual.val] #Adiciona esse elemento em ls
		atual = atual.next

	for i in range(len(ls)//2,len(ls)):
		if ls[i] != ls[len(ls)-1-i]: #A partir da metade, ê se esse termo tem o mesmo valor do espelhado correspondente, se não tiver, não é palindromo
			return False 
	return True #Não deu nenhum termo não-correspondente, logo é palindromo

def el(v): #Cria uma lista ligada de um elemento de valor v
	return Linked_List(List_Node(v))
'''
print(is_palindrome((el(3)+el(1)+el(3.14)+el(3.14)+el(1)+el(3)).head))
print(is_palindrome((el(3)+el(7)+el(7)+el(3)+el(2)).head))
print(is_palindrome((el(0)).head))
print(is_palindrome((el(3)+el(1)+el(4)+el(1)+el(5)).head))
print(is_palindrome((el(135135)+el(135136)+el(135135)).head))
'''
			
#--------------------------------------------------------------------------------------

#Problema 5
#Script de utilização - Como não foi especificado o que deveria ser feito, fiz algo bem simples
def piaFio(a:V3D, o:V3D): #Define 2 vetores 3D {a, o} e imprime o resultado de retorna pi * a + phi * o 
	piAprox = 3.141
	phiAprox = 1.618
	resp = (piAprox*a) + (phiAprox*o)
	print(resp)
piaFio(V3D([1,10,100]),V3D([1,2,3]))