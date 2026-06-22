# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:21:40 2026

@author: Maria Martin
"""

import os
import pandas as pd
import re

# 1. CONFIGURACIÓN DE RUTAS
ruta_base_imagenes = r'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/imagenes_reescaladas' 
ruta_csv = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/DATOS_TABULARES_FINAL_MATLAB_2.csv'
df = pd.read_csv(ruta_csv)

# 2. DEFINIR LOS SUFIJOS 
secuencias = {
    'Ruta_T1': 'T1_bias',
    'Ruta_T1c': 'T1c_bias',
    'Ruta_T2': 'T2_bias',
    'Ruta_FLAIR': 'FLAIR_bias',
    'Ruta_ADC': 'ADC',
    'Ruta_ASL': 'ASL'  
}

# 3. FUNCIÓN PARA NORMALIZAR EL ID (Ej: UCSF-PDGM-4 -> UCSF-PDGM-0004)
def normalizar_id(id_input):
    id_str = str(id_input).strip()
    # Buscamos el número al final del ID
    match = re.search(r'(\d+)$', id_str)
    if match:
        numero = int(match.group(1))
        # Formateamos a 4 dígitos con ceros a la izquierda
        return f"UCSF-PDGM-{numero:04d}"
    return id_str

# 4. FUNCIÓN DE BÚSQUEDA ROBUSTA
def buscar_archivo_maestro(id_original, sufijo_buscado):
    id_fijo = normalizar_id(id_original)
    nombre_carpeta = f"{id_fijo}_nifti"
    ruta_carpeta_paciente = os.path.join(ruta_base_imagenes, nombre_carpeta)
    
    if not os.path.exists(ruta_carpeta_paciente):
        return "CARPETA_NO_EXISTE"
    
    archivos_en_carpeta = os.listdir(ruta_carpeta_paciente)
    
    # Buscamos un archivo que:
    # 1. Contenga el ID normalizado (0004)
    # 2. Contenga el nombre de la secuencia (T1_bias, ASL, etc.)
    # 3. Termine en .nii o .nii.gz
    for archivo in archivos_en_carpeta:
        if id_fijo in archivo and sufijo_buscado in archivo:
            if archivo.endswith('.nii') or archivo.endswith('.nii.gz'):
                return os.path.normpath(os.path.join(ruta_carpeta_paciente, archivo))
    
    return "ARCHIVO_NO_ENCONTRADO"

# 5. EJECUCIÓN
print(f"Iniciando mapeo con normalización de IDs (padding de 4 dígitos)...")

# Aplicamos la normalización también a la columna ID del DataFrame para que coincida
df['ID_Original'] = df['ID'] # Guardamos el original por si acaso
df['ID'] = df['ID'].apply(normalizar_id)

for col_name, sufijo in secuencias.items():
    df[col_name] = df['ID'].apply(lambda x: buscar_archivo_maestro(x, sufijo))

# 6. VERIFICACIÓN FINAL
print("\n--- RESULTADOS DE BÚSQUEDA ---")
total_filas = len(df)
for col in secuencias.keys():
    encontrados = (~df[col].isin(["ARCHIVO_NO_ENCONTRADO", "CARPETA_NO_EXISTE"])).sum()
    print(f"{col}: {encontrados} de {total_filas} pacientes encontrados.")

# 7. GUARDAR
ruta_final_maestro = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/MAPA_MAESTRO_COMPLETO_2.csv'
df.to_csv(ruta_final_maestro, index=False)

print(f"\nProceso finalizado. Archivo guardado en: {ruta_final_maestro}")