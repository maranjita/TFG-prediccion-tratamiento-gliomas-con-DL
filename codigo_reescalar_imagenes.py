# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:30:45 2026

@author: Usuario
"""

import os
import nibabel as nib
from nilearn.image import resample_img
import numpy as np

# --- CONFIGURACIÓN ---
ruta_origen = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/imagenes_organizadas'
ruta_destino = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/imagenes_reescaladas'

# Define el tamaño objetivo (puedes ajustarlo según la memoria de tu GPU)
# Un estándar equilibrado para TFG es 128x128x64 o 160x160x96
target_shape = (128, 128, 64) 

if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)

def reescalar_volumen(ruta_entrada, ruta_salida, new_shape):
    """Reescala un archivo NIfTI a las dimensiones deseadas."""
    img = nib.load(ruta_entrada)
    
    # Calculamos la nueva matriz de transformación (affine)
    # para que la imagen no pierda su orientación espacial
    shape = np.array(img.shape[:3])
    new_shape = np.array(new_shape)
    new_affine = img.affine.copy()
    
    # Ajustamos el affine basándonos en la proporción del cambio
    rescale_factor = shape / new_shape
    new_affine[:3, :3] = img.affine[:3, :3] * rescale_factor
    
    # Resample de la imagen
    img_rescaled = resample_img(img, target_affine=new_affine, target_shape=new_shape, interpolation='continuous')
    
    nib.save(img_rescaled, ruta_salida)

# --- BUCLE AUTOMÁTICO ---
print("Iniciando reescalado masivo...")

pacientes = [f for f in os.listdir(ruta_origen) if os.path.isdir(os.path.join(ruta_origen, f))]

for i, paciente in enumerate(pacientes):
    path_paciente_in = os.path.join(ruta_origen, paciente)
    path_paciente_out = os.path.join(ruta_destino, paciente)
    
    if not os.path.exists(path_paciente_out):
        os.makedirs(path_paciente_out)
    
    for archivo in os.listdir(path_paciente_in):
        if archivo.endswith(('.nii', '.nii.gz')):
            input_file = os.path.join(path_paciente_in, archivo)
            output_file = os.path.join(path_paciente_out, archivo)
            
            try:
                reescalar_volumen(input_file, output_file, target_shape)
            except Exception as e:
                print(f"Error en {archivo}: {e}")
                
    if (i + 1) % 10 == 0:
        print(f"Progreso: {i + 1}/{len(pacientes)} pacientes procesados.")

print(f"\n¡Terminado! Tus imágenes reescaladas están en: {ruta_destino}")