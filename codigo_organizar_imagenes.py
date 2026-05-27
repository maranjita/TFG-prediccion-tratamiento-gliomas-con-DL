# -*- coding: utf-8 -*-
"""
PROYECTO: TFG - Organización de Dataset UCSF-PDGM
FECHA: Marzo 2026
DESCRIPCIÓN: Este script filtra 6 secuencias específicas de MRI en formato NIfTI.
"""

import os
import shutil

# --- CONFIGURACIÓN DEL USUARIO ---
# 1. Ruta de la carpeta donde están tus 500 pacientes actualmente
ruta_origen = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/PKG - UCSF-PDGM Version 5/UCSF-PDGM-v5 (IMAGENES)' 

# 2. Ruta donde quieres que se guarden las 6 secuencias filtradas
ruta_destino = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/imagenes_organizadas'

# 3. Lista de palabras clave que identifican tus 6 secuencias.
secuencias_interes = [
    '_T1_bias.nii', 
    '_T2_bias.nii', 
    '_FLAIR_bias.nii', 
    '_ADC.nii', 
    '_ASL.nii', 
    '_T1c_bias.nii'
]

# --- PROCESO AUTOMÁTICO ---

# Crear la carpeta de destino si no existe
if not os.path.exists(ruta_destino):
    os.makedirs(ruta_destino)
    print(f"Carpeta creada: {ruta_destino}")

conteo_archivos = 0
pacientes_procesados = 0

# Recorrer la carpeta de origen (Paciente por paciente)
for paciente in os.listdir(ruta_origen):
    path_paciente = os.path.join(ruta_origen, paciente)
    
    # Comprobar si es una carpeta
    if os.path.isdir(path_paciente):
        # Crear la carpeta del paciente en el destino
        nueva_carpeta_paciente = os.path.join(ruta_destino, paciente)
        
        # Listar archivos NIfTI dentro del paciente
        for archivo in os.listdir(path_paciente):
            # Solo procesar archivos .nii o .nii.gz
            if archivo.endswith(('.nii', '.nii.gz')):
                # Verificar si el nombre del archivo contiene alguna de nuestras palabras clave
                if any(keyword.lower() in archivo.lower() for keyword in secuencias_interes):
                    
                    # Si no existe la carpeta del paciente en destino, la creamos
                    if not os.path.exists(nueva_carpeta_paciente):
                        os.makedirs(nueva_carpeta_paciente)
                    
                    # Definir rutas de origen y destino final del archivo
                    origen_file = os.path.join(path_paciente, archivo)
                    destino_file = os.path.join(nueva_carpeta_paciente, archivo)
                    
                    # Copiar el archivo (shutil.copy2 mantiene fechas y metadatos)
                    shutil.copy2(origen_file, destino_file)
                    conteo_archivos += 1
        
        pacientes_procesados += 1
        if pacientes_procesados % 50 == 0:
            print(f"Progreso: {pacientes_procesados} pacientes revisados...")

print("-" * 30)
print(f"¡Proceso terminado!")
print(f"Pacientes procesados: {pacientes_procesados}")
print(f"Archivos copiados con éxito: {conteo_archivos}")