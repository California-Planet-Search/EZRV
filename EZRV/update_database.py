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

    # print(df_update)

    input_dict  = config['input_dict']

    #match input star with database
    input_names = np.array(df_update['Star_Name'],'str')
    unqiue_input_names = np.unique(input_names)
    database_names = np.array(df_internal['simbad_name'], 'str')
    time_newfile = np.array(df_update['Time'], 'd')
    obser_new = np.array(df_update['Observatory_Site'], 'str')

    # print(df_update)

    for i in range(len(unqiue_input_names)):
        table = Simbad.query_objectids(unqiue_input_names[i])
        simbad_name_input = str(table['ID'][0])

        match_name = np.where(database_names == simbad_name_input)[0]
        match_rows = np.where((input_names == unqiue_input_names[i]))[0]


        #either appends existing file or creates new file
        if np.any(match_name) == True:
            df_individual_star_file = pd.read_csv(df_internal['filename'].iloc[match_name[0]])
            time_individual_star_file = np.array(df_individual_star_file['Time'])
            obser_individual_star_file = np.array(df_individual_star_file['Observatory_Site'])

            print('updating '+unqiue_input_names[i])

            for j in range(len(match_rows)) :
                time_difference = np.array(abs(time_individual_star_file - time_newfile[match_rows[j]]))
                time_difference_min = np.min(time_difference)

                location_min = np.where(time_difference == time_difference_min)[0][0]

                

                if (time_difference_min < 2/24/60) & (obser_individual_star_file[location_min] == obser_new[match_rows[j]]):
                    continue

                #option to print what new dataframe looks like
                # print(df_update)



                df_update.iloc[[match_rows[j]]].to_csv(df_internal['filename'].iloc[match_name[0]], mode='a', index=False, header = None)

        if np.any(match_name) == False :
            print('generating new file for '+unqiue_input_names[i])
            path = config['default_directory'] + '/Database/'
            df_update.iloc[match_rows].to_csv(path + unqiue_input_names[i]+ '.csv', index=False)
