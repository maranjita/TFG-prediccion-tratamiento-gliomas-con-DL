# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:40:03 2026

@author: Usuario
"""

# -*- coding: utf-8 -*-
"""
Generador de diagrama de arquitectura multimodal (Late Fusion)
Adaptado para formato de memoria de TFG (Fondo claro con colores)
"""

import matplotlib.pyplot as plt

# Crear la figura y el lienzo con fondo blanco limpio
fig, ax = plt.subplots(figsize=(14, 11), facecolor='white')
ax.set_facecolor('white')

# Configurar límites del mapa de coordenadas (0 a 100)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# --- PALETA DE COLORES (Estilo Académico) ---
COLOR_VOLUMETRICO = '#E6F0FA'  # Azul muy claro
BORDE_VOLUMETRICO = '#1F77B4'  # Azul quirúrgico
COLOR_TABULAR = '#FFF5EB'      # Naranja muy claro
BORDE_TABULAR = '#E6550D'      # Naranja/Coral
COLOR_FUSION = '#EAF5EA'       # Verde muy claro
BORDE_FUSION = '#2CA02C'       # Verde esmeralda

# Estilos de las cajas de texto según su bloque
props_titulo = dict(boxstyle='square,pad=0.5', facecolor='none', edgecolor='none')

props_vol = dict(boxstyle='square,pad=0.8', facecolor=COLOR_VOLUMETRICO, 
                 edgecolor=BORDE_VOLUMETRICO, linewidth=1.8)

props_tab = dict(boxstyle='square,pad=0.8', facecolor=COLOR_TABULAR, 
                 edgecolor=BORDE_TABULAR, linewidth=1.8)

props_fus = dict(boxstyle='square,pad=0.8', facecolor=COLOR_FUSION, 
                 edgecolor=BORDE_FUSION, linewidth=1.8)

# --- DIBUJAR CAJAS Y TEXTOS ---

# Título Principal (Sin corchetes y en negro)
ax.text(50, 95, "ARQUITECTURA LATE FUSION", color='black', fontsize=20, 
        fontweight='bold', ha='center', va='center', bbox=props_titulo)

# Brazo Volumétrico - Izquierda (X = 20)
ax.text(20, 85, "Brazo Volumétrico: RMN 3D\n[128 x 128 x 64 x 6]", color='black', 
        fontsize=12, fontweight='bold', ha='center', va='center', bbox=props_titulo)

ax.text(20, 73, "3D-CNN (Conv + BN)", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_vol)

ax.text(20, 59, "Global Avg Pooling 3D", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_vol)

ax.text(20, 45, "FC 64 + Dropout (0.4)", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_vol)

# Brazo Tabular - Derecha (X = 80)
ax.text(80, 85, "Brazo Tabular: Metadatos\n[Vector: 32 Features]", color='black', 
        fontsize=12, fontweight='bold', ha='center', va='center', bbox=props_titulo)

ax.text(80, 73, "MLP Layer (FC 64 + ReLU)", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_tab)

ax.text(80, 59, "MLP Layer (FC 32 + ReLU)", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_tab)

# Bloques de Fusión y Salida - Centro (X = 50)
ax.text(50, 45, "Concatenation 1D", color='black', fontsize=13, 
        fontweight='bold', ha='center', va='center', bbox=props_fus)

ax.text(67, 45, "(Vector fusionado de 96 features)", color='#444444', 
        fontsize=11, style='italic', ha='left', va='center', bbox=props_titulo)

ax.text(50, 31, "FC 64 + Softmax", color='black', fontsize=12, 
        ha='center', va='center', bbox=props_fus)

ax.text(50, 18, "Salida (3 Clases)", color='black', fontsize=13, 
        fontweight='bold', ha='center', va='center', bbox=props_fus)


# --- CONFIGURACIÓN DE FLECHAS SIMÉTRICAS ---

# Estilo de las flechas (Líneas continuas gris oscuro/negro para mejor impresión en papel)
arrow_style = dict(arrowstyle="-|>", color='#222222', linestyle='-', linewidth=1.5, mutation_scale=15)

def dibujar_flecha(x_inicio, y_inicio, x_fin, y_fin):
    ax.annotate('', xy=(x_fin, y_fin), xytext=(x_inicio, y_inicio), arrowprops=arrow_style)

# Flechas verticales del Brazo Izquierdo
dibujar_flecha(20, 81, 20, 77)
dibujar_flecha(20, 69, 20, 63)
dibujar_flecha(20, 55, 20, 49)

# Flechas verticales del Brazo Derecho
dibujar_flecha(80, 81, 80, 77)
dibujar_flecha(80, 69, 80, 63)

# CORRECCIÓN DE DISTANCIA Y SIMETRÍA: Uniones perfectas en escuadra hacia la caja central
# Ambos parten de sus respectivas alturas hacia los laterales de Concatenation 1D (puntos X=37 y X=63)
ax.annotate('', xy=(37, 45), xytext=(20, 41),
            arrowprops=dict(arrowstyle="-|>", color='#222222', linestyle='-', linewidth=1.5, 
                            mutation_scale=15, connectionstyle="angle,angleA=0,angleB=90,rad=0"))

ax.annotate('', xy=(63, 45), xytext=(80, 55),
            arrowprops=dict(arrowstyle="-|>", color='#222222', linestyle='-', linewidth=1.5, 
                            mutation_scale=15, connectionstyle="angle,angleA=0,angleB=-90,rad=0"))

# Flechas del tronco común descendente
dibujar_flecha(50, 41, 50, 35)
dibujar_flecha(50, 27, 50, 22)


# --- DETALLES ESTÉTICOS FINALES ---

ax.axis('off')  # Ocultar los ejes cartesianos completamente
plt.tight_layout()

# Guardar la imagen en alta definición lista para insertar en Word o LaTeX
plt.savefig('arquitectura_tfg_clara.png', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')

# Mostrar el resultado final
plt.show()