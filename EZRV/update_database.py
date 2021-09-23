import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad

config = yaml.safe_load(open("config/config.yaml"))

#updates internal dataframe of files and first Simbad resolvable name
def update_internal_dataframe():
    print('updating database')
    df_internal = pd.DataFrame()
    database = glob.glob(config['default_directory'] + '/Database/*.csv')
    df_internal['filename']  = np.array(database)
    df_internal['simbad_name'] = np.array(database)
    print('querying Simbad')
    #queries Simbad
    for i in range(len(df_internal['filename'])):

        location_name = df_internal['filename'][i].find('Database/')

        starname = df_internal['filename'][i][location_name + 9: -4]
        table = Simbad.query_objectids(starname)
        simbad_name_internal = np.array(table['ID'], 'str')
        name = simbad_name_internal[0]

        df_internal['simbad_name'][i] = name

        df_internal.to_csv(config['default_directory'] + '/Metadata/Internal_Simbad_Names.csv')
    return df_internal


#updates headers of input file to new structure
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

    # combines new data with exisitng data
def update_database(file_name):

    df_internal = update_internal_dataframe()
    internal_starname = df_internal['simbad_name']

    df_update = update_headers(file_name)

    print(df_internal, df_update)
    input_dict  = config['input_dict']

    #match input star with database
    input_names = df_update['Star_Name']
    unqiue_input_names = np.unique(input_names)
    database_names = df_internal['simbad_name']
    time_newfile = df_update['Time']
    obser_new = df_update['Observatory_Site']


    for i in range(len(unqiue_input_names)):
        table = Simbad.query_objectids(unqiue_input_names[i])
        simbad_name_input = np.array(table['ID'][0], 'str')

        match_name = np.where(simbad_name_input == database_names)[0]
        match_rows = np.where((unqiue_input_names[i] == input_names))[0]
        print(unqiue_input_names[i],match_name,np.any(match_name)==True,np.any([2])==True)

        #either appends existing file or creates new file
        if np.any(match_name) == True:
            df_individual_star_file = pd.read_csv(df_internal['filename'].iloc[match_name[0]])
            time_individual_star_file = np.array(df_individual_star_file['Time'])
            obser_individual_star_file = np.array(df_individual_star_file['Observatory_Site'])

            print('updating '+unqiue_input_names[i])

            for j in range(len(match_rows)) :
                time_difference = np.array(time_individual_star_file - time_newfile[match_rows[j]])
                time_difference_min = np.min(time_difference)

                location_min = np.where(time_difference == time_difference_min)[0][0]

                obser_individual_star_file[location_min] == obser_new[match_rows[j]]

                if (time_difference_min < 2/24/3600) & (obser_individual_star_file[location_min] == obser_new[match_rows[j]]):
                    continue


                df_update.iloc[match_rows[j]].to_csv(df_internal['filename'].iloc[match_name[0]], mode='a', index=False, header = None)

        if np.any(match_name) == False :
            print('generating new file for '+unqiue_input_names[i])
            path = config['default_directory'] + '/Database/'
            df_update.iloc[match_rows].to_csv(path + unqiue_input_names[i]+ '.csv', index=False)
