# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:16:50 2026

@author: Usuario
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar el dataset con tu ruta local
df = pd.read_csv('C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/UCSF-PDGM-metadata_v5.csv')

# 2. Configurar el estilo del gráfico para que sea académico
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# 3. Crear el histograma entrelazado por Sexo
sns.histplot(
    data=df, 
    x='Age at MRI', 
    hue='Sex', 
    multiple='stack',   # Apila las barras para ver el total acumulado
    palette={'M': '#1f77b4', 'F': '#ff7f0e'},  # Colores profesionales (azul y naranja apagado)
    bins=15,            # Número de agrupaciones de edad
    edgecolor='white',
    alpha=0.85
)

# 4. Añadir líneas con la media de edad para dar rigor técnico
mean_age = df['Age at MRI'].mean()
plt.axvline(mean_age, color='red', linestyle='--', linewidth=1.5, 
            label=f'Media de edad: {mean_age:.1f} años')

# 5. Personalizar etiquetas y títulos
plt.title('Distribución Demográfica de la Cohorte UCSF-PDGM (Edad y Sexo)', fontsize=14, pad=15, fontweight='bold')
plt.xlabel('Edad del Paciente en la RM (Años)', fontsize=12)
plt.ylabel('Número de Pacientes', fontsize=12)
plt.legend(title='Variables Demográficas', fontsize=10, title_fontsize=11)

# Limpiar los bordes del gráfico para un acabado más elegante
sns.despine(left=True, bottom=True)

# 6. Guardar la imagen en alta resolución (300 DPI es el estándar para impresión/TFG)
plt.tight_layout()
plt.savefig('distribucion_demografica_ucsf.png', dpi=300)
plt.show()

# =============================================================================
# BLOQUE NUEVO: CÁLCULO DE VALORES ESTADÍSTICOS Y REDACCIÓN AUTOMÁTICA
# =============================================================================
print("\n" + "="*50)
print("DATOS EPIDEMIOLÓGICOS")
print("="*50 + "\n")

# Cálculos estadísticos descriptivos
min_age = df['Age at MRI'].min()
max_age = df['Age at MRI'].max()
total_patients = len(df)

# Conteo y porcentajes de sexo biológico
sex_counts = df['Sex'].value_counts()
pct_male = (sex_counts.get('M', 0) / total_patients) * 100
pct_female = (sex_counts.get('F', 0) / total_patients) * 100

# Texto formateado listo para copiar y pegar
texto_tfg = f"""Media de edad: {mean_age:.1f} años \n 
Rango de {min_age} a {max_age} años \n
%Masculino:{pct_male:.1f}% \n
%Femenino: {pct_female:.1f}%"""

print(texto_tfg)
print("\n" + "="*50)