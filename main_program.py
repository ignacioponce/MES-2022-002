# Importación de funciones y librerías
from functions import *

# ------------------------------------------

# Lectura de datos desde ArcGIS
df_377 = read_from_arcgis("377")
df_886 = read_from_arcgis("886")
df_888 = read_from_arcgis("888")

# Correción de formato de fecha y hora
df_377 = fecha_desde_arcgis(df_377)
df_886 = fecha_desde_arcgis(df_886)
df_888 = fecha_desde_arcgis(df_888)

#df_377 = pendiente(df_377)
#df_886 = pendiente(df_886)
#df_888 = pendiente(df_888)

df_377_cambios_carga = cambios_carga(df_377)
#df_886 = carga(df_886)
#df_888 = carga(df_888)
