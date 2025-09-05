# python 3.10

class Field:
    pass

class VectorSpace:
    """VectorSpace:
    Abstract Class of vector space used to model basic linear structures
    """
    
    def __init__(self, dim: int, field: 'Field'):
        """
        Initialize a VectorSpace instance.
        Args:
            dim (int): Dimension of the vector space.
            field (Field): The field over which the vector space is defined.
        """
        self.dim = dim
        self._field = field
        
    def getField(self):
        """
        Get the field associated with this vector space.
        Returns:
            Field: The field associated with the vector space.
        """
        return self._field
    
    def getVectorSpace(self):
        """
        Get a string representation of the vector space.
        Returns:
            str: A string representing the vector space.
        """
        return f'dim = {self.dim!r}, field = {self._field!r}'
        # return self.__repr__()

    def __repr__(self):
        """
        Get a string representation of the VectorSpace instance.
        Returns:
            str: A string representing the VectorSpace instance.
        """
        # return f'dim = {self.dim!r}, field = {self._field!r}'
        return self.getVectorSpace()
    
    def __mul__(self, f):
        """
        Multiplication operation on the vector space (not implemented).
        Args:
            f: The factor for multiplication.
        Raises:
            NotImplementedError: This method is meant to be overridden by subclasses.
        """
        raise NotImplementedError
    
    def __rmul__(self, f):
        """
        Right multiplication operation on the vector space (not implemented).
        Args:
            f: The factor for multiplication.
        Returns:
            The result of multiplication.
        Note:
            This method is defined in terms of __mul__.
        """
        return self.__mul__(f)
    
    def __add__(self, v):
        """
        Addition operation on the vector space (not implemented).
        Args:
            v: The vector to be added.
        Raises:
            NotImplementedError: This method is meant to be overridden by subclasses.
        """
        raise NotImplementedError
    
class Polynomial(VectorSpace):
	@staticmethod
	#Dada uma string da forma ax^b + cx^d - ex^f (...) + gx + h, onde cada termo é separado por um + ou -
	#e os termos são da forma {ax^b, ax, x^b, x}, dependendo do grau ou coeficiente.
	def stringToPolynomial(string:str, variable:str = 'x'):
		poly = {}
		if string == '': return poly
		string = str.replace(string,'-','+-')
		string = string.split('+') #Trata os sinais de - como um elemento do coeficiente
		for t in string:
			if variable in t: #caso contrário é o termo independente
				if t.index(variable) == 0: #coeficiente 1
					t = '1' + t
				elif t.index(variable) == 1 and t[0] == '-': #coeficiente -1
					t = '-1' + t[1:]
     
				if '^' in t: #coeficiente presente e expoente tambem
					poly[int(t[-1])] = float(t[:t.index(variable)])
				else: #termo de grau 1
					poly[1] = float(t[:-1])
			else: #termo de grau 0
				poly[0] = float(t)
		return poly
    
	def __init__(self, poly):
		self.coef = {}
		if type(poly) == type(''): #Se iniciou com string, executa a função de strings
			self.coef = self.stringToPolynomial(poly)
		elif type(poly) == type([]): #caso contrário, apenas passa os dados da lista para o dicionário
			for t in poly: #Assume-se uma lista de pares de elementos
				self.coef[t[0]] = t[1]
		else: #entrada inválida
			raise ValueError

	def __repr__(self): #Converte do dicionário para a string sob a mesma lógica
		res = ''
		first = True
		for key,val in sorted(self.coef.items(),reverse=True):
			if val < 0:
				val *= -1
				res += '-'
				first = False
			elif not first:
				res += '+'
			else:
				first = False

			if val*val == 1:
				nval = ''
				if val == -1: nval += '-'
				if key == 0:
					res += f'{int(val)}'
				elif key == 1:
					res += f'{nval}x'
				else:
					res += f'{nval}x^{key}'
			else:
				if abs(val - int(val)) < .1: val = int(val)
				if key == 0:
					res += f'{val}'
				elif key == 1:
					res += f'{val}x'
				else:
					res += f'{val}x^{key}'
   
		return res

	def __add__(self, other:'Polynomial'): #Adição de polinomios
		newp = Polynomial('')
		for key,val in other.coef.items():
			if key not in newp.coef.keys():
				newp.coef[key] = 0
			newp.coef[key] += val
		for key,val in self.coef.items():
			if key not in newp.coef.keys():
				newp.coef[key] = 0
			newp.coef[key] += val
		return newp

	def __neg__(self): #Negação do vetor: trocar o sinal de seus coeficientes
		newp = Polynomial('')
		for key,val in self.coef.items():
			newp.coef[key] = -val
		return newp
	
	def __sub__(self, other:'Polynomial'): #Subtração: Adição com a negação do outro vetor
		return self+(-other)

	def __mul__(self, alfa:float): #Multiplicação por escalar: P*alfa
		newp = Polynomial('')
		for key,val in self.coef.items():
			newp.coef[key] = val*alfa
		return newp