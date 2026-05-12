import numpy as np

notas = np.array([4, 7, 9, 3, 10, 6])

resultado = np.where(notas >= 6, "Aprobado", "Desaprobado")

print(resultado)
