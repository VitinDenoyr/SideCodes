import matplotlib.pyplot as plt
def plot(together = False):
	def p1(x):
		res = 0
		for i,k in enumerate([-512, 2304, -4608, 5376, -4032, 2016, -672, 144, -18, 1]):
			res += k*(x**i)
		return res

	def p2(x):
		return (x - 2)**9

	def graph():
		plt.xlabel('x'); plt.ylabel('y')
		plt.title('Avaliando polinômio')
		plt.grid(); plt.legend()
		plt.show()

	res1 = [p1(x) for x in range(1920,2081)]
	res2 = [p2(x) for x in range(1920,2081)]

	plt.figure(figsize=(6, 6))
	plt.plot(range(1920,2081), res1, 'o', label='Por coeficientes')
	if together:
		plt.plot(range(1920,2081), res2, 'x', label='Por (x-2)^9')
	graph()

	if not together:
		plt.figure(figsize=(6, 6))
		plt.plot(range(1920,2081), res2, 'x', label='Por (x-2)^9')
		graph()
plot(False)