import pandas as pd
import numpy as np

data = {
    'Nome': ['Ana', 'Bruno', 'Carla', 'Daniel', 'Eva', 'Fábio'],
    'Departamento': ['Vendas', 'TI', 'Vendas', 'TI', 'Marketing', 'Vendas'],
    'Salario': [5000, 8000, 5500, 9500, 7000, np.nan],
    'Idade': [28, 35, 29, 41, 32, 27]
}
df = pd.DataFrame(data)

#Filtrar funcionários de TI com salário acima de 9000
ti_alto_salario = df[(df['Departamento'] == 'TI') & (df['Salario'] > 9000)]
print(ti_alto_salario)

# Filtrar funcionários que são de Vendas OU Marketing
vendas_ou_mkt = df[df['Departamento'].isin(['Vendas', 'Marketing'])]
print(vendas_ou_mkt)