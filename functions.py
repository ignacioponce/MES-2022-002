import pandas as pd
import os


def read_from_arcgis(truck, separador=';'):
    """ --- Descripción:
           Lee los archivos de entrada y los funde en una única estructura de datos
     --- Parámetros de entrada:
           files: lista con nombres de los archivos .csv [list of strings]
           separador (default -> ';'): Caracter con que están separaradas las columnas en archivo .scv [str]
     --- Salida:
           return: Dataframe con datos de todos los archivos [pd.DataFrame]
    """
    assert type(truck) == str
    filepath = os.path.join('files_from_arcgis', truck)
    files = os.listdir(filepath)
    for filename in files:
        filepath = os.path.join('files_from_arcgis', truck, filename)
        if filename == files[0]:
            df = pd.read_csv(filepath, sep=',').rename(columns={'Rampa': 'Camino'})
        else:
            df_aux = pd.read_csv(filepath, sep=',').rename(columns={'Rampa': 'Camino'})
            df = df.append(df_aux, ignore_index=True)
    df = df.dropna(how='all')
    df = df.sort_values(by='field_1', ascending=True)
    df = df.reset_index(drop=True)
    df = df.drop(columns=['FID_Pol_en', 'MC', 'FID_Pol_ME', 'FID_Pol_ou', 'FID_Pol_SL'])
    df = df.drop(columns=[df.keys()[0]])
    df = df.rename(columns={'field_1': 'FID', 'F_': 'N°', 'VOLUMEN_CO': 'VOLUMEN CONSUMIDO (DIFERENCIAL)',
                            'Distancia': 'Distancia por GNSS', 'RASTERVALU': 'Elev_Corregida'})
    df = df.fillna('NA')
    return df


def fecha_desde_arcgis(df):
    ano = df['ANO'].astype(str)
    mes = df['MES'].astype(str).str.zfill(2)
    dia = df['DIA'].astype(str).str.zfill(2)

    fecha = ano.str.cat(mes, sep='-').str.cat(dia, sep='-')

    hora = df['HORA'].astype(str).str.zfill(2)
    minuto = df['MIN'].astype(str).str.zfill(2)
    seg = df['SEG'].astype(str).str.zfill(2)

    hora = hora.str.cat(minuto, sep=':').str.cat(seg, sep=':')

    fecha_y_hora = fecha.str.cat(hora, sep=' ').rename('FECHA Y HORA')
    df = df.join(fecha_y_hora)
    return df


def pendiente(df):
    s_o_b = []
    for k in range(len(df)):
        s_o_b.append('NA')
    df = df.join(pd.Series(s_o_b, name='Direccion_pendiente'))
    tramo_actual = 'NA'
    primer_registro = 0
    for n_fila in range(len(df) - 1):
        print(f'Progreso {n_fila * 100 / len(df)} %')
        fila = df.loc[n_fila + 1, :]
        fila_anterior = df.loc[n_fila, :]
        tramo = fila['Tramo']
        tramo_anterior = fila_anterior['Tramo']
        if tramo != tramo_anterior:
            if tramo_anterior != 'NA':
                ultimo_registro = n_fila
                assert df.loc[primer_registro, 'Tramo'] == df.loc[ultimo_registro, 'Tramo']
                pendiente = df.loc[primer_registro, 'Pendiente']
                if pendiente <= 3:
                    # Pendiente plana
                    df.loc[primer_registro:ultimo_registro, 'Direccion_pendiente'] = 'plano'
                else:
                    # Pendiente bajando o subiendo
                    # Mas de un registro
                    if primer_registro != ultimo_registro:
                        diff_elev = df.loc[ultimo_registro, 'Elev_Corregida'] - df.loc[
                            primer_registro, 'Elev_Corregida']
                    else:
                        # Registro único, se toma según la elevación del punto anterior
                        diff_elev = df.loc[ultimo_registro, 'Elev_Corregida'] - df.loc[
                            ultimo_registro - 1, 'Elev_Corregida']
                    if diff_elev > 0:
                        df.loc[primer_registro:ultimo_registro, 'Direccion_pendiente'] = 'subiendo'
                    elif diff_elev < 0:
                        df.loc[primer_registro:ultimo_registro, 'Direccion_pendiente'] = 'bajando'
                    else:
                        df.loc[primer_registro:ultimo_registro, 'Direccion_pendiente'] = 'warning'
            tramo_actual = tramo
            primer_registro = n_fila + 1
        else:
            pass
    return df


def cambios_carga(df):
    cat_carga_init = df.loc[0, 'Cat_Carga']
    ilocs_cambios = [0]
    cat_cambios = [cat_carga_init]
    for n_fila in range(int(len(df)/5)):
        print(f'Progreso {n_fila * 100 / len(df)} %')
        fila = df.loc[n_fila + 1, :]
        fila_anterior = df.loc[n_fila, :]
        if fila['Cat_Carga'] != fila_anterior['Cat_Carga']:
            iloc = n_fila + 1
            cat_cambio = fila['Cat_Carga']
            ilocs_cambios.append(iloc)
            cat_cambios.append(cat_cambio)
    df_cambios_carga = pd.Series(cat_cambios, index=ilocs_cambios)
    return df_cambios_carga