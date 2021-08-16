import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad

config = yaml.safe_load(open("config/config.yaml"))

#updates internal dataframe of files and first Simbad resolvable name
def update_internal_dataframe():
    df_internal = pd.DataFrame()
    database = glob.glob('Database/*.csv')
    df_internal['filename']  = np.array(database)
    df_internal['simbad_name'] = np.array(database)
    for i in range(len(df_internal['filename'] )):
        starname = df_internal['filename'][i][9:-4]
        table = Simbad.query_objectids(starname)
        simbad_name_internal = np.array(table['ID'], 'str')
        name = simbad_name_internal[0]

        df_internal['simbad_name'][i] = name

    return df_internal


# #updates headers of input file to our structure
def update_headers(file_name):
    input_dict  = config['input_dict']
    df = pd.read_csv(file_name)

    Time = np.ones(len(df), 'd')
    RV = np.ones_like(Time)
    Uncertainty = np.ones_like(Time)
    Observatory_Name = np.ones(len(df), 'str')

    df_update = pd.DataFrame()

    for i in range(len(list(input_dict.keys()))):
        dict_name = list(input_dict.keys())[i]

        if input_dict[dict_name][:9] != 'constant:' :
            df_update[dict_name] = df[str(input_dict[dict_name])]

        if input_dict[dict_name][:9] == 'constant:' :
            df_update[dict_name] = input_dict[dict_name][9:]

    return df_update

    #DONE!!^ updates the headers


    # # HAVE TO TEST! : needs information from previous functions, so I might combine them all since they dont work on their own
    # #combines new data with exisitng data
def update_database(file_name):
    df_internal = update_internal_dataframe()
    df_update = update_headers(file_name)
    input_dict  = config['input_dict']



    #match input star with database
    input_names = df_update['Star_Name']
    unqiue_input_names = np.unique(input_names)
    database_names = df_internal['simbad_name']

    # simbad_name_input = np.unique(input_names)

    for i in range(len(unqiue_input_names)):
        table = Simbad.query_objectids(unqiue_input_names[i])
        simbad_name_input = np.array(table['ID'][0], 'str')

        match_name = np.where(simbad_name_input == database_names)[0]
        match_rows = np.where(unqiue_input_names[i] == input_names)[0]

        # print(match_rows, df_update.iloc[match_rows])
    # #either appends existing file or creates new file
        if np.any(match_name) == True:
            df_update.iloc[match_rows].to_csv(df_internal['filename'].iloc[match_name[0]], mode='a+', index=False, header = None)
            #
            # print([i],input_names[i], simbad_name_input, df_update[match_rows])
            # print(df_internal['filename'].iloc[match_name[0]])

        if np.any(match_name) == False :
            path = r'Database/'
            df_update.iloc[match_rows].to_csv(path + unqiue_input_names[i]+ '.csv', index=False)
            # print(df_update[match_rows])
