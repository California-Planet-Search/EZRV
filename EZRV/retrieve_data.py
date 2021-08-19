import numpy as np
import yaml
import pandas as pd
import glob
from astroquery.simbad  import Simbad
from .update_database import *

config = yaml.safe_load(open("config/config.yaml"))

def retrieve_data(input_star_name, test_query_simbad):
    table = Simbad.query_objectids(input_star_name)
    simbad_name_retrieve = np.array(table['ID'][0], 'str')
    print(simbad_name_retrieve)

    #convert to bjd calling from feis function call time_conversion(file_name) if they want conversion then adds the column to a new dataframe
    #similar true false as below




    #match simbad_name_retrieve to corresponding file in our database- use the first simbad name to match_name
    if test_query_simbad == True :
        df_internal = update_internal_dataframe()
        internal_starname = df_internal['simbad_name']
        print(internal_starname)
    if test_query_simbad == False :
        df_internal = pd.read_csv(config['default_directory'] + 'Internal_Simbad_Names.csv')


    match_name = np.where(df_internal == simbad_name_retrieve)[0]

    #if match == True then print data(dataframe)/data file and plot
