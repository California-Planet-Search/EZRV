import numpy as np
import yaml
import pandas as pd
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
from astroquery.simbad  import Simbad
from .update_database import *
from .bc_bjd import *
config = yaml.safe_load(open("config/config.yaml"))

def retrieve_data(input_star_name, test_query_simbad, test_bjd_conversion):
    table = Simbad.query_objectids(input_star_name)
    simbad_name_retrieve = np.array(table['ID'][0], 'str')
    print(simbad_name_retrieve)

    #match simbad_name_retrieve to corresponding file in our database- use the first simbad name to match_name
    print('retrieving data')
    if test_query_simbad == True :
        df_internal = update_internal_dataframe()
        internal_starname = df_internal['simbad_name']
        print(internal_starname)
    if test_query_simbad == False :
        df_internal = pd.read_csv(config['default_directory'] + '/Metadata/Internal_Simbad_Names.csv')


    match_name = np.where(df_internal['simbad_name'] == simbad_name_retrieve)[0]

    retrieve_file = df_internal['filename'].iloc[match_name[0]]

    if test_bjd_conversion == True:
        df_output = time_conversion(retrieve_file)
    if test_bjd_conversion == False:
        df_outuput = pd.read_csv(retrieve_file)

    print(df_output)


    #plot RV vs Time for retrieved file

    Time = np.array(df_output['Time'])
    RV = np.array(df_output['RV'])
    Uncert = np.array(df_output['Uncertainty'])
    rms = np.sqrt(np.mean(RV**2))
    print(rms)
    
    # plt.plot(Time,RV,'o')
    plt.figure()
    plt.errorbar(Time , RV, yerr = [Uncert, Uncert ], xerr=None, fmt= 'o')


    #add units!! for the labels and the naming for the title

    plt.xlabel('Time')
    plt.ylabel('Radial Velocity [m/s]')
    plt.title('RV vs Time')
    plt.legend()
    plt.show()
    plt.close()


    #add plot function!



    #if match == True then print data(dataframe)/data file and plot
