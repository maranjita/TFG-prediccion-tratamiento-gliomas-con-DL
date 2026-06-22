# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:42:55 2026

@author: Usuario
"""

import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# 1. CONFIGURA AQUÍ LAS RUTAS DE TUS ARCHIVOS NIfTI
# =========================================================================
# Ruta a la carpeta que contiene tus archivos .nii o .nii.gz
RUTA_BASE = r"C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/imagenes_organizadas/UCSF-PDGM-0004_nifti"

# Nombres exactos de tus archivos NIfTI mapeados con sus etiquetas
archivos_secuencias = {
    'ADC': 'UCSF-PDGM-0004_ADC.nii',
    'ASL': 'UCSF-PDGM-0004_ASL.nii',
    'FLAIR': 'UCSF-PDGM-0004_FLAIR_bias.nii',
    'T1': 'UCSF-PDGM-0004_T1_bias.nii',
    'T1c': 'UCSF-PDGM-0004_T1c_bias.nii',
    'T2': 'UCSF-PDGM-0004_T2_bias.nii'
}

# =========================================================================
# 2. FUNCIÓN PARA CARGAR NIfTI Y EXTRAER UN CORTE (SLICE) AXIAL
# =========================================================================
def cargar_cortes_nifti(ruta_base, diccionario_archivos):
    cortes_2d = {}
    
    for secuencia, nombre_archivo in diccionario_archivos.items():
        ruta_completa = os.path.join(ruta_base, nombre_archivo)
        
        # Verificar si el archivo existe
        if not os.path.exists(ruta_completa):
            print(f"⚠️ Alerta: No se encontró el archivo para {secuencia} en: {ruta_completa}")
            cortes_2d[secuencia] = np.zeros((256, 256)) # Matriz vacía de respaldo
            continue
            
        # Cargar el volumen NIfTI usando nibabel
        nifti_obj = nib.load(ruta_completa)
        volumen_data = nifti_obj.get_fdata()
        
        # Los volúmenes NIfTI suelen indexarse como (X, Y, Z) o (H, W, Slices)
        # Tomamos el corte axial central (eje Z)
        total_slices = volumen_data.shape[2]
        corte_central_idx = total_slices // 2 # Modifica este número si deseas otro nivel anatómico
        
        # Extraer el corte 2D
        corte_2d = volumen_data[:, :, corte_central_idx]
        
        # Rotar 90 grados para orientación anatómica estándar en matplotlib
        corte_2d = np.rot90(corte_2d)
        
        cortes_2d[secuencia] = corte_2d
        
    return cortes_2d

# Cargar los cortes de tus NIfTI reales
images = cargar_cortes_nifti(RUTA_BASE, archivos_secuencias)

# =========================================================================
# 3. CONFIGURACIÓN DEL PANEL Y VISUALIZACIÓN
# =========================================================================

# Crear la figura (2 filas, 3 columnas) con fondo negro
fig, axs = plt.subplots(2, 3, figsize=(15, 10), facecolor='black')
fig.subplots_adjust(wspace=0.05, hspace=0.2)

# CORRECCIÓN AQUÍ: Vinculación estricta con las llaves de tu diccionario de archivos
secuencias_layout = [
    ('T1', 'T1'),
    ('T2', 'T2'),
    ('FLAIR', 'FLAIR'),
    ('T1c', 'T1c (Gad)'),
    ('ADC', 'ADC'),
    ('ASL', 'ASL')
]

for i, (key, title) in enumerate(secuencias_layout):
    row = i // 3
    col = i % 3
    ax = axs[row, col]
    
    img_data = images[key]
    
    # Validar que la imagen no esté vacía
    if np.max(img_data) > 0:
        # CORRECCIÓN DE CONTRASTE: Filtra artefactos de alta intensidad (vmax al percentil 99.5)
        # Esto soluciona que las cajas aparezcan completamente blancas por discrepancias de rango.
        vmin = np.percentile(img_data, 1)
        vmax = np.percentile(img_data, 99.5)
        ax.imshow(img_data, cmap='gray', vmin=vmin, vmax=vmax)
    else:
        # Si la matriz está vacía, muestra el cuadro negro de fondo
        ax.imshow(img_data, cmap='gray')
    
    # Formato estético del panel
    ax.set_title(title, color='white', fontsize=16, y=-0.12)
    ax.axis('off')

plt.tight_layout()
plt.show()