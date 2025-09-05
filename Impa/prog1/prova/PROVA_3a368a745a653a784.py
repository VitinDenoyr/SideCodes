import math

def my_code():
    return "3a368a745a653a784"

def my_name():
    return "Paulo Vitor Correia de Oliveira"

class Forca:
    def __init__(self, x, y): #Inicializar a força segundo as instruções da classe
        self.x = x
        self.y = y
    def __str__(self): #String no formato especificado, com 2 casas decimais
        return f"[{self.x:.2f}, {self.y:.2f}]"
    def __add__(self, aux): #Soma de 'vetores'
        return Forca((self.x + aux.x),(self.y + aux.y))
    def __sub__(self, aux): #Subtração de 'vetores'
        return Forca((self.x - aux.x),(self.y - aux.y))
    def __mul__(self, esc): #Multiplicação por escalar
        return Forca((self.x * esc),(self.y * esc))
    def __rmul__(self, esc): #Multiplicação do outro lado
        return Forca((esc * self.x),(esc * self.y))
    
class Bloco:
    def __init__(self, p, q, m): #Inicializar o bloco segundo as instruções da classe
        self.p = p
        self.q = q
        self.m = m
    def __str__(self): #String no formato especificado, com 2 casas decimais
        return f"({self.p:.2f}, {self.q:.2f}, {self.m:.2f})"
    def aplica_forca(self, f:Forca): #Metodo que aplica força em cada coordenada do bloco
        self.p = self.p + (f.x*math.log(1 + self.m))
        self.q = self.q + (f.y*math.log(1 + self.m))
    def __imul__(self, f:Forca): #Operador *=, onde ele executa aplica_forca em si mesmo e depois se retorna
        self.aplica_forca(f)
        return self
    def menos(self, aux): #retorna uma força que é calculada de acordo com (2)
        fres1 = (self.p - aux.p)*(1 - math.sin(math.log(1 + self.m + aux.m))) #Formula (2)
        fres2 = (self.q - aux.q)*(1 - math.sin(math.log(1 + self.m + aux.m)))
        return Forca(fres1,fres2)
    def __sub__(self, aux): #Operador - que faz a mesma coisa que menos()
        return self.menos(aux)

def colisao(t1, t2):
    #Calcula a força resultante
    fsum = t1[0] + t2[0] #Soma das forças, dada pelo operador +
    fsub = t1[0] - t2[0] #Subtração das forças, dada pelo operador -
    nfsum = math.sqrt((fsum.x*fsum.x) + (fsum.y*fsum.y)) #Norma da soma das forças
    nfsub = math.sqrt((fsub.x*fsub.x) + (fsub.y*fsub.y)) #Norma da subtração das forças
    fres = math.sqrt(nfsub * nfsum) * (fsum) #Força resultante segundo (3)

    #Calcula o bloco resultante
    brMod = 0.5*(t1[1].m + t2[1].m) #'Modulo' do bloco segundo a formula
    brP = 0.5*(t1[1].p + t2[1].p)*(1 - math.cos(math.sqrt(t1[1].m * t2[1].m))) #Formula (3) de br_i na primeira coordenada
    brQ = 0.5*(t1[1].q + t2[1].q)*(1 - math.cos(math.sqrt(t1[1].m * t2[1].m))) #Formula (3) de br_i na segunda coordenada
    bres = Bloco(brP,brQ,brMod) #Bloco resultante segundo (3)

    #Agora, aplicaremos a força resultante no bloco resultante e retornaremos
    bres *= fres
    return bres

class Campo:
    def __init__(self, blocklist:list): #Inicialização, só coloca a lista no lugar
        self.blocks = blocklist
    def __str__(self): #Converte o campo em uma string
        strconv = "" #String a ser retornada
        for i in range(len(self.blocks)):
            if i > 0: #Vai ter um - antes de cada descrição de bloco, exceto no primeiro
                strconv += " - "
            strconv += str(self.blocks[i]) #E depois o bloco em forma de string
        return strconv
    def caminhada(self, tf):
        for f in tf: #Pra cada força:
            for b in self.blocks: #Pra cada bloco:
                b *= f #Aplica a força no bloco
    def carregue(self, file):
        try:
            with open(file, 'r') as file:
                #Ler arquivo
                forcas = []
                conteudo = file.read().split('\n') #Quebra o arquivo em linhas
                for ln in conteudo:
                    dados = ln.split(' ') #Quebra a linha em informações por espaços
                    if dados[0] == 'Bloco:': #Vai ler um bloco
                        self.blocks.append(Bloco(float(dados[1]),float(dados[2]),float(dados[3])))
                    else: #Vai ler uma força, pois o arquivo só tem blocos e forças
                        forcas.append(Forca(float(dados[1]),float(dados[2])))
                #Após ler tudo, faz a caminhada:
                self.caminhada(forcas)        
        except FileNotFoundError:
            print(f"Arquivo '{file}' não existe.")
        except IOError:
            print(f"Erro ao ler arquivo '{file}'.")