# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:51:33 2026

@author: Usuario
"""

import pandas as pd

# 1. CARGAR LOS DATOS
# Cambia la ruta por la de tu archivo
ruta_entrada = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/UCSF-PDGM-metadata_v5.csv'
df = pd.read_csv(ruta_entrada)

# 2. DEFINIR LA FUNCIÓN DE CLASIFICACIÓN
def definir_clase(row):
    os = row['OS']
    status = row['1-dead 0-alive']  # 1=fallecido, 0=vivo
    
    # Clase 1: Buena (Más de 450 días, da igual si vivo o muerto)
    if os > 450:
        return 1
    
    # Clase 2: Intermedia (181-450 días y SOLO fallecidos)
    elif 181 <= os <= 450 and status == 1:
        return 2
    
    # Clase 3: Pobre (0-180 días y SOLO fallecidos)
    elif os <= 180 and status == 1:
        return 3
    
    # Pacientes vivos con menos de 450 días: No se pueden clasificar con certeza
    else:
        return None

# 3. APLICAR LA LÓGICA
df['clase_respuesta'] = df.apply(definir_clase, axis=1)

# 4. LIMPIEZA PARA LA RED NEURONAL
# Eliminamos los pacientes que quedaron como None (los que no podemos asegurar su clase)
# Esto asegura que tu red solo aprenda de casos confirmados.
df_final = df.dropna(subset=['clase_respuesta'])

# Convertimos la clase a entero (para que no sea 1.0, 2.0...)
df_final['clase_respuesta'] = df_final['clase_respuesta'].astype(int)

# 5. GUARDAR EL RESULTADO
ruta_salida = 'C:/Users/Usuario/Documents/UAX/4º/TFG/DATOS/UCSF_PDGM_etiquetado_clases.csv'
df_final.to_csv(ruta_salida, index=False)

print("--- Resumen del Etiquetado ---")
print(f"Pacientes Clase 1 (Buena): {len(df_final[df_final['clase_respuesta']==1])}")
print(f"Pacientes Clase 2 (Intermedia): {len(df_final[df_final['clase_respuesta']==2])}")
print(f"Pacientes Clase 3 (Pobre): {len(df_final[df_final['clase_respuesta']==3])}")
print(f"Pacientes excluidos (vivos < 450 días): {df['clase_respuesta'].isna().sum()}")
print(f"\nArchivo guardado en: {ruta_salida}")