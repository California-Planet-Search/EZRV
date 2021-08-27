import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad
from .update_database import *
config = yaml.safe_load(open("config/config.yaml"))


def improve_data(file_name):
    # df_internal = update_internal_dataframe()
    df_internal = pd.read_csv('Metadata/Internal_Simbad_Names.csv')
    df_update = update_headers(file_name)
    input_dict  = config['input_dict']
    input_names = df_update['Star_Name']
    unqiue_input_names = np.unique(input_names)
    database_names = df_internal['simbad_name']

    for i in range(len(unqiue_input_names)):
        table = Simbad.query_objectids(unqiue_input_names[i])
        simbad_name_input = np.array(table['ID'][0], 'str')

        match_name = np.where(simbad_name_input == database_names)[0]
        match_rows_inter = np.where( == )

        match_rows_new = np.where((unqiue_input_names[i] == input_names))[0]
        

        if np.any(match_name) == True:
            # print(match_rows)
            # print(df_internal['filename'].iloc[match_rows[0]])
            #match name of new file with file in database, then look at file in database and match instrument (match_instru = )and drop the data in the internal file

            df_internal.iloc[match_rows].drop(match_rows)

            #after the data is dropped, append to new file
            df_update.iloc[match_rows].to_csv(df_internal['filename'].iloc[match_name[0]], mode='a', index=False, header = None)

        if np.any(match_name) == False:
            #new file
