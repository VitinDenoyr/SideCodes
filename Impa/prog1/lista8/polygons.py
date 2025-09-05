import csv
import time
import turtle

class Point2D:  # Classe do ponto
    def __init__(self, coordX: float, coordY: float):
        self.coord = [coordX, coordY]

class Polygon:  # Classe do polígono
    def __init__(self, listaDePontos: list, cor: str):
        self.points = listaDePontos.copy()
        self.color = cor

class Polygons:  # Classe para guardar vários polígonos
    def __init__(self):
        self.polygons = []

    def removePolygon(self, nome: str):
        self.polygons = [dupla for dupla in self.polygons if dupla[0] != nome]

    def addPolygon(self, novoPoligono: Polygon, nome: str):
        self.polygons.append([nome, novoPoligono])

    def save_to_file(self, filename: str):
        with open(filename, 'w', newline='') as arquivoCsv:  # Abre o CSV
            writerCsv = csv.writer(arquivoCsv)  # Abre o writer
            for poligono in self.polygons:  # Coloca na linha primeiro a cor depois os pontos
                linha = [poligono[0], poligono[1].color]
                for ponto in poligono[1].points:
                    linha += [ponto.coord[0], ponto.coord[1]]
                writerCsv.writerow(linha)

    def load_from_file(self, filename: str):
        with open(filename, 'r') as arquivoCsv:  # Abre o arquivo CSV
            readerCsv = csv.reader(arquivoCsv)  # Abre o reader
            self.polygons.clear()  # Limpa os polígonos velhos porque vai carregar
            for linha in readerCsv:
                nome, cor = linha[0], linha[1]
                pontosPoligono = []
                for i in range(2, len(linha), 2):  # Pega as coordenadas que estão na linha
                    x, y = float(linha[i]), float(linha[i + 1])
                    pontosPoligono.append(Point2D(x, y))
                self.polygons.append([nome, Polygon(pontosPoligono, cor)])  # Adiciona um polígono dessa linha

    def plotPoints(self):
        # Criar tela no tamanho certo
        minimoX, minimoY, maximoX, maximoY = float('inf'), float('inf'), float('-inf'), float('-inf')
        for _, poligono in self.polygons:
            minimoX = min(minimoX, min(p.coord[0] for p in poligono.points))
            minimoY = min(minimoY, min(p.coord[1] for p in poligono.points))
            maximoX = max(maximoX, max(p.coord[0] for p in poligono.points))
            maximoY = max(maximoY, max(p.coord[1] for p in poligono.points))

        # Configurações padrão: criar tela, colocar fundo e definir o tamanho
        tela = turtle.Screen()  # Cria tela
        margem_x = (maximoX - minimoX) / 5
        margem_y = (maximoY - minimoY) / 5
        tela.setworldcoordinates(minimoX - margem_x, minimoY - margem_y, maximoX + margem_x, maximoY + margem_y)

        tartarugas = []  # Guarda todos os ponteiros, um para cada polígono para padronizar
        for _ in range(len(self.polygons)):
            tartarugas.append(turtle.Turtle())  # Criando tartaruga

        for i, tartaruga in enumerate(tartarugas):
            poligono = self.polygons[i][1]  # i-ésimo polígono
            ultimo_ponto = poligono.points[-1].coord
            tartaruga.hideturtle()  # Esconde o ponteiro da tartaruga
            tartaruga.pencolor(poligono.color)  # Define a cor
            tartaruga.pensize(3)  # Define a espessura do traço
            tartaruga.speed(0)  # Define a velocidade do desenho
            tartaruga.penup()
            tartaruga.goto(ultimo_ponto[0], ultimo_ponto[1])  # Move para o ponto inicial, que é o último ponto
            tartaruga.pendown()
            for ponto in poligono.points:
                tartaruga.goto(ponto.coord[0], ponto.coord[1])  # Move para o próximo ponto

        time.sleep(4)
        tela.clearscreen()

# Testes para ver se funciona: cria quatro quadrados

print("Criando uma peça composta por 4 quadrados de 1x1 que formam um quadrado de 2x2...")

# Criando os quadrados com diferentes cores

quadrado1 = Polygon([Point2D(-50, 50), Point2D(-50, 0), Point2D(0, 0), Point2D(0, 50)], "blue")
quadrado2 = Polygon([Point2D(0, 50), Point2D(0, 0), Point2D(50, 0), Point2D(50, 50)], "red")
quadrado3 = Polygon([Point2D(-50, 0), Point2D(-50, -50), Point2D(0, -50), Point2D(0, 0)], "green")
quadrado4 = Polygon([Point2D(0, 0), Point2D(0, -50), Point2D(50, -50), Point2D(50, 0)], "yellow")

p = Polygons()

p.addPolygon(quadrado1, "quadrado1")
p.addPolygon(quadrado2, "quadrado2")
p.addPolygon(quadrado3, "quadrado3")
p.addPolygon(quadrado4, "quadrado4")

p.save_to_file("peca_2x2.csv")
p.load_from_file("peca_2x2.csv")

p.plotPoints()
