from polygons import csv, turtle, time, Point2D, Polygon, Polygons

# Problema 1
def juntaListas(lista1, lista2): # Função de fundir duas listas
    tamanho1 = len(lista1)
    tamanho2 = len(lista2)
    indice1 = 0 # Índice na lista1
    indice2 = 0 # Índice na lista2
    lista3 = [] # Lista resultante
    while(indice1 < tamanho1 and indice2 < tamanho2): # Primeiro, verifica o primeiro não adicionado de cada lista, que é o maior
        if lista1[indice1] >= lista2[indice2]: # Insere o maior na lista e move o ponteiro dessa lista para a frente
            lista3.append(lista1[indice1])
            indice1 += 1
        else: # Faz o mesmo com lista2
            lista3.append(lista2[indice2])
            indice2 += 1
    while(indice1 < tamanho1): # Se chegou aqui, uma lista já acabou. Se ela for lista2, isso vai executar e completar com lista1
        lista3.append(lista1[indice1])
        indice1 += 1
    while(indice2 < tamanho2): # Caso lista1 que acabou, então completa com lista2
        lista3.append(lista2[indice2])
        indice2 += 1
    # Agora garantimos que as duas listas já acabaram.
    # Cada termo foi adicionado só uma vez e faz quantidade constante de algumas operações em relação a cada um dos n termos de uma lista e dos m termos de outras, entao o código é O(n+m), proporcional ao total de termos
    return lista3
print(juntaListas([13,5,1],[14,7,6,2,0]))


# Problema 2
def problemaDasCompras(n:int, k:int, itens:list):
    maiornum = max(item for item in itens)+1
    qtd = [0]*maiornum # Array que marca quantas vezes comprei o item i nas últimas k compras
    fila = [] # fila que vai guardar os tipos dos ultimos k itens
    total = 0
    for i in range(n):
        if qtd[itens[i]] == 0: # Posso adicionar pois não há esse item nos anteriores
            qtd[itens[i]] += 1 # Há um item a mais
            fila = [itens[i]] + fila # Adiciona na fila com o número dos k itens em ordem
            total += 1 # Total de itens comprados aumenta
            if len(fila) > k: # Caso existam mais de k itens anteriores nessa iteração, desconsidere o item há k+1 iterações atras na quantidade
                ultimo = fila.pop()
                qtd[ultimo] -= 1
    return total
print(problemaDasCompras(5,3,[1,2,5,1,1]))

# Problema 3
def problemaDosParenteses(string:str):
    qtAbertos = 0 # Quantos parênteses estão abertos
    for caractere in string:
        if caractere == '(':
            qtAbertos += 1 # Tem mais um parêntese aberto
        elif caractere == ')':
            qtAbertos -= 1 # Foi fechado um parêntese
        if qtAbertos < 0: # Se tem mais fechados que abertos, não é válida
            return False
    return qtAbertos == 0 # Se depois de passar por todos os caracteres, não tiver nenhum parêntese aberto, é válida
print(problemaDosParenteses('(())()()()()()()()((()))((()()))'))

# Problema 4 e Problema 5
# Script
def funcaoArvore():
    poligonos = [
        # Tronco da árvore
        Polygon([
            Point2D(-0.1, 0), Point2D(-0.1, -0.5), Point2D(0.1, -0.5), Point2D(0.1, 0)
        ], 'brown'),

        # Copas da árvore
        Polygon([
            Point2D(-0.5, 0), Point2D(0.5, 0), Point2D(0, 1)
        ], 'green'),
        Polygon([
            Point2D(-0.4, 0.5), Point2D(0.4, 0.5), Point2D(0, 1.5)
        ], 'green'),
        Polygon([
            Point2D(-0.3, 1), Point2D(0.3, 1), Point2D(0, 2)
        ], 'green'),
    ]

    poligonos_obj = Polygons()
    for indice, poligono in enumerate(poligonos):
        poligonos_obj.addPolygon(poligono, f"x{indice + 1}")  # Adiciona os polígonos com nomes x1 ... xn

    poligonos_obj.plotPoints()  # Executa plot points
funcaoArvore()
