import numpy as np
arr = np.array([10, 20, 30, 40, 50])
# Crear un filtro booleano
filtro = arr > 25
print("Filtro booleano:", filtro)
# Aplicar filtro al array
print("Elementos mayores a 25:", arr[filtro])