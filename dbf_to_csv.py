import os
from simpledbf import *


def dbf_to_csv(files):
    for filename in files:
        filepath = os.path.join('files_from_arcgis', filename)
        dbf = Dbf5(filepath)
        new_filename = filename.split('.')[0] + '.csv'
        new_filepath = os.path.join('files_from_arcgis', new_filename)
        dbf.to_csv(new_filepath)
    return


files_arcgis = os.listdir('files_from_arcgis')
dbf_to_csv(files_arcgis)
