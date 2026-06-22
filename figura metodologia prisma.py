# -*- coding: utf-8 -*-
'''
Created on Mon Jun 22 23:31:41 2026

@author: Usuario
'''
# -*- coding: utf-8 -*-

'''
Generador de Diagrama de Flujo PRISMA para Revisión Sistemática
Diseñado en formato claro y profesional para la memoria del TFG
'''

import os
import matplotlib.pyplot as plt

# Ajustamos la figura a una escala más compacta
fig, ax = plt.subplots(figsize=(11, 11), facecolor='white')
ax.set_facecolor('white')

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# --- PALETA DE COLORES ---
COLOR_ETAPA = '#FFF2CC'  # Amarillo pastel
BORDE_ETAPA = '#D6B656'  # Dorado/ocre suave
COLOR_BLOQUE = '#FFFFFF' 
BORDE_BLOQUE = '#000000' 

props_etapa = dict(boxstyle='round,pad=0.5', facecolor=COLOR_ETAPA, edgecolor=BORDE_ETAPA, linewidth=1.5)
props_bloque = dict(boxstyle='square,pad=0.8', facecolor=COLOR_BLOQUE, edgecolor=BORDE_BLOQUE, linewidth=1.2)

# =========================================================================
# 1. TEXTOS Y BLOQUES (COORDINADA X DE ETAPAS ACTUALIZADA A 22)
# =========================================================================

# --- ETAPA 1: IDENTIFICACIÓN (Y = 88) ---
ax.text(22, 88, "Identificación", color='black', fontsize=13, fontweight='bold', ha='center', va='center', rotation=90, bbox=props_etapa)

texto_identificacion = "Registros identificados en bases de datos\n    PubMed: 95\n    IEEE Xplore: 10\n    Web of Science: 273\n    arXiv: 4"
ax.text(48, 88, texto_identificacion, color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)


# --- ETAPA 2: DUPLICADOS (Y = 70) ---
ax.text(22, 70, "Duplicado", color='black', fontsize=13, fontweight='bold', ha='center', va='center', rotation=90, bbox=props_etapa)
ax.text(48, 70, "Número de artículos\nanalizados\nn = 282", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)
ax.text(83, 70, "Número de registros\neliminados por duplicados\nn = 97", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)


# --- ETAPA 3: CRIBADO (Y = 52) ---
ax.text(22, 52, "Cribado", color='black', fontsize=13, fontweight='bold', ha='center', va='center', rotation=90, bbox=props_etapa)
ax.text(48, 52, "Número de registros\ncribados:\nn = 26", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)
ax.text(83, 52, "Número de registros\nexcluidos: n = 259", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)


# --- ETAPA 4: IDONEIDAD (Y = 32) ---
ax.text(22, 32, "Idoneidad", color='black', fontsize=13, fontweight='bold', ha='center', va='center', rotation=90, bbox=props_etapa)
ax.text(48, 32, "Número de artículos\nde texto completo\nevaluados para su\nelegibilidad: \n n = 15", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)
ax.text(83, 32, "Número de artículos\nde texto completo\nexcluidos: n = 9", color='black', fontsize=11, ha='center', va='center', bbox=props_bloque)


# --- ETAPA 5: INCLUSIÓN (Y = 12) ---
ax.text(22, 12, "Inclusión", color='black', fontsize=13, fontweight='bold', ha='center', va='center', rotation=90, bbox=props_etapa)
ax.text(48, 12, "Estudios seleccionados\npara la revisión\nsistemática:\nn = 6", color='black', fontsize=11, fontweight='bold', ha='center', va='center', bbox=props_bloque)


# =========================================================================
# 2. CONFIGURACIÓN DE FLECHAS (RECALCULADAS PARA EL NUEVO CENTRO X=48)
# =========================================================================
arrow_style = dict(arrowstyle="-|>", color='black', linestyle='-', linewidth=1.5, mutation_scale=15)

def dibujar_flecha(x_inicio, y_inicio, x_fin, y_fin):
    ax.annotate('', xy=(x_fin, y_fin), xytext=(x_inicio, y_inicio), arrowprops=arrow_style)

# Flechas de la columna principal descendente (alineadas al nuevo centro X = 48)
dibujar_flecha(48, 80.5, 48, 75.5)
dibujar_flecha(48, 64.5, 48, 57.5)
dibujar_flecha(48, 46.5, 48, 39.5)
dibujar_flecha(48, 24.5, 48, 17.5)

# Flechas de exclusión laterales ajustadas de forma milimétrica
dibujar_flecha(60.5, 70, 70.5, 70)
dibujar_flecha(58.5, 52, 70.5, 52)
dibujar_flecha(61.5, 32, 70.5, 32)

ax.axis('off')
plt.tight_layout()

# Guardar la imagen optimizada
plt.savefig('diagrama_prisma_tfg.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()