import pandas as pd
import os

files = ["377_Muestra_Filtrada.xlsx", "886_Muestra_Filtrada.xlsx", "888_Muestra_Filtrada.xlsx"]

for file in files:
    # Lee archivo excel crudo
    df = pd.read_excel(os.path.join('input_files', file), sheet_name='Toda_Data')
    # Corrige formato coordenadas
    df_coordenadas = df['Coordenadas'].str.split(',', expand=True).rename(columns={0: 'Latitud', 1: 'Longitud'})
    # Corrige formato fecha y hora para leer con ArcGIS
    df_fecha_hora = df['Hora'].str.split(' ', expand=True).rename(columns={0: 'Fecha', 1: 'Hora'})
    df_ano_mes_dia = df_fecha_hora['Fecha'].str.split('-', expand=True).rename(columns={0: 'ANO', 1: 'MES', 2: 'DIA'})
    df_hora_min_seg = df_fecha_hora['Hora'].str.split(':', expand=True).rename(columns={0: 'HORA', 1: 'MIN', 2: 'SEG'})
    df = df.drop(columns=['Hora', 'Coordenadas'])
    df = df.join(df_ano_mes_dia).join(df_hora_min_seg).join(df_coordenadas)
    # Exporta BD en .csv
    df.to_csv(file.split('.')[0] + '.csv', sep=';', decimal='.')
