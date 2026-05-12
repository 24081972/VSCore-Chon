import pandas as pd
import numpy as np

# Creamos un pequeño reporte de prueba
datos = {
    'Estación': ['Cataforesis', 'Primer', 'Color', 'Barniz'],
    'Eficiencia': [98.5, 94.2, 92.8, 96.1],
    'Unidades': [120, 115, 112, 118]
}

df = pd.DataFrame(datos)

print("--- Reporte de Proceso ---")
print(df)
print("\nPromedio de Eficiencia:", df['Eficiencia'].mean())
