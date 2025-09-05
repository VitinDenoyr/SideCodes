#Problema 5:
import collections
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
	ranks = [str(n) for n in range(2, 11)] + list('JQKA')
	suits = 'spades diamonds clubs hearts'.split()
 
	def __init__(self):
		self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

	def __len__(self):
		return len(self._cards)

	def __getitem__(self, position):
		return self._cards[position]

	def __setitem__(self, index, value):
		self._cards[index] = value

myDeck = FrenchDeck()
random.shuffle(myDeck) #não estava embaralhando as cartas, então implementei setitem
print(myDeck[1]) #Troca de ordem das linhas 21 e 22: erro de lógica