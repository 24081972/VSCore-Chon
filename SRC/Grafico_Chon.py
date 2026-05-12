import pandas as pd
import matplotlib.pyplot as plt

# 1. Los datos del proceso
datos = {
    'Estación': ['Cataforesis', 'Primer', 'Color', 'Barniz'],
    'Eficiencia': [98.5, 94.2, 92.8, 96.1]
}

df = pd.DataFrame(datos)

# 2. Creamos el gráfico
plt.figure(figsize=(8, 5)) # Tamaño de la ventana
plt.bar(df['Estación'], df['Eficiencia'], color='skyblue')

# 3. Decoración (Modo Reporte)
plt.title('Eficiencia por Estación de Pintado', fontsize=14)
plt.xlabel('Estaciones', fontsize=12)
plt.ylabel('% Eficiencia', fontsize=12)
plt.ylim(0, 110) # Para que la escala sea de 0 a 110
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 4. Mostrar el gráfico
plt.show()