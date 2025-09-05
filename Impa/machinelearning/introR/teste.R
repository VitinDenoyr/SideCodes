print("Hello World!")

# Logical (booleano)
logico <- TRUE
print(logico)
print(typeof(logico))  # "logiceal"

# Integer (inteiro)
inteiro <- 42L
print(inteiro)
print(typeof(inteiro))  # "integer"

# Double (numeric, ponto flutuante)
decimal <- 3.14
print(decimal)
print(typeof(decimal))  # "double"

# Complex
complexo <- 2 + 3i
print(complexo)
print(typeof(complexo))  # "complex"

# Character (string)
texto <- "Olá, R!"
print(texto)
print(typeof(texto))  # "character"

# Raw (byte cru)
byte <- as.raw(255)
print(byte)
print(typeof(byte))  # "raw"

# --- Valores especiais ---
faltando <- NA       # Valor ausente
indefinido <- NaN    # Not a number
infinito <- Inf      # Infinito positivo
nulo <- NULL         # Sem valor/objeto

print(faltando)
print(indefinido)
print(infinito)
print(nulo)

x <- 3 + 8
y <- 58 + 3
print((x + y))

print(y %/% x)

x <- "olá "
y <- "mundo"

k <- paste(x, y, x)
print(k)

print(bitwXor(1, 2))


#' Essa função tem o objetivo de calcular a soma de Gauss para um dado n.
#' Entrada: Um inteiro n >= 0
#' Saída: O resultado de 1+2+3+...+n
sum_to_n <- function(n){
	(n * (n + 1)) / 2
}

tetration <- function(b,exp){
	if(exp == 0) return(1)
	b^tetration(b,exp-1)
}

tetracao <- function(b,exp){
	res <- 1
	for(i in 1:exp){
		res <- (b^res)
	}
	res
}

print(tetration(2,4))
print(tetracao(2,4))

m <- c(50,30,13,513,3,6,3,25,31)
print(length(m))

ba <- matrix(
  c(1, 2, 3, 4, 5, 6, 7, 8, 9), 
  nrow = 3,   
  ncol = 3,         
  byrow = TRUE,     
)

print("")

print(exists("A"))

primos <- function(n){
	isprime <- rep(1,n)
	isprime[1] <- 0;
	for(i in 2:n){
		if(isprime[i]){
			if(i*i <= n){
				isprime[seq(i*i,n,i)] <- 0
			}
		}
	}
	isprime
}
print(primos(15))