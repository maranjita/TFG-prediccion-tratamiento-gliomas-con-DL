# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:45:55 2026

@author: Usuario
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# 1. CARGAR LOS DATOS
# Asegúrate de que esta ruta apunta a tu último archivo generado
ruta_input = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/UCSF_PDGM_LIMPIO_PARA_MLP_CLASES_V2.csv'
df = pd.read_csv(ruta_input)

# 2. ASEGURAR QUE 'ID' SEA TEXTO (String)
# A veces, si los IDs son solo números, Python los lee como int. 
# Lo forzamos a string para que MATLAB lo trate como identificador.
df['ID'] = df['ID'].astype(str)

# 3. ELIMINAR COLUMNAS DE SUPERVIVENCIA (Evitar Data Leakage)
# Eliminamos 'OS' y cualquier otra que dé pistas de la respuesta real
cols_a_eliminar = ['OS', '1-dead 0-alive']
df = df.drop(columns=[c for c in cols_a_eliminar if c in df.columns])

# 4. CREAR EL SPLIT ESTRATIFICADO (70% Train, 15% Val, 15% Test)
# Primero: separamos el 15% para el Test final
resto_df, test_df = train_test_split(
    df, 
    test_size=0.15, 
    stratify=df['clase_respuesta'], 
    random_state=42 # Para que el reparto sea siempre el mismo
)

# Segundo: del 85% restante, separamos el fragmento para Validación.
# (0.15 / 0.85 = 0.1765 aprox para que sea el 15% del total original)
train_df, val_df = train_test_split(
    resto_df, 
    test_size=0.1765, 
    stratify=resto_df['clase_respuesta'], 
    random_state=42
)

# 5. CREAR LA COLUMNA 'Set'
df['Set'] = ''
df.loc[train_df.index, 'Set'] = 'Train'
df.loc[val_df.index, 'Set'] = 'Validation'
df.loc[test_df.index, 'Set'] = 'Test'

# 6. VERIFICACIÓN DE SEGURIDAD
print("--- RESUMEN DEL REPARTO ---")
print(df['Set'].value_counts())
print("\n--- PROPORCIÓN DE CLASES EN TEST (Debe ser similar al original) ---")
print(test_df['clase_respuesta'].value_counts(normalize=True))

# 7. GUARDAR EL ARCHIVO MAESTRO PARA MATLAB
ruta_final = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/DATOS_TABULARES_FINAL_MATLAB_2.csv'
df.to_csv(ruta_final, index=False)

print(f"\n¡Éxito! Archivo 'MAESTRO' generado en: {ruta_final}")