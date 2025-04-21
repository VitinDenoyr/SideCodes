board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
player = ['X','O']; playerId = 0; turns = 0

def printBoard():
	print("+-----------+")
	print(f"| {board[0][0]} | {board[0][1]} | {board[0][2]} |")
	print("+---+---+---+")
	print(f"| {board[1][0]} | {board[1][1]} | {board[1][2]} |")
	print("+---+---+---+")
	print(f"| {board[2][0]} | {board[2][1]} | {board[2][2]} |")
	print("+-----------+\n")

def verifyWin():
	for i in range(3):
		if (board[i][0]+board[i][1]+board[i][2] == "XXX"):
			return 1
		if (board[i][0]+board[i][1]+board[i][2] == "OOO"):
			return 2
		if (board[0][i]+board[1][i]+board[2][i] == "XXX"):
			return 1
		if (board[0][i]+board[1][i]+board[2][i] == "OOO"):
			return 2
	if board[0][0]+board[1][1]+board[2][2] == "XXX":
		return 1
	if board[0][0]+board[1][1]+board[2][2] == "OOO":
		return 2
	if board[2][0]+board[1][1]+board[0][2] == "XXX":
		return 1
	if board[2][0]+board[1][1]+board[0][2] == "OOO":
		return 2
	return 0

while True:
	printBoard()
	l = input("Digite a linha a ser jogada: ")
	if not l in ["1","2","3"]:
		print("Linha inválida! Tente novamente.\n")
		continue
	c = (input("Digite a coluna a ser jogada: "))
	if not c in ["1","2","3"]:
		print("Coluna inválida! Tente novamente.\n")
		continue
	l = int(l)-1; c = int(c)-1		
  
	if (board[l][c] != ' '):
		print("Posição já ocupada! Tente novamente.\n")
		continue
	print()
 
	board[l][c] = player[playerId]
	playerId = 1 - playerId
	turns += 1
	resp = verifyWin()
	if resp == 1:
		printBoard()
		print("Jogador X venceu!")
		break
	elif resp == 2:
		printBoard()
		print("Jogador O venceu!")
		break
	elif turns == 9:
		printBoard()
		print("Empate!")
		break