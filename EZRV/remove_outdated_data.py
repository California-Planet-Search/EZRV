import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad
from .update_database import *
config = yaml.safe_load(open("config/config.yaml"))


def remove_outdated_data(file_name, input_instr,add_improved_data):
    # df_internal = update_internal_dataframe()
    df_internal = pd.read_csv('Metadata/Internal_Simbad_Names.csv')
    df_update = update_headers(file_name)
    input_dict  = config['input_dict']
    input_names = df_update['Star_Name']
    unqiue_input_names = np.unique(input_names)
    database_names = df_internal['simbad_name']
    instr_internal = df_update['Instrument']

    for i in range(len(unqiue_input_names)):
        table = Simbad.query_objectids(unqiue_input_names[i])
        simbad_name_input = np.array(table['ID'][0], 'str')
        #matches user input with star in our database
        match_name = np.where(simbad_name_input == database_names)[0]
        # match_rows_inter = np.where( == )
        match_instr = np.where(instr_internal == input_instr)[0]

        # match_rows_new = np.where(unqiue_input_names[i] == input_names)[0]

        if np.any(match_name) == True:
            # reads in dataframe of file

            df_file = pd.read_csv(df_internal['filename'].iloc[match_name[0]])
            print(df_file)

            drop_list = df_file.loc[df_file['Instrument'] == input_instr].index

            df_new = df_file.drop(drop_list)
            print(df_new)

            df_new.to_csv(df_internal['filename'].iloc[match_name[0]], index=False)
            #
            # if add_improved_data == True :
            #     update_database(file_name)
