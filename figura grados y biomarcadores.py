# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:46:20 2026

@author: Usuario
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:35:00 2026

@author: Usuario
"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. CARGAR EL DATASET (Ruta local de tu equipo)
path = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/UCSF-PDGM-metadata_v5.csv'
df = pd.read_csv(path)

# Configuración de estilo académico
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11


# =============================================================================
# FIGURA 1: GRÁFICO DE DONA - DISTRIBUCIÓN DE GRADOS OMS
# =============================================================================
fig1, ax1 = plt.subplots(figsize=(7, 7))

# Extraer el conteo de la columna real 'WHO CNS Grade'
grade_counts = df['WHO CNS Grade'].value_counts().sort_index()
labels_grade = [f'Grado {int(i)}' for i in grade_counts.index]
colors_grade = ['#8da0cb', '#fc8d62', '#e78ac3'] 

wedges_g, texts_g, autotexts_g = ax1.pie(
    grade_counts, 
    labels=labels_grade, 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=colors_grade,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
    pctdistance=0.70,     
    labeldistance=1.1,    
    textprops={'fontsize': 12}
)

for autotext in autotexts_g:
    autotext.set_color('white')
    autotext.set_weight('bold')

# Añadir el círculo blanco en el centro
centre_circle = plt.Circle((0,0), 0.55, fc='white')
ax1.add_artist(centre_circle)
ax1.axis('equal')  

plt.title('Distribución Porcentual de Grados Histológicos OMS (N=501)', fontsize=14, pad=20, fontweight='bold')
plt.tight_layout()
plt.savefig('tfg_distribucion_grados_oms.png', dpi=300)
plt.show()

print("¡Figura 1 (Grados OMS) guardada con éxito!")


# =============================================================================
# FIGURA 2: MULTI-PLOT CON LEYENDA VERTICAL A LA DERECHA (SIN SOLAPAMIENTOS)
# =============================================================================
# Ensanchamos la imagen un poco más para que las leyendas de la derecha queden perfectas
fig2, axes = plt.subplots(1, 3, figsize=(22, 6.5))
paleta_base = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']

# Configuración limpia sin textos flotantes
config_tartas = {
    'autopct': '%1.1f%%',
    'startangle': 90,
    'wedgeprops': {'edgecolor': 'white', 'linewidth': 1.5, 'antialiased': True},
    'pctdistance': 0.65,
}

# --- Tarta 1: Mutaciones de IDH por Grado (83%, 67%, 8%) ---
idh_grados_valores = [83, 67, 8]
idh_labels = ['Grado II (83%)', 'Grado III (67%)', 'Grado IV (8%)']
colors_idh = ['#66c2a5', '#fc8d62', '#8da0cb']

wedges0, texts0, autotexts0 = axes[0].pie(
    idh_grados_valores,
    colors=colors_idh,
    **config_tartas
)
axes[0].set_title('Distribución de Mutaciones IDH\npor Grado Histológico', fontsize=13, pad=15, fontweight='bold')
axes[0].axis('equal')
# Leyenda vertical a la DERECHA
axes[0].legend(
    wedges0, idh_labels,
    title="Prevalencia",
    loc="center left",           # Anclaje izquierdo de la caja de la leyenda
    bbox_to_anchor=(1.05, 0.5),  # Lo mueve justo a la derecha (1.05) y centrado verticalmente (0.5)
    ncol=1,                      # Formato vertical
    frameon=True
)

# --- Tarta 2: Codeleción 1p/19q por Grado (20%, 5%, <1%) ---
codeleccion_valores = [20, 5, 0.5] 
labels_1p19q = ['Grado II (20%)', 'Grado III (5%)', 'Grado IV (<1%)']
colors_1p19q = ['#a6d854', '#ffd92f', '#e5c494']

wedges1, texts1, autotexts1 = axes[1].pie(
    codeleccion_valores,
    colors=colors_1p19q,
    **config_tartas
)
axes[1].set_title('Distribución de Codeleción 1p/19q\npor Grado Histológico', fontsize=13, pad=15, fontweight='bold')
axes[1].axis('equal')
# Leyenda vertical a la DERECHA
axes[1].legend(
    wedges1, labels_1p19q,
    title="Prevalencia",
    loc="center left",
    bbox_to_anchor=(1.05, 0.5),
    ncol=1,
    frameon=True
)

# --- Tarta 3: Hipermetilación de MGMT (Foco Grado IV - 63%) ---
mgmt_valores = [63, 37]
labels_mgmt = ['Grado IV Metilado (63%)', 'Otros Grados / No (37%)']
colors_mgmt = ['#e78ac3', '#b3b3b3']

wedges2, texts2, autotexts2 = axes[2].pie(
    mgmt_valores,
    colors=colors_mgmt,
    **config_tartas
)
axes[2].set_title('Detección del Promotor MGMT\nen la Cohorte', fontsize=13, pad=15, fontweight='bold')
axes[2].axis('equal')
# Leyenda vertical a la DERECHA
axes[2].legend(
    wedges2, labels_mgmt,
    title="Estado Promotor",
    loc="center left",
    bbox_to_anchor=(1.05, 0.5),
    ncol=1,
    frameon=True
)

# Formatear los porcentajes internos en blanco y negrita
todos_los_autotextos = autotexts0 + autotexts1 + autotexts2
for autotext in todos_los_autotextos:
    autotext.set_color('white')
    autotext.set_weight('bold')
    autotext.set_fontsize(11)

plt.suptitle('Análisis Estratificado de Biomarcadores Moleculares según Criterios OMS', fontsize=16, fontweight='bold', y=1.05)
plt.tight_layout()

# Aumentamos el wspace a 0.7 para dar un margen generoso a las leyendas derechas sin que pisen el siguiente gráfico
plt.subplots_adjust(wspace=0.7) 

# Guardar la imagen con los márgenes corregidos
plt.savefig('tfg_biomarcadores_filtrados.png', dpi=300, bbox_inches='tight')
plt.show()

print("¡Figura 2 corregida! Leyendas movidas a la derecha para evitar colisiones.")