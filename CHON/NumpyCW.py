import numpy as np

# Desde una lista
lista = [1, 2, 3, 4, 5]
arr1 = np.array(lista)
print("Array desde lista:", arr1)
# Desde una tupla
tupla = (10, 20, 30, 40)
arr2 = np.array(tupla)
print("Array desde tupla:", arr2)
# Array 2D (matriz)
lista2d = [[1, 2, 3], [4, 5, 6]]
arr3 = np.array(lista2d)
print("Array 2D:\n", arr3)